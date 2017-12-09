from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
import pandas as pd

finlist = None
num = 0

def get_place_details(primeurl):
    global finlist, num
    s = soup(urlopen(primeurl).read(), "lxml")
    try:
        pages = int(s.select('.pageNumbers > .last')[0].text)
    except:
        return False
    title = s.select('.heading_title')[0].text
    category = s.select('.attraction_details')[0].text
    return pages, title, category


def container_parser(rev, venue):
    # print i.select('.memberBadgingNoText > span')
    global finlist, num
    user_name = rev.select('.username')[0].text
    member_badge = rev.select('.memberBadgingNoText > span')
    user_rev_count = int(member_badge[1].text)
    try:
        user_approval = int(member_badge[3].text)
    except:
        user_approval = -1

    date = pd.Timestamp(rev.select('.ratingDate')[0].attrs['title'])
    rating = float(rev.select('.rating span')[0].attrs['class'][1][-2:]) / 10
    title = unicode(rev.select('span.noQuotes')[0].text)
    text = unicode(rev.select('div.entry')[0].text)
    finlist.loc[num] = [rating, title, text, date,
                        venue['title'], venue['category'],
                        user_name, user_approval, user_rev_count]
    num += 1


def review_site_parser(url, lim, venue):
    global finlist, num
    s = soup(urlopen(url).read(), "lxml")
    try:
        year = int(s.select('.review-container .ratingDate')
                   [0].attrs['title'].split(" ")[-1])
    except:
        print "year problem :", url
        year = 2017
    print url, year
    if (year < 2013 and lim > 20) or (year < 2011 and lim <= 20):
        return
    for i in s.select('.review-container'):
        container_parser(i, venue)


def primary_crawler(placelist_url):
    global finlist, num
    finlist = pd.DataFrame(columns=('Rating', 'Title', 'Text', 'Date',
                                    'Venue_title', 'Venue_category',
                                    'User_name', 'User_approval',
                                    'User_review_count'))
    num = 0
    mains = soup(urlopen(placelist_url).read(), "lxml")
    baseurl = 'https://www.tripadvisor.in'
    for i in mains.select('.listing_title > a'):
        place_link = i.attrs['href']
        venue = {}
        primeurl = baseurl + place_link.replace('Reviews', 'Reviews-or10')
        template = baseurl + place_link.replace('Reviews', 'Reviews-orXYXZX')
        print primeurl
        ratings = []
        place_details = get_place_details(primeurl)
        if place_details == False:
            # Not a place
            continue
        else:
            lim, venue_title, venue_category = place_details
            venue['title'] = venue_title
            venue['category'] = venue_category

        if lim < 10:
            # Skip place if it has less than 10*10 reviews
            continue

        for x in range(10, lim * 10, 10):
            rev_url = template.replace('XYXZX', str(x))
            review_site_parser(rev_url, lim, venue)


def save_reviews(fname):
    global finlist, num
    if fname.endswith('.csv'):
        finlist.to_csv(fname)
    elif fname.endswith('.pkl'):
        finlist.to_pickle(fname)
    else:
        print "Filename must be CSV or Pickle"
        finlist.to_csv("reviews.csv")
