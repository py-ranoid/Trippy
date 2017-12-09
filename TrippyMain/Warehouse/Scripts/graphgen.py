import pandas as pd
import os

# Generating the mutual visits between people using the scraped data.

def mutualGen(place):
    df_all = pd.read_pickle("../Reviews/" + place + "_RevFin.pkl")

    # Generating the graph of attractions within Udaipur city.
    len(df_all['Venue_title'].unique())

    places_list = df_all['Venue_title'].unique()

    graph = {}
    for i in places_list:
        print i
        graph[i] = {}
        for j in places_list:
            num = len(set(df_all[df_all['Venue_title'] == i]['User_name']).intersection(
                set(df_all[df_all['Venue_title'] == j]['User_name'])))
            graph[i][j] = num

    df = pd.DataFrame()
    df = df.from_dict(graph)

    os.mkdir("../BasicCityData/" + place)
    df.to_pickle("../BasicCityData/" + place + "/mutual_visits.pkl")
