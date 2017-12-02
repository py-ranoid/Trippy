# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import JsonResponse

import json
import pandas as pd
import os

# Create your views here.

BASE = os.path.dirname(os.path.abspath(__file__))

def forAttraction(request):
    body = json.loads(request.body)
    print body
    lat = body.get('lat', None)
    lng = body.get('lng', None)
    lang = body.get('lang', None)
    print lat, lng, lang

    #logic to determine the city belongs here.
    ATTR = "CityPalace"
    uri1=BASE + "/data/sa" + ATTR + ".pkl"

    print str(lang.lower()).strip(), 'spanish'
    print str(lang.lower()).strip(), 'hindi'

    if str(lang.lower()).strip() == 'spanish':
        print 'here1'
        uri1=BASE + "/data/spasa" + ATTR + ".pkl"
    elif str(lang.lower()).strip() == 'hindi':
        print 'here2'
        uri1=BASE + "/data/hinsa" + ATTR + ".pkl"

    df = pd.read_pickle(uri1)
    df = df.T

    # Generating JSON data.
    ddf = df.to_dict()
    ddf2 = {}
    ddf2['resp'] = []

    for i in ddf.keys():
        ddf[i]['said'] = i
        ddf2['resp'].append(ddf[i])

    ddf2['success'] = True

    return JsonResponse(ddf2)
