import random
from random import choice

import json

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
    pelt_patterns_blotched = [
        "Tabby",
        "Classic",
        "Sokoke",
        "Marbled"
    ]
    pelt_patterns_mackerel = [
        "Mackerel",
        "Masked"
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

    # load json files
    with open('resources/genetics/pelt_genotypes.json') as f:
        pelt_genotypes = json.load(f)
    with open('resources/genetics/pelt_phenotypes.json') as f:
        pelt_phenotypes = json.load(f)
    with open('resources/genetics/pelt_genotypes_requirements.json') as f:
        pelt_genotype_requirements = json.load(f)
    
    def __init__(
        self,
        genotype: dict = None,
        phenotype: dict = None
    ) -> None:
        if genotype:
            self.genotype = genotype
            self.phenotype = self.get_phenotype()
        elif phenotype:
            self.genotype = self.get_genotype(phenotype)
            self.phenotype = phenotype
        else:
            self.random_genotype()
            self.phenotype = self.get_phenotype()

    def check_genotype(self) -> bool:
        # check dna
        if not self.genotype:
            print("WARNING in check_genotype: no genotype")
            return False
        for locus in self.pelt_genotypes.keys():
            if locus in self.genotype.keys():
                # enough allels?
                if len(self.genotype[locus]) > 2:
                    print("WARNING in check_genotype: too many allels")
                    return False # too many allels
                elif len(self.genotype[locus]) == 1 and locus != "X":
                    print("WARNING in check_genotype: too few allels")
                    return True # too few allels
                elif len(self.genotype[locus]) == 0 and locus != "Y":
                    print("WARNING in check_genotype: too few allels for a female cat")
                    return False # too few allels
    			# does this allel exist?
                for allel in self.genotype[locus]:
                    if not allel in self.pelt_genotypes[locus]:
                        print("WARNING in check_genotype: allel ", allel, " not known at locus ", locus)
                        return False
            # chromosome missing => damaged dna
            else:
                print("WARNING in check_genotype: missing allel")
                return False
        return True
    
    def is_female(self) -> bool:
        if self.check_genotype():
            return not "Y" in self.genotype["X"]
        else:
            print("ERROR in is_female: invalid dna")
    
    # ------------------------------------------------------------------------------------------------------------#
    #   RANDOM GENOME GENERATION
    # ------------------------------------------------------------------------------------------------------------#

    def random_genotype(self, female = None):
        # random dna
        self.genotype = {}
        for chromosome in self.pelt_genotypes.keys():
            self.genotype[chromosome] = [
                self.random_trait(self.pelt_genotypes[chromosome]),
                self.random_trait(self.pelt_genotypes[chromosome])
            ]
            self.genotype[chromosome].sort()
        if female is None:
            female = choice([True, False])
        if not female: # delete second X-chromosome
            self.genotype["X"] = [self.genotype["X"][0]]

    def random_trait(self, options):
        given_trait = ""
        random_number = random.randint(1, 100)
        summe = 0
        for option in options.keys():
            summe += options[option]["rarity"]
            if given_trait == "" and random_number <= summe:
                given_trait = options[option]["gen"]
        return given_trait

    # ------------------------------------------------------------------------------------------------------------#
    #   REALISTIC INHERITANCE
    # ------------------------------------------------------------------------------------------------------------#

    def from_parents( self, parent_1, parent_2 ):
        # generate kitten_dna
        self.genotype = {}
        # go through every chromosome
        for chromosome in parent_1.genotype.keys():
            if chromosome != "X":
                self.genotype[chromosome] = [choice(parent_1.genotype[chromosome]), choice(parent_2.genotype[chromosome])]
            # the kitten shall become a female
            elif random.random() < 0.5:
                self.genotype[chromosome] = [choice(parent_1.genotype[chromosome]), choice(parent_2.genotype[chromosome])]
    		# the kitten will become a male
            else:
                self.genotype[chromosome] = [choice(parent_1.genotype[chromosome])]
            self.genotype[chromosome].sort() #2

    # ------------------------------------------------------------------------------------------------------------#
    #   GENOTYPE -> PHENOTYPE
    # ------------------------------------------------------------------------------------------------------------#

    def has_trait(self, trait) -> bool:
        if "require" in trait.keys():
            for condition in trait["require"]:
                # size requirements
                if "size" in condition.keys():
                    if len(self.genotype[condition["locus"]]) != condition["size"]:
                        return False
                # allel requirements
                if "gen" in condition.keys():
                    # specific allels required
                    if type(condition["gen"]) is list:
                        if self.genotype[condition["locus"]] != condition["gen"]:
                            return False
                    else:
                        if not condition["gen"] in self.genotype[condition["locus"]]:
                            return False
        return True
    
    def get_phenotype(self) -> dict:
        phenotype = {}
        for feature in self.pelt_phenotypes.keys(): # such as diluted, color, ...
            result = []
            found = False
            exclusive_mode = True
            # go through every possible option
            for option in self.pelt_phenotypes[feature]:
                if not found:
                    if "exclusive" in option.keys():
                        # case 1: option needs to stand alone
                        if option["exclusive"] and exclusive_mode:
                            if self.has_trait(option):
                                result.append(option["trait"])
                                found = True
                        # case 2: one other trait can be appended after this one
                        elif not option["exclusive"]:
                            if self.has_trait(option):
                                result.append(option["trait"])
                                exclusive_mode = False
                    else:
                        if self.has_trait(option):
                            result.append(option["trait"])
                            found = True # finish searching
            phenotype[feature] = result
        return phenotype

    def has_feature(self, phenotype, feature) -> bool:
        # no requirements
        if not "require" in feature:
            return True
        # check requirements
        for requirement in feature["require"]:
            if "feature" in requirement and not requirement["feature"] in phenotype[requirement["category"]]:
                return False
            if "feature_in" in requirement:
                found_one = False
                for has_features in phenotype[requirement["category"]]:
                    if has_features in requirement["feature_in"]:
                        found_one = True
                if not found_one:
                    return False
            if "size" in requirement and not len(phenotype[requirement["category"]]) == requirement["size"]:
                return False
        return True

    def get_genotype(self, pelt) -> dict:
        phenotype = {}

        

        return self.get_genotype_from_phenotype(phenotype)

    def get_genotype_from_phenotype(self, phenotype) -> dict:
        genotype = {}
        for locus in self.pelt_genotype_requirements.keys():
            result = []
            i = 0
            # go through every possible option
            for option in self.pelt_genotype_requirements[locus]:
                if len(result) == 0 and self.has_feature(phenotype, option):
                    if "trait" in option.keys():
                        result = option["trait"]
                    elif "traits" in option.keys():
                        result = choice(option["traits"])
                    else:
                        result = [
                            self.random_trait(self.pelt_genotypes[locus]),
                            self.random_trait(self.pelt_genotypes[locus])
                        ]
                i += 1
            genotype[locus] = result
        return genotype

    def get_pelt_eye_color(self, pelt, color):
        match color:
            case "red":
                return "COPPER"
            case "blue":
                return choice(pelt.blue_eyes)
            case "brown":
                return choice(["BRONZE", "AMBER", "HAZEL"])
            case "green":
                return choice(pelt.green_eyes)
        return choice(pelt.yellow_eyes)