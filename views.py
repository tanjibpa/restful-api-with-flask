from findRestaurant import findRestaurants
from geocode import getGeocodeLocation
from models import Base, Restaurant
from flask import Flask, request, jsonify
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()
app = Flask(__name__)


@app.route('/restaurants', methods=['GET', 'POST'])
def loadRestaurants():
    if request.method == 'POST':
        location_name = request.args.get('location', '')
        latitude, long = getGeocodeLocation(location_name)
        all_restaurants = json.loads(findRestaurants(str(latitude), str(long)))
        # print(type(all_restaurants))
        for restaurant in all_restaurants:
            addRestaurant(restaurant)
        return "Added to database."
    if request.method == 'GET':
        return getAllRestaurants()


@app.route('/restaurant/<string:restaurant_id>', methods=['GET', 'DELETE'])
def getARestaurant(restaurant_id):
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
        return jsonify(Restaurant = restaurant.serialize)
    if request.method == 'DELETE':
        return deleteRestaurant(restaurant_id)



def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [i.serialize for i in restaurants])

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
                                rating=rating,
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
    # else:
    #     return jsonify(Restaurant = {'result': "There's no restaurant with ID: %s" % restaurant_id})


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
