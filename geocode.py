import httplib2
import json
import os

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']


def getGeocodeLocation(inputString):
    locationString = inputString.replace(" ", "+")
    url = ("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %
           (locationString, GOOGLE_API_KEY))
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(str(content, "utf-8"))
    # print(result['results'][0]['geometry']['location'])
    loc = result['results'][0]['geometry']['location']
    # latitude = result['results'][0]['geometry']['location']['lat']
    # longitude = result['results'][0]['geometry']['location']['lng']
    latitude = loc['lat']
    longitude = loc['lng']
    return (latitude, longitude)
#
# print(getGeocodeLocation('chittagong'))
