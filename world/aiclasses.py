from aitools import *
#from state import *
import time

class Government:
    def __init__(self):      # All stats 0-100
        self.military = 0    # Military Power    
        self.resources = 0   # Available raw resources
        self.funds = 0       # Available money
        self.tech = 0        # Technological superiority
        self.freedom = 0     # Freedom of citizenry
        self.discipline = 0  # Overall organization and effectiveness of command structure
        self.centralized = 0 # Is the government susceptible to collapse in key areas, or will it hold together if a major system falls
        self.loyalty = 0     # Are the denizens loyal to there government, or easily subverted
        self.covert = 0      # Extent of the governments covert network
        
        
class Job:
    def __init__(self):
        self.stubborn = 0
        self.patient = 0
        self.openminded = 0
        self.strong = 0
        self.shy = 0
        self.trained = 0
        self.experienced = 0
        self.religious = 0
        self.brutal = 0
        self.intelligent = 0
        self.satisfied = 0
        self.rowdy = 0
        self.antsy = 0
        
class Personality:
    def __init__(self):
        self.training = 0
        self.experience = 0
        self.bravery = 0
        self.intelligence = 0
        self.tenacity = 0
        self.morality = 0
        self.loyalty = 0
        self.honesty = 0
        self.mercy = 0
        self.faith = 0
