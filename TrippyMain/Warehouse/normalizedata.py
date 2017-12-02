import pandas as pd

def normalize():
    df = pd.read_pickle("place_details.pkl")
    df = df.T
    dfextra = pd.read_excel("basicdescs.xlsx")

    df['imgurls'] = dfextra['imgurls']
    df['desc'] = dfextra["   Description"]

    newind = range(1000, 1025)
    df['ind'] = newind

    df = df.set_index('ind')
    df['Name'] = df['TA_name']

    del df['Google_name']
    del df['TA_name']

    df.to_pickle("final_udaipur.pkl")

normalize()