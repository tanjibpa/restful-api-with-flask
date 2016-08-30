from flask import Flask, request, jsonify, abort, g, render_template, make_response, Response, redirect, url_for
from flask import session as flask_session
from findRestaurant import findRestaurants
from geocode import getGeocodeLocation
from models import Base, Restaurant, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from oauth2client import client
import json
import os
import httplib2
import requests
from functools import wraps

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine(os.environ['DATABASE_URI'])
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()
app = Flask(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not verify_password(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/clientOAuth')
def start():
    return render_template('oauthclient.html')


@app.route('/dashboard')
def user_dashboard():
    return render_template('dashboard.html')


@app.route('/oauth/<string:provider>', methods=['POST'])
def login(provider):
    # auth_code = request.json.get('code')
    auth_code = request.json.get('code')
    if provider == 'google':
        try:
            oauth_flow = client.OAuth2WebServerFlow(
                client_id='850414830066-0s13h14gti05jectsabuke1vp6io68ct.apps.googleusercontent.com',
                client_secret='tcG9arN1iKntz7PQ86vWepCb',
                scope='profile email',
                redirect_uri='http://localhost:5000/dashboard')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except client.FlowExchangeError:
            response = make_response(json.dumps('Failed to upgrade the authorization code.'), 201)
            response.headers['Content-Type'] = 'application/json'
            return response
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            return response
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()
        name = data['name']
        email = data['email']
        picture = data['picture']
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(username=name, picture=picture, email=email)
            session.add(user)
            session.commit()

        token = user.generate_auth_token()
        return jsonify({ 'token': token.decode('ascii') })
        # flask_session['name'] = name
        # flask_session['token'] = token
        # return redirect(url_for('user_dashboard', name=name, token=token.decode('utf-8')))
    else:
        # return 'Unrecognized provider'
        return False

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('utf-8')})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201


@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).first()
    print(user.username)
    if not user:
        abort(400)
    return jsonify(user.username)

@app.route('/restaurants', methods=['GET', 'POST'])
@auth.login_required
def loadRestaurants():
    if request.method == 'POST':
        location_name = request.args.get('location', '')
        latitude, long = getGeocodeLocation(location_name)
        all_restaurants = json.loads(findRestaurants(str(latitude), str(long)))
        for restaurant in all_restaurants:
            addRestaurant(restaurant)
        return "Added to database."
    if request.method == 'GET':
        return getAllRestaurants()


def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [i.serialize for i in restaurants])

@app.route('/restaurant/<string:restaurant_id>', methods=['GET', 'DELETE'])
@auth.login_required
def getARestaurant(restaurant_id):
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
        return jsonify(Restaurant = restaurant.serialize)
    if request.method == 'DELETE':
        return deleteRestaurant(restaurant_id)

def addRestaurant(restaurant_info):
    if not session.query(Restaurant).filter_by(restaurant_id=restaurant_info['place_id']).first():
        try:
            if restaurant_info['rating']:
                rating = restaurant_info['rating']
        except:
           rating = 0
        restaurant = Restaurant(name=restaurant_info['name'],
                                restaurant_id=restaurant_info['place_id'],
                                address=restaurant_info['vicinity'],
                                rating=str(rating),
                                types=', '.join([i for i in restaurant_info['types']]))
        session.add(restaurant)
        session.commit()
        return jsonify(Restaurant=[restaurant.serialize])

def deleteRestaurant(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
        session.delete(restaurant)
        session.commit()
        return jsonify(Restaurant = {'result': "Removed restaurant with ID: %s" % restaurant_id})
    except Exception:
        return jsonify(Restaurant={'result': "There's no restaurant with ID: %s" % restaurant_id})


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
