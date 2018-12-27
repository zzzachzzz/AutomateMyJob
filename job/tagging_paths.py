from typing import Tuple
import json


PageTypeLocators = {
    'Landing Page A': ('Landing Page', 'A'),
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
    with open('job/product_ids_and_rpcs.json', 'r') as file:
        data = json.load(file)

    return data['room_pool_codes'][sheet_title]


def get_product_id(page_type: str, sheet_title: str) -> str:
    with open('job/product_ids_and_rpcs.json', 'r') as file:
        data = json.load(file)

    return data['product_ids'][page_type][sheet_title]


def get_page_type(sheet_title: str) -> str:
    if PageTypeLocators.get(sheet_title):
        return sheet_title

    with open('job/product_ids_and_rpcs.json', 'r') as file:
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
    def __init__(self, sheet_title: str, marsha: str):
        self._room_pool_code = None
        self._product_id = None
        self._page_type = get_page_type(sheet_title)
        assert self._page_type is not None

        if self._page_type == 'Room Details':
            self._room_pool_code = get_room_pool_code(sheet_title)
        elif ProductLocators.get(self._page_type):
            self._product_id = get_product_id(self._page_type, sheet_title)
        else:
            self._page_type = sheet_title

        self._page_type_locator = PageTypeLocators[self._page_type]

        self._marsha = marsha
        self.marsha = ['MARSHA Codes', marsha[0], marsha]

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
        self.mapWhatsNearby = ['HWS Tier 3', *self._page_type_locator, 'mapWhatsNearby']

        self.room_pool_code = ['Property Information', 'Room Codes',
                               'Room Pool Codes', self._room_pool_code]
        # Delegate product ID matching to a function in job.py
        # ProductLocators.get(self._page_type) gets string like
        # 'Products Dining' or 'Products Spa'.
        self.product_id = [ProductLocators.get(self._page_type),
                           self._marsha[0], self._marsha, self._product_id]

    def instance(self, instance):
        return ['Instance', instance]    

    def heroImageHeaderTextCta(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'heroImageHeaderTextCta', tile]

    def imageClusterHeadingTextCta(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageClusterHeadingTextCta', tile]

    def imageHeaderTextCtaAdvanced(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageHeaderTextCtaAdvanced', tile]
    
    def dividerImageText(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'dividerImageText', tile]
    
    def imageMosaicHeadingTextCta(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageMosaicHeadingTextCta', tile]

    def imageTextCarousel(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageTextCarousel', tile]

    def imageTextCtaCarousel(self, tile):
        return ['HWS Tier 3', *self._page_type_locator,
                'imageTextCtaCarousel', tile]

    def imageTextCtaCarouselDining(self, tile):    
        return ['HWS Tier 3', *self._page_type_locator,
                'imageTextCtaCarouselDining', tile]

    def video(self, tile):
        return ['HWS Tier 3', *self._page_type_locator, 'video', tile]
