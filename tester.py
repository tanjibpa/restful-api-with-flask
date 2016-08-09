import os
import httplib2
import json
import unittest
from models import Restaurant, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from findRestaurant import findRestaurants
from geocode import getGeocodeLocation


class RestaurantTester(unittest.TestCase):

    def setUp(self):
        self.address = 'http://localhost:5000'
        self.h = httplib2.Http()
        engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBsession = sessionmaker(bind=engine)
        self.session =  DBsession()
        self.load_restaurants()

    def tearDown(self):
        db_file = os.path.dirname(os.path.abspath(__file__)) + '/test.db'
        os.remove(db_file)

    def load_restaurants(self):
        location_name = 'chittagong,bangladesh'
        latitude, long = getGeocodeLocation(location_name)
        all_restaurants = json.loads(findRestaurants(str(latitude), str(long)))
        for restaurant in all_restaurants:
            self.addRestaurant(restaurant)

    def addRestaurant(self, restaurant_info):
        if not self.session.query(Restaurant).filter_by(restaurant_id=restaurant_info['place_id']).first():
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
            self.session.add(restaurant)
            self.session.commit()

    def test_get_restaurant(self):
        url = self.address + '/restaurants?location=chittagong,bangladesh'
        resp, result = self.h.request(url, 'POST')
        self.assertEqual(resp['status'], '200')

    def test_get_all_restaurants(self):
        url = self.address + '/restaurants'
        resp, result = self.h.request(url, 'GET')
        self.assertEqual(resp['status'], '200')

    def test_read_a_restaurant(self):
        restaurant = self.session.query(Restaurant).all()
        restaurant_id = restaurant[-1].restaurantId()
        url = self.address + '/restaurant/%s' % restaurant_id
        resp, content = self.h.request(url, 'GET')
        self.assertEqual(resp['status'], '200')


if __name__ == '__main__':
    unittest.main()


