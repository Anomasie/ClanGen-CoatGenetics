import random
from random import choice

class PeltGenome:
    # base color series
    pelt_colours_black_series = [
        "BLACK",    # BLACK
        "GHOST",    # BLACK + smoked
        "SILVER",   # BLACK + shaded
        "DARKGREY", # BLACK + dd
        "GREY",     # BLACK + dd + smoked
        "PALEGREY", # BLACK + dd + shaded
        "LILAC",    # BLACK + dd + caramel
        "LILAC",    # BLACK + dd + caramel + smoked
        "LIGHTBROWN",    # BLACK + dd + caramel + shaded
    ]
    pelt_colours_brown_series = [
        "CHOCOLATE",    # BROWN
        "DARKBROWN",    # BROWN + smoked
        "LILAC",        # BROWN # shaded
        "GOLDEN-BROWN", # BROWN + dd
        "PALEGINGER",   # BROWN + dd + smoked
        "CREAM",        # BROWN + dd + shaded
        "LILAC",        # BROWN + dd + caramel
        "LILAC",        # BROWN + dd + caramel + smoked
        "LIGHTBROWN",   # BROWN + dd + caramel + shaded
    ]
    pelt_colours_cinnamon_series = [
        "SIENNA",       # CINNAMON
        "SIENNA",       # CINNAMON + smoked
        "PALEGINGER",   # CINNAMON + shaded
        "GREY",         # CINNAMON + dd
        "SILVER",       # CINNAMON + dd + smoked
        "PALEGREY",     # CINNAMON + dd + shaded
        "LIGHTBROWN",   # CINNAMON + dd + caramel
        "LIGHTBROWN",   # CINNAMON + dd + caramel + smoked
        "WHITE",        # CINNAMON + dd + caramel + shaded
    ]
    pelt_colours_red_series = [
        "DARKGINGER",   # RED
        "GINGER",       # RED + smoked
        "CREAM",        # RED + shaded
        "PALEGINGER",   # RED + dd
        "PALEGINGER",   # RED + dd + smoked
        "CREAM",        # RED + dd + shaded
        "GOLDEN",       # RED + dd + caramel
        "GOLDEN",       # RED + dd + caramel + smoked
        "CREAM",        # RED + dd + caramel + shaded
    ]

    # patterns
    ## Missing: SingleColour, TwoColour, Smoke, Tortie, Calico
    pelt_patterns_mackerel = [
        "Mackerel",
        "Masked"
    ]
    pelt_patterns_blotched = [
        "Tabby",
        "Classic",
        "Sokoke",
        "Marbled"
    ]
    pelt_patterns_spotted = [
        "Speckled",
        "Rosette",
        "Bengal"
    ]
    pelt_patterns_ticked = [
        "Ticked",
        "Agouti",
        "Singlestripe"
    ]
    
    def __init__(
        self,
    ) -> None:
        print("initialized!")
    
    def pattern_color_inheritance_realistic(self, parents: tuple = (), gender="female"):
        # setting parent pelt categories
        # We are using a set, since we don't need this to be ordered, and sets deal with removing duplicates.
        

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        


        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        print("1!")

    def randomize_gene(locus, locus_alleles):
        locus = set(choice(locus_alleles), choice(locus_alleles))

genome = PeltGenome()