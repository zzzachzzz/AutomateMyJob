# 'Visual Navigation ( E )': 'unknown' WHO ARE YOU
# perhaps 'imageHeaderTextCta' ?

# 'name': marsha+'_'+sheet_title+'_imageMosaicHeadingTextCta_TileA_Article_Body',

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


Build = {
    'Landing Page B': {
        'Hero Image/Video': {
            'type': 'heroTextOverlay'
        },
        'Narrative Element 1 - Overlay Interstitial': {
            'type': 'dividerImageText',
            'tile': 'Tile A',
        },
        'Narrative Element 1 - Content Image Cluster': {
            'type': 'imageMosaicHeadingTextCta',
            'tile': {
                'Content Image Cluster Tile 1': 'Tile A',
                'Content Image Cluster Tile 2': 'Tile B',
                'Content Image Cluster Tile 3': 'Tile C',
            },
        },
        'Narrative Element 2 - Overlay Interstitial': {
            'type': 'dividerImageText',
            'tile': 'Tile B',
        },
        'Narrative Element 2 - Primary Feature List': {
            'type': 'imageClusterHeadingTextCta',
            'tile': {
                'Primary Feature Card 1': 'Tile A',
                'Primary Feature Card 2': 'Tile B',
                'Primary Feature Card 3': 'Tile C',
            },
        },
        'Narrative Element 3 - Overlay Interstitial': {
            'type': 'dividerImageText', 'tile': 'Tile C'
        },
        'Narrative Element 3 - Content Image Cluster': {
            'type': 'imageMosaicHeadingTextCta',
            'tile': {
                'Content Image Cluster Tile 1': 'Tile A',
                'Content Image Cluster Tile 2': 'Tile B',
                'Content Image Cluster Tile 3': 'Tile C',
            },
        },
        'Narrative Element 4 - Vertical Interstitial (No Photo)': {
            'type': 'heroImageHeaderTextCta', 'tile': 'Tile A',
        },
        'Narrative Element 4 - Featured Carousel': {
            'type': 'imageTextCarousel',
            'tile': 'Tile A',
            'instance': {
                'Featured Carousel Card 1': '01',
                'Featured Carousel Card 2': '02',
                'Featured Carousel Card 3': '03',
                'Featured Carousel Card 4': '04',
                'Featured Carousel Card 5': '05',
                'Featured Carousel Card 6': '06',
            },
        },
        'Destination Overview - Vertical Interstitial': {
            'type': 'heroImageHeaderTextCta',
            'tile': 'Tile B',
        },
        'Attractions Map Listings': {
            'type': None
        },
        'Narrative Element 5 - Narrative Element Title (60-80 characters)': {
            'type': 'titleSubtitleText'
        },
        'Primary Feature Card': {
            'type': 'imageClusterHeadingTextCta',
            'tile': 'Tile D',
        },
        'Narrative Element 5 - Messaging Carousel': {
            'type': 'imageTextCarousel'
        },
        'Narrative Element 1 - Secondary Feature List': {
            'type': 'imageHeaderTextCtaAdvanced'
        },
    },
    'Hotel Overview': {
        'Hero Image': {
            'type': 'wrapper',
            'tags': ['singleHeroImage'],
            'ref': ['Image URL'],
        },
        'Intro (A)': {
            'type': 'article',
            'tags': ['titleSubtitleText'],
            'ref': [
                'Page Subhead (30-60 characters )',
                'Intro Copy (No character limit)',
            ],
        },
        'Primary Feature List (B)': {
            'Primary Feature Card 1 (B)': [
                {
                    'type': 'wrapper',
                    'tags': ['imageClusterHeadingTextCta'],
                    'ref': [
                        'Main Image URL',
                        'Bottom Left Image URL',
                        'Bottom Center Image URL',
                        'Bottom Right Image URL',
                    ],
                },
                {
                    'type': 'article',
                    'tags': [
                        'imageClusterHeadingTextCta',
                        'Header',
                    ],
                    'ref': [
                        'Card Title (60-80 characters)',
                    ],
                },
                {
                    'type': 'article',
                    'tags': [
                        'imageClusterHeadingTextCta',
                        'Body',
                    ],
                    'ref': [
                        'Card Subhead (30-60 characters)',
                        'Card Body Copy (144-160 characters)',
                    ],
                },
            ],
            'Primary Feature Card 2 (B)': {

            },
            
        },
        'Secondary Feature List ( C )': {
            'type': 'imageHeaderTextCtaAdvanced'
        },
        'Messaging Carousel (D)': {
            'type': 'imageTextCarousel'
        }
    }
}


TILE_imageClusterHeadingTextCta = {
    'Primary Feature Card 1 (B)': 'Tile A',
    'Primary Feature Card 2 (B)': 'Tile B',
}

TILE_imageHeaderTextCtaAdvanced = {
    'Secondary Feature Card 1': 'Tile A',
    'Secondary Feature Card 2': 'Tile B',
}

TILE_imageTextCarousel = {
    'Messaging Carousel Card 1': '01',
    'Messaging Carousel Card 2': '02',
}

TILE_unkown = {
    'Visual Navigation Card 1': 'Tile A',
    'Visual Navigation Card 2': 'Tile B',
}

pre_content = {
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
    'If buttons are used, List cards will link to (select one):',
}

ignore = {
    '=LEN(D84)',  # 131, literal value in sheet
    'Overview Page'
    '(Add link to style guide)',
    'Section is required',
    'Section is Optional. If used ...',
    'Section si Pre-Populated with 4 cards; ...',
}


"""
Iterate through column D.
Upon cell matching as type such as
(Intro, Primary Feature List), complete
previous content piece and start new one.
Upon cell matching as pre-content,
get contents of next cell row if not empty,
and add to current content piece.
Perhaps create dictionary with pre-content
('Card Body Copy') as key, and content in
next row as the value.
Upon reaching several blank lines in a row,
maybe like 7, complete previous content piece
and end parsing for current sheet.
"""