import dryscrape
import sys
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
#from TAscraper import primary_crawler, save_reviews
import argparse

parser = argparse.ArgumentParser(description='Argument Description')
parser.add_argument("-p", "--place", help="City/Tourist Place",
                    type=str, default='Udaipur')
args = parser.parse_args()
value = args.place


if 'linux' in sys.platform:
    dryscrape.start_xvfb()


def getTAurl(value):
    search_term = 'Trip Advisor Places to Visit in ' + value
    sess = dryscrape.Session(base_url='http://google.com')
    sess.set_attribute('auto_load_images', False)
    sess.visit('/')
    q = sess.at_xpath('//*[@name="q"]')
    q.set(search_term)
    q.form().submit()

    places_url = [link['href'] for link in sess.xpath(
        '//a[@href]') if link['href'].startswith('https://www.tripadvisor.in/Attraction')]

    if places_url:
        return places_url[0]
        # primary_crawler(places_url[0])
        # save_reviews(value + '_reviews.pkl')
    else:
        print "Prime URL not found"
