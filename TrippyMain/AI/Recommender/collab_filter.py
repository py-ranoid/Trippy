import pandas as pd
from scipy.spatial.distance import cosine

data = pd.read_pickle('rating_table.pkl')
data.head()
user_list = data.index
place_list = data.columns

# Dataframe listing item vs. item similarity (Item-based similarity)
data_ibs = pd.DataFrame(index=place_list, columns=place_list)

# Fill empty spaces with cosine similarities
for i in range(0, len(data_ibs.columns)):
    for j in range(0, len(data_ibs.columns)):
        print i, j, 1 - cosine(data.ix[:, i], data.ix[:, j])
        data_ibs[place_list[i]][place_list[j]] = 1 - \
            cosine(data.ix[:, i], data.ix[:, j])

data_ibs.to_pickle('ibs_graph.pkl')

# Create a placeholder items for closest neighbours to an item
# (Sorting recommendations on ascending orders of probability)
data_neighbours = pd.DataFrame(index=data_ibs.columns, columns=[range(1, 11)])

# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(len(data_ibs.columns)):
    probs = data_ibs.ix[0:, place_list[i]]
    sorted_probs = probs.sort_values(ascending=False)
    data_neighbours.ix[place_list[i], :10] = sorted_probs[:10].index
