import os
import pandas as pd

CATEGORY_MATRIX_NAME = 'cat_graph.py'
fin_categories = {'Lakes': u'Bodies of Water',
                  'Parks': u'Nature & Parks',
                  'Historic Museums': u'History Museums',
                  'Museums': u'Museums',
                  'Pilgrimage Sites': u'Sacred & Religious Sites',
                  'Architectural Buildings': u'Architectural Buildings',
                  'Gardens': u'Gardens',
                  'Shopping': u'Shopping',
                  'Monuments': u'Monuments & Statues'
                  }


def save_matrix():
    df = pd.read_pickle('UdpRevFin.pkl')
    categories = df[['Venue_title', 'Venue_category']
                    ].drop_duplicates().set_index(['Venue_title'])
    finlist = pd.DataFrame(columns=('Venue_title', 'Category'))
    num = 0

    for i in categories.index:
        for j in categories.loc[i][0].strip().split(','):
            finlist.loc[num] = [i.strip(), j.strip()]
            num += 1

    finlist = finlist.set_index('Category')
    finlist = finlist[finlist.index.value_counts().between(2, 8)]
    finlist.to_pickle(CATEGORY_MATRIX_NAME)
    return finlist


def get_places(category):
    return list(finlist.loc[fin_categories[category]]['Venue_title'])


def get_category_list():
    return fin_categories.keys()


if os.path.exists(CATEGORY_MATRIX_NAME):
    finlist = pd.read_pickle(CATEGORY_MATRIX_NAME)
else:
    finlist = save_matrix()
