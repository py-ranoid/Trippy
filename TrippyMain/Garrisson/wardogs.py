from google.cloud.firestore_v1beta1 import GeoPoint
import firebasic


class Place(object):
    """
        Images : List of 5 image URLs. 1st = Main
    """

    def __init__(self, lat, lng, name, images, desciption_mp3=None, desc=None):
        default_desc = """
         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam at mi interdum, porttitor magna vel, commodo metus. Duis mauris augue, volutpat id lacinia tempor, tristique sed tellus. Nam non cursus justo. Praesent magna dolor, semper ut ipsum cursus, faucibus aliquam augue. Cras pulvinar tortor in efficitur aliquam. Nulla facilisi. Fusce sed neque vel sem interdum interdum. Curabitur euismod sit amet libero eu consequat. In mollis vehicula gravida. Maecenas et ante et turpis lacinia egestas id a neque. Nullam condimentum quis diam at ultrices. Donec et est non magna interdum condimentum. Maecenas nec metus nec nisi malesuada mattis. Vestibulum ornare lectus in sapien ornare, vitae consectetur leo egestas. Pellentesque consectetur neque sapien, vel ultricies nisl auctor vitae.
        """
        default_link = 'https://vocaroo.com/i/s1H8pXQTTID2'
        self.name = name
        self.lat = lat
        self.lng = lng
        self.images = images
        self.desc_mp3 = desciption_mp3 if desciption_mp3 is not None else default_link
        self.desc = desc if desc is not None else default_desc

    def loc_object(self, lat, lng):
        return GeoPoint(latitude=lat, longitude=lng)

    def to_dict(self):
        return {
            'loc': self.loc_object(self.lat, self.lng),
            'imgurl_main': self.images[0],
            'imgurls': self.images[1:],
            'name': self.name,
            'desc_mp3': unicode(self.desc_mp3),
            'desc': unicode(self.desc)
        }


class City(Place):
    def __init__(self, name, lat, lng, images, helplines=None, desc_mp3=None, desc=None):
        default_helplines = {
            'police': 100,
            'fire': 100,
            'ambulance': 100,
            'tourism': 100,
        }
        super(City, self).__init__(lat, lng, name, images, desc_mp3, desc)
        self.helplines = helplines if helplines is not None else default_helplines

    def from_dict(source):
        pass

    def to_dict(self):
        basic = super(City, self).to_dict()
        basic['helpline'] = self.helplines
        return basic

    def fire(self, overwrite=False):
        city_dict = self.to_dict()
        city_id = self.name[:3]
        city_col = firebasic.get_col(firebasic.CITY_COLLECTION)
        firebasic.add_record(city_col, city_id, city_dict, overwrite)
        pth = [firebasic.CITY_COLLECTION, city_id, firebasic.ATTR_COLLECTION]
        col_path = '/'.join(pth)
        firebasic.add_collection(col_path)


class Attraction(Place):
    def __init__(self, key, name, lat, lng, images, hl, city, desc_mp3=None, desc=None, prices=None):
        default_prices = {
            'price1': 10,
            'price2': 20,
            'price3': 30,
            'price4': 40
        }
        super(Attraction, self).__init__(
            lat, lng, name, images, desc_mp3, desc)
        self.city = city
        self.attr_id = key
        self.highlights = hl
        self.prices = prices if prices is not None else default_prices

    def from_dict(source):
        pass

    def to_dict(self):
        basic = super(Attraction, self).to_dict()
        basic['attr_id'] = self.attr_id
        basic['highlights'] = self.highlights
        basic['ticket_price'] = self.prices
        return basic

    def fire(self, overwrite=False):
        attr_dict = self.to_dict()
        attr_key = self.city[:3] + "%.2d" % self.attr_id
        path = [firebasic.CITY_COLLECTION,
                self.city[:3], firebasic.ATTR_COLLECTION]
        col_path = '/'.join(path)
        attr_col = firebasic.get_col(col_path)
        firebasic.add_record(attr_col, attr_key, attr_dict, overwrite)


"""
from wardogs import City, Attraction
c = City(name=u'tr8ial',lat=2,lng=3,images = [u'na']*5)
c.fire()
a = Attraction(key = 02,name="meh",lat=2,lng=4,images=['na1']*5,hl="mehmehmeh",city='tr8ial')
a.fire()
"""
