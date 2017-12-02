import pandas as pd

df = pd.read_pickle('UdpRevFin.pkl')
places_list = df['Venue_title'].unique()

graph = {}
for i in places_list:
    graph[i] = {}
    for j in places_list:
        num = len(set(df[df['Venue_title'] == i]['User_name']).intersection(
            set(df[df['Venue_title'] == j]['User_name'])))
    graph[i][j] = num

df = pd.DataFrame()
df = df.from_dict(graph)

df.to_pickle('vis_graph.pkl')
