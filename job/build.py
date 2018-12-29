from job import tagging_paths

content_identifiers = {
    'Image URL',
    'Page Title',
    'Page Subhead (30-60 characters )',
    'Intro Copy (No character limit)',
    'Main Image URL',
    'Bottom Left Image URL',
    'Bottom Right Image URL',
    'Bottom Center Image URL',
    'Card Title (60-80 characters)',
    'Card Subhead (30-60 characters)',
    'Card Body Copy (144-160 characters)',
    'Card Button Copy (XX characters)',
    'What Page Should Button Link To? (URL or descriptive text)',
    'Card Image URL',
}


# Add tp.marsha and tp.room_pool_code

class Build:
    def __init__(self, sheet_title, marsha):
        self.tp = tagging_paths.TaggingPaths(sheet_title, marsha)
        self.sheet_title = sheet_title.replace(' ', '')
        self._marsha = marsha

        if self.tp._room_pool_code is not None:
            self.base_tags = [self.tp.room_pool_code, self.tp.marsha]
        elif self.tp._product_id is not None:
            self.base_tags = [self.tp.product_id, self.tp.marsha]
        else:
            self.base_tags = [self.tp.marsha]

    def singleHeroImage(self):
        return [
            {
                'type': 'wrapper',
                'name': self._marsha+'_'+self.sheet_title+'_singleHeroImage',
                'tags': [self.tp.singleHeroImage] + self.base_tags,
                'ref': [
                    'Image URL',
                ],
            },
        ]

    def titleSubtitleText(self):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_titleSubtitleText',
                'tags': [self.tp.titleSubtitleText] + self.base_tags,
                'title': 'Page Subhead (30-60 characters )',
                'body': 'Intro Copy (No character limit)',
            },
        ]

    def imageClusterHeadingTextCta(self, tile):
        return [
            {
                'type': 'wrapper',
                'name': self._marsha+'_'+self.sheet_title+'_imageClusterHeadingTextCta_'+tile.replace(' ', ''),
                'tags': [self.tp.imageClusterHeadingTextCta(tile)] + self.base_tags,
                'ref': [
                    'Main Image URL',
                    'Bottom Left Image URL',
                    'Bottom Center Image URL',
                    'Bottom Right Image URL',
                ],
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_imageClusterHeadingTextCta_'+tile.replace(' ', '')+'_Article_Header',
                'tags': [self.tp.imageClusterHeadingTextCta(tile), self.tp.Header] + self.base_tags,
                'title': 'Card Title (60-80 characters)',
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_imageClusterHeadingTextCta_'+tile.replace(' ', '')+'_Article_Body',
                'tags': [self.tp.imageClusterHeadingTextCta(tile), self.tp.Body] + self.base_tags,
                'title': 'Card Subhead (30-60 characters)',
                'body': 'Card Body Copy (144-160 characters)',
            },
        ]

    def imageHeaderTextCtaAdvanced(self, tile):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_imageHeaderTextCtaAdvanced_'+tile.replace(' ', '')+'_Article',
                'title': 'Card Title (60-80 characters)',
                'body': 'Card Body Copy (144-160 characters)'
            },
            {
                'type': 'wrapper',
                'name': self._marsha+'_'+self.sheet_title+'_imageHeaderTextCtaAdvanced_'+tile.replace(' ', ''),
                'tags': [self.tp.imageHeaderTextCtaAdvanced(tile)] + self.base_tags,
                'ref': [
                    'Main Image URL',
                    self._marsha+'_'+self.sheet_title+'_imageHeaderTextCtaAdvanced_'+tile.replace(' ', '')+'_Article',
                ],

            },
        ]

    def imageTextCarousel(self, tile, instance):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_imageTextCarousel_'+tile.replace(' ', '')+'_'+instance+'_Article',
                'title': 'Card Title (60-80 characters)',
                'body': 'Card Body Copy (144-160 characters)'
            },
            {
                'type': 'wrapper',
                'name': self._marsha+'_'+self.sheet_title+'_imageTextCarousel_'+tile.replace(' ', '')+'_'+instance,
                'tags': [self.tp.imageTextCarousel(tile), self.tp.instance(instance)] + self.base_tags,
                'ref': [
                    'Card Image URL',
                    self._marsha+'_'+self.sheet_title+'_imageTextCarousel_'+tile.replace(' ', '')+'_'+instance+'_Article',
                ],
            },
        ]

    def roomLongDescription(self):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'roomLongDescription',
                'tags': [self.tp.roomLongDescription] + self.base_tags,
                'body': 'Intro Copy (No character limit)',
            },
        ]

    def headingTextListOfArticles(self):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_headingTextList_Article01_Header',
                'tags': [self.tp.headingTextListOfArticles, self.tp.Header] + self.base_tags,
                'title': 'Section Header (60-80 characters)',
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_headingTextList_Article02',
                'title': 'Subsection 1 Header (30-60 characters)',
                'body': 'Subsection 1 Body - Bullets or Paragraph (No character limit)',
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_headingTextList_Article03',
                'title': 'Subsection 2 Header (30-60 characters)',
                'body': 'Subsection 2 Body - Bullets or Paragraph (No character limit)',
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_headingTextList_Article04',
                'title': 'Subsection 3 Header (30-60 characters)',
                'body': 'Subsection 3 Body - Bullets or Paragraph (No character limit)',
            },
            {
                'type': 'wrapper',
                'name': self._marsha+'_'+self.sheet_title+'_headingTextList',
                'tags': [self.tp.headingTextListOfArticles] + self.base_tags,
                'ref': [
                    self._marsha+'_'+self.sheet_title+'_headingTextList_Article02',
                    self._marsha+'_'+self.sheet_title+'_headingTextList_Article03',
                    self._marsha+'_'+self.sheet_title+'_headingTextList_Article04',
                ],
            },
        ]

    def headerTextCta(self):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_headerTextCta_article',
                'tags': [self.tp.headerTextCta] + self.base_tags,
                'title': 'Card Title (60-80 characters)',
                'body': 'Card Body Copy (144-160 characters)',
            },
        ]
    # May need method overloading in Build, version without tile argument
    def imageMosaicHeadingTextCta(self, tile):
        return [
            {
                'type': 'wrapper',
                'name': self._marsha+'_'+self.sheet_title+'_imageMosaicHeadingTextCta',
                'tags': [self.tp.imageMosaicHeadingTextCta(tile)] + self.base_tags,
                'ref': [
                    'Main Image URL',
                    'Bottom Left Image URL',
                    'Bottom Right Image URL',
                ],
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_imageMosaicHeadingTextCta_Article_Header',
                'tags': [self.tp.imageMosaicHeadingTextCta(tile), self.tp.Header] + self.base_tags,
                'title': 'Card Title (60-80 characters)',
            },
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_imageMosaicHeadingTextCta_Article_Body',
                'tags': [self.tp.imageMosaicHeadingTextCta(tile), self.tp.Body] + self.base_tags,
                'title': 'Card Subhead (30-60 characters)',
                'body': 'Card Body Copy (144-160 characters)',
            },

        ]

    def restaurantOverview(self):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_restaurantOverview',
                'tags': [self.tp.restaurantOverview] + self.base_tags,
                'body': 'Intro Copy (No character limit)',
            },
        ]

    def heroImageHeaderTextCta(self, tile):
        return [
            {
                'type': 'article',
                'name': self._marsha+'_'+self.sheet_title+'_heroImageHeaderTextCta_'+tile.replace(' ', ''),
                'tags': [self.tp.heroImageHeaderTextCta(tile)] + self.base_tags,
                'title': 'Tile Title (60-80 characters)',
                'body': 'Tile Body Copy (144-160 characters )',
            },
            # {
            #     'type': 'image',
            #     'tags': [self.tp.heroImageHeaderTextCta(tile)] + self.base_tags,
            #     'image': 'Image URL',
            # },
        ]




# Will later reference articles / images by matching name to vcmid
# name: 'VCM9302834290483ID'

# Links to be handled in the fuuuture
