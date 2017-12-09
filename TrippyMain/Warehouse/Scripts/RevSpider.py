from RevScraper import primary_crawler, save_reviews
import pandas as pd
import json

with open('RevPlacesList.json', 'r') as placesfile:
    content = placesfile.read()
    plist = json.loads(content)


def save_links(plist):
    from RevSearch import getTAurl
    place_links = {}
    for city in plist['places']:
        link = getTAurl(city)
        links = [link,
                 link.replace('-Activities-', '-Activities-oa30-'),
                 link.replace('-Activities-', '-Activities-oa60-'), ]
        place_links[city] = links

    with open('RevPlacesList.json', 'w') as placesfile:
        content = {'places': place_links}
        json.dump(content, placesfile)


for city in plist['places']:
    print '========================\n' + city.upper()
    links = plist['places'][city]
    for i in range(3):
        primary_crawler(links[i])
        pickle_path = '../Reviews/' + city + '_reviews_' + str(i) + '.pkl'
        save_reviews(pickle_path)

    df = []
    for i in range(3):
        pickle_path = '../Reviews/' + city + '_reviews_' + str(i) + '.pkl'
        df[i] = pd.read_pickle(pickle_path)

    df_all = pd.concat(df)
    df_all.to_pickle('../Reviews/' + city + 'RevFin.pkl')
