#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:04:46 2018

@author: kalenga
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:29:54 2017

@author: kalenga
"""

class TextField:
    def __init__(self,position, nb_fields, label, window_width, window_height):
        self.position = position
        self.label = label
        self.current_string = "0"
        self.message = self.label + ": " + self.current_string
        self.top = position*(window_height / (nb_fields + 1)) - 10
        self.bottom = self.top + 20
        self.left = window_width - 180
        self.right = self.left + 150
        self.border_color = (255,255,255)
        
    def __repr__(self):
        return "Text Field: {}, {}".format(self.label,self.message)
        
    def display(self, current_string):
        self.current_string = current_string
        self.message = self.label + ":  "+ self.current_string
        
        
    def increment(self):
        self.current_string = str(int(self.current_string) + 1)
        self.display(str(int(self.current_string)))