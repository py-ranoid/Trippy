from Warehouse.Scripts.deets import generate_place_details
from Warehouse.Scripts.graphgen import mutualGen
from Warehouse.Scripts.normalizedata import normalize
from Warehouse.Scripts.bing_image import BingWebSearch
from Warehouse.Scripts.AudioRektnika import withPickle

from wardogs import City

import pandas as pd

def addCity(city="Chennai"):
    cities = pd.read_excel("Cities.xlsx")
    cities = cities.set_index("CityCode")
    cities = cities[pd.notnull(cities.index)]
    cities = cities.set_index("CityName")

    data = cities.loc[city]

    images = BingWebSearch(search = city)

    helplines = dict()
    helplines['police'] = data["HelplinePolice"]
    helplines['fire'] = data["HelplineFire"]
    helplines['ambulance'] = data["HelplineAmbulance"]
    helplines['tourism'] = data["HelplineTourism"]

    city = City(name = city, helplines = helplines, lat = data["Latitude"], lng = data["Longitude"], images = images)
    city.fire()

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
        data = cities.loc[i]

        images = BingWebSearch(search = data["CityName"])

        helplines = dict()
        helplines['police'] = data["HelplinePolice"]
        helplines['fire'] = data["HelplineFire"]
        helplines['ambulance'] = data["HelplineAmbulance"]
        helplines['tourism'] = data["HelplineTourism"]

        city = City(name = data["CityName"], helplines = helplines, lat = data["Latitude"], lng = data["Longitude"], images = images)
        city.fire()

        '''
        mutualGen(city)
        generate_place_details(city)
        normalize(city)    This script requires attraction descriptions
        withPickle(city)    This script requires attraction descriptions
        '''
