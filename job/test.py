class Content:
    def __init__(self, tile=''):
        self.tile = tile
        self.content = {
            'skittle_backlink': { 'regex': r'_backToParentLink', 'tag': 'textLink' },
            'skittle_meta': { 'regex': r'_meta', 'tag': 'HotelOverview' },
            'skittle_hero': { 'regex': r'_singleHeroImage', 'tag': 'singleHeroImage' },
            'skittle_B': { 'regex': r'_HotelOverview', 'tag': 'HotelOverview' },
            'skittle_C': { 'regex': r'_headingTextListOfArticles', 'tag': self.tile },
            'skittle_D': { 'regex': r'_imageHeaderTextCtaAdvanced', 'tag': self.tile },
            'skittle_E': { 'regex': r'_imageHeaderTextCta(?!Advanced)', 'tag': self.tile },
            'header_C': { 'regex': r'_headingTextListOfArticles_TITLE[A-Z]', 'tag': 'Header' },
            'header_E': { 'regex': r'_imageHeaderTextCta_TITLE[A-Z]', 'tag': 'Header' },
        }
        self.wrapper_tile = r'_(Tile|Type)[A-Z]'
        self.article = r'_Article[0-9]{1,2}'
