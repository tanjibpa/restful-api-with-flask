from flask import render_template, request, make_response, Blueprint, g, url_for, redirect, session
from find_restaurant import dbsession
from find_restaurant.member import authentications
from find_restaurant.member.models import User, UserPref
from find_restaurant.member.authentications import auth, google_login, verify_token
import httplib2
import json
import requests

members = Blueprint('members', __name__, template_folder='templates', static_folder='static')

@members.route('/clientOAuth')
def start():
    return render_template('member/oauthclient.html')


@members.route('/oauth/<string:provider>', methods=['POST'])
def oauth_result(provider):
    auth_code = request.json.get('code')
    # auth_code = request.args.get('code')
    if provider == 'google':
        access_token = google_login(auth_code)
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            return response
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()
        name = data['name']
        email = data['email']
        picture = data['picture']

        # TODO: Email authentication
        user = dbsession.query(User).filter_by(email=email).first()
        if not user:
            user = User(username=name, picture=picture, email=email)
            # user_pref = UserPref(user_id=user.id)
            # user_pref.generate_api_key()
            dbsession.add(user)
            dbsession.commit()

        token = user.generate_auth_token(600)
        # g.user = user
        return url_for('members.authenticate_user', token=token)


@members.route('/authenticate')
def authenticate_user():
    token = request.args.get('token')
    if verify_token(token):
        session['user_id'] = g.user.id
        return redirect(url_for('members.user_login'))
    return render_template('member/404.html')

@members.route('/user')
def user_login():
    if 'user_id' in session:
        user = dbsession.query(User).filter_by(id=session['user_id']).one()
        user_pref = dbsession.query(UserPref).filter_by(id=session['user_id']).first()
        if user_pref is None:
            user_pref = UserPref(id=session['user_id'])
            user_pref.generate_api_key()
            dbsession.add(user_pref)
            dbsession.commit()
        return render_template('member/dashboard.html',
                                name=user.username,
                                picture=user.picture,
                                email=user.email,
                                api_key=user_pref.api_key)
    return redirect(url_for('members.start'))

@members.route('/logout')
def index():
    session.pop('user_id', None)
    return redirect(url_for('members.start'))
