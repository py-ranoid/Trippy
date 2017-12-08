import requests
import pandas as pd

YOUR_API_KEY = 'AIzaSyBebwYnPp4vPegob7TckO9oEZ8rP0j6W6k'
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=24.5709329,73.6762453&radius=7000&keyword=%s&key=' + YOUR_API_KEY

def generate_place_details(place = "Udaipur"):
    df = pd.read_pickle('../BasicCityData/' + place + '/mutual_visits.pkl')
    place_list = list(df.index)
    details = {}
    for place in place_list:
        details[place] = []
        query_url = url % '%20'.join(place.split(' '))
        r = requests.get(query_url)
        result = r.json()['results'][0]

        name = place
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']

        gname = result['name']
        place_id = result['place_id']
        vicinity = result['vicinity']
        details[place] = {
            'TA_name': place,
            'Google_name': gname,
            'lat': lat,
            'lng': lng,
            'Place_id': place_id,
            'Vicinity': vicinity
        }
    df = pd.DataFrame()
    df = df.from_dict(details)
    df.to_pickle('place_details.pkl')


generate_place_details()

def open_or_not(place):
    query_url = url % '%20'.join(place.split(' '))
    r = requests.get(query_url)
    result = r.json()['results'][0]
    try:
        o = result['opening_hours']['open_now']
        if o:
            return 1
        else:
            return 0
    except:
        return -1
