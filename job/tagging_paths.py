from typing import Tuple
import json
# from collections import OrderedDict


PageTypeLocators = {
    'Landing Page A' ('Landing Page', 'A'),
    'Landing Page B': ('Landing Page', 'B'),
    'Hotel Overview': ('Overview', ),
    'Map & Directions': ('Overview', 'Map & Directions'),
    'Rooms & Suites Overview': ('Rooms & Suites', ),
    'Room Details': ('Rooms & Suites', 'Room Details'),
    'Dining Overview': ('Dining', ),
    'Dining Details': ('Dining Details', ),
    'Spa & Fitness Overview': ('Spa and Fitness', ),
    'Spa Details': ('Spa and Fitness', 'Spa Details'),
    'Fitness Details': ('Spa and Fitness', 'Fitness Details'),
    'Area & Activities': ('Area & Activities', ),
    'Golf Overview': ('Golf Club Overview', ),
    'Golf Details': ('Golf Details', ),
    'Meetings': ('Meetings & Events', ),
    'Weddings': ('Weddings & Occasions', ),
    'Group Bookings': ('Group Bookings', ),
    'Offers': ('Offers', ),
    'Generic Subpage': ('', ),  #TODO
    'Generic Primary': ('', ),  #TODO
}

ProductLocators = {
    'Dining Details': 'Products Dining',
    'Spa Details': 'Products Spa',
    'Fitness Details': 'Products Fitness',
    'Golf Details': 'Products Golf Courses',
}


def get_room_pool_code(sheet_title: str) -> str:
    with open('product_ids_and_rpcs.json', 'r') as file:
        data = json.load(file)

    return data['room_pool_codes'][sheet_title]


def get_product_id(page_type: str, sheet_title: str) -> str:
    with open('product_ids_and_rpcs.json', 'r') as file:
        data = json.load(file)

    return data['product_ids'][page_type][sheet_title]


def get_page_type() -> str:
    with open('product_ids_and_rpcs.json', 'r') as file:
        data = json.load(file)

    if data['room_pool_codes'].get(sheet_title) is not None:
        return 'Room Details'

    if data['product_ids']['Dining Details'].get(sheet_title) is not None:
        return 'Dining Details'

    if data['product_ids']['Spa Details'].get(sheet_title) is not None:
        return 'Spa Details'

    if data['product_ids']['Fitness Details'].get(sheet_title) is not None:
        return 'Fitness Details'

    if data['product_ids']['Golf Details'].get(sheet_title) is not None:
        return 'Golf Details'
    return None


"""
If passing page_type_locator containing only one string in the tuple,
pass parameter as such: tp = TaggingPaths(('string', ), 'marsha')
"""
class TaggingPaths:
    def __init__(self, sheet_title: str, marsha: str,
                 tile='', instance=''):
        if PageTypeLocators.get(sheet_title) is None:
            self._page_type = get_page_type(sheet_title)
            if page_type == 'Room Details':
                self._room_pool_code = get_room_pool_code(sheet_title)
            else:
                self._product_id = get_product_id(sheet_title)
        else:
            self._page_type = sheet_title

        self._page_type_locator = PageTypeLocators[self._page_type]

        self._marsha = marsha
        self._tile = tile
        self._instance = instance

        self.Header = ['Text Length', 'MultiArticle', 'Header']
        self.Body = ['Text Length', 'MultiArticle', 'Body']
        self.Modal = ['Hotel Websites Placement', 'Link', 'Modal']

        self.singleHeroImage = ['HWS Tier 3', *self._page_type_locator,
                                'singleHeroImage']
        self.heroTextOverlay = ['HWS Tier 3', *self._page_type_locator,
                                'herotextOverlay']  # They didn't camelcase it
        self.heroTitleLongDescriptionCta = ['HWS Tier 3', *self._page_type_locator,
                                            'heroTitleLongDescriptionCta']
        self.titleSubtitleText = ['HWS Tier 3', *self._page_type_locator,
                                  'titleSubtitleText']
        self.headingTextListOfArticles = ['HWS Tier 3', *self._page_type_locator,
                                          'headingTextListOfArticles']
        self.headerTextCta = ['HWS Tier 3', *self._page_type_locator,
                              'headerTextCta']
        self.titleImage = ['HWS Tier 3', *self._page_type_locator, 'titleImage']

        # self._page_type_locator is probably only ever ('Dining Details', )
        self.restaurantOverview = ['HWS Tier 3', *self._page_type_locator,
                                   'restaurantOverview']
        # self._page_type_locator is probably only
        # ever ('Rooms & Suites', 'Room Details')
        self.roomLongDescription = ['HWS Tier 3', *self._page_type_locator,
                                    'roomLongDescription']
        # self._page_type_locator is probably only
        # ever ('Spa and Fitness', 'Fitness Details')
        self.fitnessOverview = ['HWS Tier 3', *self._page_type_locator,
                                'fitnessOverview']
        # self._page_type_locator is probably only
        # ever ('Spa and Fitness', 'Spa Details')
        self.spaOverview = ['HWS Tier 3', *self._page_type_locator,
                            'spaOverview']
        # self._page_type_locator is probably only ever (Golf Details', )
        self.golfOverview = ['HWS Tier 3', *self._page_type_locator,
                             'golfOverview']

    @property
    def marsha(self):
        return ['MARSHA Codes', self._marsha[0], self._marsha]

    @property
    def instance(self):
        return ['Instance', self._instance]

    @property
    def room_pool_code(self):
        return ['Property Information', 'Room Codes',
                'Room Pool Codes', self._room_pool_code]

    # Delegate product ID matching to a function in job.py
    @property
    def product_id(self):
        # ProductLocators.get(self._page_type) gets string like
        # 'Products Dining' or 'Products Spa'.
        return [ProductLocators.get(self._page_type), self._marsha[0],
                self._marsha, self._product_id]

    @property
    def heroImageHeaderTextCta(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'heroImageHeaderTextCta', self._tile]

    @property
    def imageClusterHeadingTextCta(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageClusterHeadingTextCta', self._tile]

    @property
    def imageHeaderTextCtaAdvanced(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageHeaderTextCtaAdvanced', self._tile]
    
    @property
    def dividerImageText(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'dividerImageText', self._tile]
    
    @property
    def imageMosaicHeadingTextCta(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageMosaicHeadingTextCta', self._tile]

    @property
    def imageTextCarousel(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageTextCarousel', self._tile]

    @property
    def imageTextCtaCarousel(self):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageTextCtaCarousel', self._tile]

    @property
    def imageTextCtaCarouselDining(self):    
        return ['HWS Tier 3', *self._page_type_locator,
                'imageTextCtaCarouselDining', self._tile]

    @property
    def mapWhatsNearby(self):
        return ['HWS Tier 3', *self._page_type_locator, 'mapWhatsNearby']

    @property
    def video(self):
        return ['HWS Tier 3', *self._page_type_locator, 'video', self._tile]
