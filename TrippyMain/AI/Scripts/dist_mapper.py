import requests
import pandas as pd

YOUR_API_KEY = 'AIzaSyD6N7W6sJ82Vw7a4OwZU41PI0dra6Xc2sg'
url = 'https://maps.googleapis.com/maps/api/directions/json?origin=%f,%f&destination=%f,%f&key=' + YOUR_API_KEY

df = pd.read_pickle('vis_graph.pkl')
plac_df = pd.read_pickle('place_details.pkl')

places_list = list(df.index)
DIST_MATRIX_FILE = 'dist_graph.pkl'


def generate_distance_matrix():
    graph = {}
    for i in places_list:
        graph[i] = {}
        graph[i][i] = 0
        for j in places_list:
            if j in graph:
                num = graph[j][i]
            else:
                num = get_dist(i, j)
            graph[i][j] = num
    df = pd.DataFrame()
    df = df.from_dict(graph)
    df.to_pickle(DIST_MATRIX_FILE)


if os.path.exist(DIST_MATRIX_FILE):
    df = pd.read_pickle(DIST_MATRIX_FILE)
else:
    generate_distance_matrix()


def get_dist(x, y):
    # print x, y
    xlat, xlng = plac_df[x]['lat'], plac_df[x]['lng']
    ylat, ylng = plac_df[y]['lat'], plac_df[y]['lng']
    query_url = url % (xlat, xlng, ylat, ylng)
    r = requests.get(query_url)
    result = r.json()['routes'][0]
    walking = result['legs'][0]
    distance = walking['distance']['value']
    return distance
