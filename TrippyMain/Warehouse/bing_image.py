import json
import requests
from pprint import pprint
Key1 = "82ff9ab8a7614161b2bba97dfbbce3f5"
Key2 = "f94ad171570449278a28c720c9c76235"

subscriptionKey = Key1
endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

def BingWebSearch(search, lim=5):
    if not len(subscriptionKey) == 32:
        print("Invalid Bing Search API subscription key!")
        print("Please paste yours into the source code.")
        return
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    query = "%20".join(search.split(" "))
    url = endpoint + "?q=" + query + "&size=medium"
    r = requests.get(url, headers=headers)
    x = r.json()
    image_links = []
    for i in range(lim):
        image_links.append(x['value'][i]['contentUrl'])
    return image_links

# Testing
#print BingWebSearch("City Palace of Palace")
