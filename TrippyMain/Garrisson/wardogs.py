from google.cloud.firestore_v1beta1 import GeoPoint
import firebasic


class City(object):
    def __init__(self, name, lat, lng, images, helplines=None, desciption_mp3=None, desc=None):
        """
            Images : List of 5 image URLs. 1st = Main
        """
        default_helplines = {
            'police': 100,
            'fire': 100,
            'ambulance': 100,
            'tourism': 100,
        }

        default_desc = """
         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam at mi interdum, porttitor magna vel, commodo metus. Duis mauris augue, volutpat id lacinia tempor, tristique sed tellus. Nam non cursus justo. Praesent magna dolor, semper ut ipsum cursus, faucibus aliquam augue. Cras pulvinar tortor in efficitur aliquam. Nulla facilisi. Fusce sed neque vel sem interdum interdum. Curabitur euismod sit amet libero eu consequat. In mollis vehicula gravida. Maecenas et ante et turpis lacinia egestas id a neque. Nullam condimentum quis diam at ultrices. Donec et est non magna interdum condimentum. Maecenas nec metus nec nisi malesuada mattis. Vestibulum ornare lectus in sapien ornare, vitae consectetur leo egestas. Pellentesque consectetur neque sapien, vel ultricies nisl auctor vitae.
        """

        default_link = 'https://vocaroo.com/i/s1H8pXQTTID2'
        self.name = name
        self.lat = lat
        self.lng = lng
        self.images = images
        self.helplines = helplines if helplines is not None else default_helplines
        self.desc_mp3 = desciption_mp3 if desciption_mp3 is not None else default_desc
        self.desc = desc if desc is not None else default_desc

    def from_dict(source):
        pass

    def loc_object(self, lat, lng):
        return GeoPoint(latitude=lat, longitude=lng)

    def to_dict(self):
        return {
            'loc': self.loc_object(self.lat, self.lng),
            'imgurl_main': self.images[0],
            'imgurls': self.images[1:],
            'name': self.name,
            'helpline': self.helplines,
            'desc_mp3': unicode(self.desc_mp3),
            'desc': unicode(self.desc)
        }
        # ...

    def fire(self):
        city_dict = self.to_dict()
        city_id = self.name[:3]
        city_col = firebasic.get_col(firebasic.CITY_COLLECTION)
        firebasic.add_record(city_col, city_id, city_dict)
