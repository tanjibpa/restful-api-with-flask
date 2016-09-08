from flask import Blueprint, request
from find_restaurant.api.findRestaurant import getGeocodeLocation
from find_restaurant.api.query import editARestaurant, addRestaurant, getARestaurant, getAllRestaurants, deleteRestaurant, check_api_key
from find_restaurant import dbsession
from find_restaurant.member.models import UserPref
import json

api = Blueprint('api', __name__)


@api.route('/restaurants', methods=['GET', 'POST'])
@check_api_key
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


@api.route('/restaurant/<string:restaurant_id>', methods=['GET', 'DELETE'])
@check_api_key
def getRestaurant(restaurant_id):
    if request.method == 'GET':
        return getARestaurant(restaurant_id)
    if request.method == 'DELETE':
        return deleteRestaurant(restaurant_id)

@api.route('/restaurant/edit', methods=['PUT'])
@check_api_key
def editRestaurant():
    if request.method == 'PUT':
        restaurant_info = request.get_json()
        print(request.get_json())
        data = editARestaurant(restaurant_info)
        return data
