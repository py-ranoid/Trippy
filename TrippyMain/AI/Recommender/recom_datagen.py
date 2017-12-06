import pandas as pd

df = pd.read_pickle('TrippyMain/Warehouse/UdpRevFin.pkl')
print df.shape

rev = df[
    (df['User_approval'] > 10) & (df['User_review_count'] > 14)]
print rev.shape

rev = df.groupby('User_name').filter(lambda x: len(x) > 4)
rev.shape

subdf = rev[['User_name', 'Rating', 'Venue_title']]
print subdf.shape


place_list = list(subdf['Venue_title'].unique())
user_list = list(subdf['User_name'].unique())
print place_list

rev_dict = {}
for x, i in subdf.iterrows():
    name = i['User_name']
    place = i['Venue_title']
    rating = i['Rating']
    if rev_dict.get(name, None) == None:
        rev_dict[name] = {}
    rev_dict[name][place] = rating

rating_tb = pd.DataFrame(index=range(len(user_list)), columns=place_list)
for i in range(0, len(user_list)):
    for j in range(0, len(place_list)):
        name = user_list[i]
        place = place_list[j]
        person_dict = rev_dict[name]
        if person_dict.get(place, None) == None:
            rating_tb.iloc[i, j] = 0
        else:
            rating_tb.iloc[i, j] = person_dict[place]

rating_tb.head()
rating_tb.to_pickle('rating_table.pkl')
