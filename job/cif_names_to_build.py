# Content Intake Form Names
class CIF:
    def __init__(self, b: 'Build'):
        self.names = {
            'Hero Image': lambda: b.singleHeroImageWrapper(),
            'Intro (A)': lambda: b.titleSubtitleText(),
            'Primary Feature Card 1 (B)': lambda: b.imageClusterHeadingTextCta('Tile A'),
            'Primary Feature Card 2 (B)': lambda: b.imageClusterHeadingTextCta('Tile B'),
            'Secondary Feature Card 1': lambda: b.imageHeaderTextCtaAdvanced('Tile A'),
            'Secondary Feature Card 2': lambda: b.imageHeaderTextCtaAdvanced('Tile B'),
            'Secondary Feature Card 3': lambda: b.imageHeaderTextCtaAdvanced('Tile C'),
            'Secondary Feature Card 4': lambda: b.imageHeaderTextCtaAdvanced('Tile D'),
            'Secondary Feature Card 5': lambda: b.imageHeaderTextCtaAdvanced('Tile E'),
            'Secondary Feature Card 6': lambda: b.imageHeaderTextCtaAdvanced('Tile F'),
            'Secondary Feature Card 7': lambda: b.imageHeaderTextCtaAdvanced('Tile G'),
            'Secondary Feature Card 8': lambda: b.imageHeaderTextCtaAdvanced('Tile H'),
            'Secondary Feature Card 9': lambda: b.imageHeaderTextCtaAdvanced('Tile I'),
            'Secondary Feature Card 10': lambda: b.imageHeaderTextCtaAdvanced('Tile J'),
            'Messaging Carousel Card 1':  lambda: b.imageTextCarousel('Tile A', '01'),
            'Messaging Carousel Card 2':  lambda: b.imageTextCarousel('Tile A', '02'),
            'Messaging Carousel Card 3':  lambda: b.imageTextCarousel('Tile A', '03'),
            'Marketing Message (D)': lambda: b.headerTextCta(),
            # The Vert Int names are sooo varied O_O needs revisiting
            'Vertical Interstitial': lambda: b.heroImageHeaderTextCta('Tile A'),
            # The Landing Page leads one to believe that a total of
            # 9 tiles are possible... must investigate. Should be A-F
            'Content Image Cluster Tile 1': lambda: b.imageMosaicHeadingTextCta('Tile A'),
            'Content Image Cluster Tile 2': lambda: b.imageMosaicHeadingTextCta('Tile B'),
            'Content Image Cluster Tile 3': lambda: b.imageMosaicHeadingTextCta('Tile C'),
            
        }

class RoomDetails(CIF):
    def __init__(self, b):
        super().__init__(b)
        self.names.update({
            'Intro (A)': lambda: b.roomLongDescription(),
            'Room Highlights - Editorial (B)': lambda: b.headingTextListOfArticles(),
            # Currently assuming that the tag
            # imageMosaicHeadingTextCta == imageMosaicHeadingTextCta/Tile A
            'Primary Feature Card 1': lambda: b.imageMosaicHeadingTextCta('Tile A'),
        })


class DiningDetails(CIF):
    def __init__(self, b):
        super().__init__(b)
        self.names.update({
            'Intro (A)': lambda: b.restaurantOverview()
        })


class SpaDetails(CIF):
    def __init__(self, b):
        super().__init__(b)
        self.names.update({
            'Hero Image': lambda: b.singleHeroImage(),
            'Vertical Interstitial Photo (B)': lambda: b.heroImageHeaderTextCta('Tile A'),
            'Primary Feature Card 1': lambda: b.imageMosaicHeadingTextCta('Tile A'),
            'Tertiary Content List ( E )': lambda: b.imageHeaderTextCtaTitle(),
            'Tertiary Card 1': lambda: b.imageHeaderTextCta('Tile A'),
            'Tertiary Card 2': lambda: b.imageHeaderTextCta('Tile B'),
            'Tertiary Card 3': lambda: b.imageHeaderTextCta('Tile C'),
            'Tertiary Card 4': lambda: b.imageHeaderTextCta('Tile D'),
            'Tertiary Card 5': lambda: b.imageHeaderTextCta('Tile E'),
            'Tertiary Card 6': lambda: b.imageHeaderTextCta('Tile F'),
            'Tertiary Card 7': lambda: b.imageHeaderTextCta('Tile G'),
            'Tertiary Card 8': lambda: b.imageHeaderTextCta('Tile H'),
            'Tertiary Card 9': lambda: b.imageHeaderTextCta('Tile I'),
            'Tertiary Card 10': lambda: b.imageHeaderTextCta('Tile J'),
            'Vertical Interstitial Photo (G)': lambda: b.heroImageHeaderTextCta('Tile B'),
            'Marketing Message (H)': lambda: b.headerTextCta(),
        })


class LandingPageA(CIF):
    pass
    # Narrative Element 2 - Content Image Cluster (K)
    # Narrative Element 4 - Content Image Cluster (O)
    # Narrative Element 5 - Content Image Cluster (N)

class LandingPageB(CIF):
    pass
    # Narrative Element 1 - Content Image Cluster
    # Narrative Element 3 - Content Image Cluster
    # Narrative Element 6 - Content Image Cluster

    # 'Content Image Cluster Tile 1': lambda: b.imageMosaicHeadingTextCta('Tile D'),
    # 'Content Image Cluster Tile 2': lambda: b.imageMosaicHeadingTextCta('Tile E'),
    # 'Content Image Cluster Tile 3': lambda: b.imageMosaicHeadingTextCta('Tile F'),
