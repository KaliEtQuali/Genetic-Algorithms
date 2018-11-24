#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:35:19 2018

@author: kalenga
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:17:09 2017

@author: kalenga
"""


class Case:
    def __init__(self, i, j,value):
        self.i = i
        self.j = j
        self.i_pixel = i*24
        self.j_pixel = j*24
        self.value = value
        self.state = "up"
        self.sensors = {"front": 0, "left": 0, "right": 0}
        
    def __repr__(self):
        return "Case {},{}   value: {}".format(self.i, self.j, self.value) 
    
    def set_state(self, state):
        self.state = state
        
    def set_value(self,value):
        self.value=value
        
    def up(self):
        if self.value == "RevealedMine":
            self.set_state("mine")
        elif self.value == "Flagged":
            self.set_state("flag")
        else:
            self.set_state("up")
    
    def down(self):
        self.set_state("down")
        
    def sense(self):
        if self.value == "RevealedMine":
            self.set_state("sense_mine")
        else:
            self.set_state("sense_empty")
        
    def set_sensors(self, sensor, value):
        self.sensors[sensor] = value
            
    