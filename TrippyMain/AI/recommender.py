import pandas as pd

df_ibs = pd.read_pickle('AI/ibs_graph.pkl')
df_coords = pd.read_pickle('Warehouse/place_details.pkl').loc[['lat', 'lng']]


def get_net_score(places=['Eklingji Temple', 'Jagmandir Isla', 'Lake Pichola']):
    df_sum = df_ibs[places].sum(axis=1).sort_values(
        ascending=False)[:13].to_dict()
    fin_dict = {}

    for i in df_sum:
        if i not in places:
            fin_dict[i] = df_sum[i]
    fin_dict
    return fin_dict


def get_recommendations(places=None, lat=0, lng=0):
    if places == None:
        places = get_net_score()
    else:
        places = get_net_score(places)
    df_combined = get_distances(places, lat, lng)
    coeff = 1 / df_combined.loc['Dist'].max()
    return list(((1 - (df_combined.loc['Dist'] * coeff)) * 10 + df_combined.loc['Score']).sort_values(ascending=False).index)


def get_distances(place_dict=None, lat=0, lng=0):
    if lat == 0:
        lat = df_coords['Jagdish Temple']['lat']
    if lng == 0:
        lng = df_coords['Jagdish Temple']['lng']
    if place_dict == None:
        place_dict = {u'Bagore Ki Haveli': 0.37700201051520521,
                      u'City Palace Government Museum': 0.14515397172161548,
                      u'City Palace of Udaipur': 0.58697271742497403,
                      u'Eklingji Temple': 0.3372493736153851,
                      u'Garden of the Maidens (Sahelion Ki Bari)': 0.2950766551894547,
                      u'Jagdish Temple': 0.35834493940722112,
                      u'Lake Fatehsagar Udaipur': 0.39468644755186799,
                      u'Monsoon Palace': 0.22795704484564772,
                      u'Srinathji Temple': 0.095573657039414561,
                      u'Vintage Collection of Classic Cars Museum': 0.040202336211546452}
    fin_dict = {}
    for i in place_dict:
        dist = (df_coords[i]['lat'] - lat)**2 + (df_coords[i]['lng'] - lng)**2
        fin_dict[i] = {'Score': place_dict[i],
                       'Dist': dist}
    df_combined = pd.DataFrame()
    df_combined = df_combined.from_dict(fin_dict)
    return df_combined
