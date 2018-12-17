your_marsha = ''
your_tile = ''
your_room_pool_code = ''


class TaggingPaths:
    def __init__(self, marsha, tile=''):
        self._marsha = marsha
        self._tile = tile

        self.Header = ['Text Length', 'MultiArticle', 'Header']
        self.Body = ['Text Length', 'MultiArticle', 'Body']
        self.Modal = ['Hotel Websites Placement', 'Link', 'Modal']

    @property
    def marsha(self):
        return ['MARSHA Codes', self._marsha[0], self._marsha]


# Accepts landing_layout 'A' or 'B'
class LandingPage(TaggingPaths):
    def __init__(self, landing_layout, marsha, tile='', instance=''):
        super().__init__(marsha, tile)
        self._landing_layout = landing_layout
        self._instance = instance

        self.heroTextOverlay = ['HWS Tier 3', 'Landing Page', self._landing_layout, 'heroTextOverlay']
        self.titleSubtitleText = ['HWS Tier 3', 'Landing Page', self._landing_layout, 'titleSubtitleText']

    @property
    def heroImageHeaderTextCta(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'heroImageHeaderTextCta', self._tile]

    @property
    def imageClusterHeadingTextCta(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'imageClusterHeadingTextCta', self._tile]

    @property
    def imageTextCarousel(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'imageTextCarousel', self._tile]

    @property
    def instance(self):
        return ['Instance', self._instance]

    @property
    def imageHeaderTextCtaAdvanced(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'imageHeaderTextCtaAdvanced', self._tile]
    
    @property
    def dividerImageText(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'dividerImageText', self._tile]
    
    @property
    def imageMosaicHeadingTextCta(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'imageMosaicHeadingTextCta', self._tile]

    # Possibly need different tag for Layout B
    # 'imageTextCtaCarouselDining'
    @property
    def imageTextCtaCarousel(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'imageTextCtaCarousel', self._tile]

    @property
    def mapWhatsNearby(self):
        return ['HWS Tier 3', 'Landing Page', self._landing_layout, 'mapWhatsNearby']
    
    
class HotelOverview(TaggingPaths):
    def __init__(self, marsha, locator, tile=''):
        super().__init__(marsha, tile)

        self.singleHeroImage = ['HWS Tier 3', *locator, 'singleHeroImage']


    
    

class RoomsAndSuites(TaggingPaths):
    def __init__(self, marsha, tile=''):
        super().__init__(marsha, tile)

        self.singleHeroImage = ['HWS Tier 3', 'Rooms & Suites', 'singleHeroImage']
        self.heroTitleLongDescriptionCta = ['HWS Tier 3', 'Rooms & Suites', 'heroTitleLongDescriptionCta']
    
    @property
    def imageMosaicHeadingTextCta(self):
        return ['HWS Tier 3', 'Rooms & Suites', 'imageMosaicHeadingTextCta', self._tile]
    
    @property
    def imageHeaderTextCtaAdvanced(self):
        return ['HWS Tier 3', 'Rooms & Suites', 'imageHeaderTextCtaAdvanced', self._tile]


class RoomDetails(RoomsAndSuites):
    def __init__(self, marsha, room_pool_code, tile=''):
        super().__init__(marsha, tile)
        self._room_pool_code = room_pool_code

        self.singleHeroImage = ['HWS Tier 3', 'Rooms & Suites', 'Room Details', 'singleHeroImage']
        self.roomLongDescription = ['HWS Tier 3', 'Rooms & Suites', 'Room Details', 'roomLongDescription']
        self.headingTextListOfArticles = ['HWS Tier 3', 'Rooms & Suites', 'Room Details', 'headingTextListOfArticles']
        self.headerTextCta = ['HWS Tier 3', 'Rooms & Suites', 'Room Details', 'headerTextCta']
        self.titleImage = ['HWS Tier 3', 'Rooms & Suites', 'Room Details', 'titleImage']

    @property
    def room_pool_code(self):
        return ['Property Information', 'Room Codes', 'Room Pool Codes', self._room_pool_code]

    @property
    def video(self):
        return ['HWS Tier 3', 'Rooms & Suites', 'Room Details', 'video', self._tile]
    
    
    