import httplib2
import json
from find_restaurant.api.geocode import getGeocodeLocation
from config import GOOGLE_API_KEY


def findRestaurants(lat, long):
    url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s"\
          "&radius=%s"\
          "&type=%s"\
          "&key=%s" % (lat, long, 50000, 'restaurant', GOOGLE_API_KEY))

    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content.decode('utf-8'))

    result_json = []

    for i in range(len(result['results'])):
        result_json.append(result['results'][i]['name'])
    # print(result['results'][0].keys())
    return json.dumps(result['results'])
    # return result['results'][0]['name']

# print(findRestaurants(22.3475365, 91.8123324))
