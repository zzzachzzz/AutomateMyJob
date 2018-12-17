from typing import Tuple


"""
If passing page_type_locator containing only one string in the tuple,
pass parameter as such: tp = TaggingPaths(('string', ), 'marsha')
"""
class TaggingPaths:
    def __init__(self, page_type_locator: Tuple[str], marsha: str,
                 tile='', instance='', room_pool_code='', product_id=''):
        self._marsha = marsha
        self._tile = tile
        self._instance = instance
        self._room_pool_code = room_pool_code
        self._product_id = product_id

        self.Header = ['Text Length', 'MultiArticle', 'Header']
        self.Body = ['Text Length', 'MultiArticle', 'Body']
        self.Modal = ['Hotel Websites Placement', 'Link', 'Modal']

        self.singleHeroImage = ['HWS Tier 3', *page_type_locator,
                                'singleHeroImage']
        self.heroTextOverlay = ['HWS Tier 3', *page_type_locator,
                                'heroTextOverlay']
        self.titleSubtitleText = ['HWS Tier 3', *page_type_locator,
                                  'titleSubtitleText']
        self.heroTitleLongDescriptionCta = ['HWS Tier 3', *page_type_locator,
                                            'heroTitleLongDescriptionCta']

        self.roomLongDescription = ['HWS Tier 3', *page_type_locator,
                                    'roomLongDescription']
        self.headingTextListOfArticles = ['HWS Tier 3', *page_type_locator,
                                          'headingTextListOfArticles']
        self.headerTextCta = ['HWS Tier 3', *page_type_locator,
                              'headerTextCta']
        self.titleImage = ['HWS Tier 3', *page_type_locator, 'titleImage']

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

    # TODO Needs work
    # Delegate product ID matching to a function in job.py
    @property
    def product_id(self):
        # page_type_locator would unpack something like:
        # ('Products Dining', ) or ('Products Spa', )
        return [*page_type_locator, self._marsha[0],
                self._marsha, self._product_id]

    @property
    def heroImageHeaderTextCta(self):
        return ['HWS Tier 3', *page_type_locator,
                'heroImageHeaderTextCta', self._tile]

    @property
    def imageClusterHeadingTextCta(self):
        return ['HWS Tier 3', *page_type_locator,
                'imageClusterHeadingTextCta', self._tile]

    @property
    def imageTextCarousel(self):
        return ['HWS Tier 3', *page_type_locator,
                'imageTextCarousel', self._tile]

    @property
    def imageHeaderTextCtaAdvanced(self):
        return ['HWS Tier 3', *page_type_locator,
                'imageHeaderTextCtaAdvanced', self._tile]
    
    @property
    def dividerImageText(self):
        return ['HWS Tier 3', *page_type_locator,
                'dividerImageText', self._tile]
    
    @property
    def imageMosaicHeadingTextCta(self):
        return ['HWS Tier 3', *page_type_locator,
                'imageMosaicHeadingTextCta', self._tile]

    # Possibly need different tag for Layout B
    # 'imageTextCtaCarouselDining'
    @property
    def imageTextCtaCarousel(self):
        return ['HWS Tier 3', *page_type_locator,
                'imageTextCtaCarousel', self._tile]

    @property
    def mapWhatsNearby(self):
        return ['HWS Tier 3', *page_type_locator, 'mapWhatsNearby']

    @property
    def video(self):
        return ['HWS Tier 3', *page_type_locator, 'video', self._tile]
