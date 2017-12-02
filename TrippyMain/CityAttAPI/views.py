# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import JsonResponse
from AI.recommender import get_recommendations

import json
import pandas as pd
import os

# Create your views here.

BASE = os.path.dirname(os.path.abspath(__file__))


def forCity(request):
    body = json.loads(request.body)
    print body
    lat = body.get('lat', None)
    lng = body.get('lng', None)
    lang = body.get('lang', None)
    recommend = body.get('flag', None)
    print lat, lng, lang

    # logic to determine the city belongs here.
    CITY = "udaipur"
    uri1 = BASE + "/data/final_" + CITY + ".pkl"
    uri2 = BASE + "/data/" + CITY + "_eng.json"

    print str(lang.lower()).strip(), 'spanish'
    print str(lang.lower()).strip(), 'hindi'

    if str(lang.lower()).strip() == 'spanish':
        print 'here1'
        uri1 = BASE + "/data/spafinal_" + CITY + ".pkl"
        uri2 = BASE + "/data/" + CITY + "_spa.json"
    elif str(lang.lower()).strip() == 'hindi':
        print 'here2'
        uri1 = BASE + "/data/hinfinal_" + CITY + ".pkl"
        uri2 = BASE + "/data/" + CITY + "_hin.json"

    df = pd.read_pickle(uri1)
    df = df.T

    about = json.loads(open(uri2, 'r').read())

    # Generating JSON data.
    rec = get_recommendations(lat=lat, lng=lng)
    ddf = df.to_dict()
    ddf2 = {}
    ddf2['resp'] = []

    print rec

    if recommend == "0":
        for i in ddf.keys():
            ddf[i]['aid'] = i
            ddf2['resp'].append(ddf[i])
    else:
        for i in rec:
            for j in ddf.values():
                if j['name'] == i:
                    ddf2['resp'].append(j)

    ddf2['success'] = True
    ddf2['about'] = about

    return JsonResponse(ddf2)
