# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import JsonResponse

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

    #logic to determine the city belongs here.
    CITY = "udaipur"
    uri1=BASE + "/data/final_" + CITY + ".pkl"
    uri2=BASE + "/data/" + CITY + "_eng.json"

    if lang.lower == 'spanish':
        uri1=BASE + "/data/spafinal_" + CITY + ".pkl"
        uri2=BASE + "/data/" + CITY + "_spa.json"
    elif lang.lower == 'hindi':
        uri1=BASE + "/data/hinfinal_" + CITY + ".pkl"
        uri2=BASE + "/data/" + CITY + "_hin.json"

    df = pd.read_pickle(uri1)
    df = df.T

    about = json.loads(open(uri2, 'r').read())

    # Generating JSON data.
    ddf = df.to_dict()
    ddf2 = {}
    ddf2['resp'] = []

    for i in ddf.keys():
        ddf[i]['aid'] = i
        ddf2['resp'].append(ddf[i])

    ddf2['success'] = True
    ddf2['about'] = about

    return JsonResponse(ddf2)
