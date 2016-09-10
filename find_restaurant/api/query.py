from flask import jsonify, request
from find_restaurant import dbsession
from find_restaurant.api.models import Restaurant
from find_restaurant.member.models import UserPref
from functools import wraps


def check_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.args.get('api_key')
        if dbsession.query(UserPref).filter_by(api_key=api_key).first() is None:
            return jsonify(Restaurant = {"error": "Access Denied"})
        return f(*args, **kwargs)
    return wrapper


def getAllRestaurants():
    restaurants = dbsession.query(Restaurant).all()
    return jsonify(Restaurants = [i.serialize for i in restaurants])


def getARestaurant(restaurant_id):
    restaurant = dbsession.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
    return jsonify(Restaurant = restaurant.serialize)


def addARestaurant(restaurant_info):
    try:
        if not dbsession.query(Restaurant).filter_by(restaurant_id=restaurant_info['place_id']).first():
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
            dbsession.add(restaurant)
            dbsession.commit()
            return jsonify(Restaurant = {"success": "Restaurant with ID: %s successfully added."})
    except KeyError:
        return jsonify(Restaurant = {"error": "key doesn't macth."})


def deleteRestaurant(restaurant_id):
    try:
        restaurant = dbsession.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
        dbsession.delete(restaurant)
        dbsession.commit()
        return jsonify(Restaurant = {"success": "Removed restaurant with ID: %s" % restaurant_id})
    except Exception:
        return jsonify(Restaurant = {"error": "There's no restaurant with ID: %s" % restaurant_id})


def editARestaurant(restaurant_info):
    try:
        restaurant_id = restaurant_info['restaurant_id']
        restaurant = dbsession.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
        if restaurant is not None:
            for i in restaurant_info:
                print(i)
                if i not in restaurant.properties():
                    return jsonify(Restaurant = {"error" : "%s is not a restaurant property." % i})
                setattr(restaurant, i, restaurant_info[i])
                dbsession.commit()
                print("%s added" % i)
            return jsonify(Restaurant = {"success": "Restaurant with ID: %s successfully updated." % restaurant_id})
        return jsonify(Restaurant = {"error": "There's no restaurant with ID: %s" % restaurant_id})
    except KeyError:
        return jsonify(Restaurant = {"error": "restaurant_id key is not provided."})
