# Content Intake Form Names
class CIF:
    def __init__(self, b: 'Build'):
        self.names = {
            'Hero Image': lambda: b.singleHeroImage(),
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
        }

class RoomDetails(CIF):
    def __init__(self, b):
        super().__init__(b)
        self.names.update({
            'Intro (A)': lambda: b.roomLongDescription(),
        })