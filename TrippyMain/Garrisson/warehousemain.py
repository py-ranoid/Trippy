from Warehouse.Scripts.deets import generate_place_details
from Warehouse.Scripts.graphgen import mutualGen
from Warehouse.Scripts.normalizedata import normalize
from Warehouse.Scripts.bing_image import BingWebSearch
from Warehouse.Scripts.AudioRektnika import withPickle, withText

from wardogs import City, Attraction

import pandas as pd

def pusher(data):
    images = BingWebSearch(search = data["CityName"])
    desc = data["Description"]

    helplines = dict()
    helplines['police'] = data["HelplinePolice"]
    helplines['fire'] = data["HelplineFire"]
    helplines['ambulance'] = data["HelplineAmbulance"]
    helplines['tourism'] = data["HelplineTourism"]

    (en, enurl, hin, hinurl, spa, spaurl) = withText(desc, city + "Desc")

    city = City(name = data["CityName"], helplines = helplines, lat = data["Latitude"], lng = data["Longitude"], images = images)
    city.fire()

def addCity(city="Chennai"):
    cities = pd.read_excel("Cities.xlsx")
    cities = cities.set_index("CityCode")
    cities = cities[pd.notnull(cities.index)]
    cities = cities.set_index("CityName")

    data = cities.loc[city]

    pusher(data)

    '''
    mutualGen(city)
    generate_place_details(city)
    normalize(city)    This script requires attraction descriptions
    withPickle(city)    This script requires attraction descriptions
    '''

def addAllCities():
    cities = pd.read_excel("Cities.xlsx")
    cities = cities.set_index("CityCode")
    cities = cities[pd.notnull(cities.index)]

    for i in cities.index:
        print "LOG: Adding city:", data["CityName"]
        data = cities.loc[i]

        pusher(data)
        
        '''
        mutualGen(city)
        generate_place_details(city)
        normalize(city)    This script requires attraction descriptions
        withPickle(city)    This script requires attraction descriptions
        '''
