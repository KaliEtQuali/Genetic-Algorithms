#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 12:12:36 2018

@author: kalenga
"""
import numpy as np
from random import randint, uniform

class Gene:
    def __init__(self, Id, population, wheels=np.ones([4,6])):
        self.id = Id
        self.population = population
        self.score = 0
        self.wheels = wheels
        self.sensors = {"front": 0, "left": 0, "right": 0}
        self.track = []
        self.track_count = 0
    
    def __repr__(self):
        return "Id: {} \nPopulation: {} \nScore: {}".format(self.id, self.population, self.score)
    
    def update_track(self, i,j):
        if len(self.track)>0:
            for place in self.track:
                if place == (i,j):
                    self.track_count += 1
                else:
                    self.track.append((i,j))
        else:
            self.track.append((i,j))
    
    def is_circling(self):
        if self.track_count >=5:
            return True
        else:
            return False
        
    def set_sensors(self, sensor, value):
        self.sensors[sensor] = value
        
    def determine_action(self):
        # determine what to do depending on the sensors and the wheels
        sensor_array = np.ndarray([6,1])
        sensor_array[0,0] = self.sensors["front"]
        sensor_array[1,0] = self.sensors["front"]**2
        sensor_array[2,0] = self.sensors["left"]
        sensor_array[3,0] = self.sensors["left"]**2
        sensor_array[4,0] = self.sensors["right"]
        sensor_array[5,0] = self.sensors["right"]**2
        actions = np.matmul(self.wheels, sensor_array)
        keys = ["up", "down", "left", "right"]
        return keys[np.argmax(actions)]

    def slightly_change_gene(self):
       nb_changes = randint(0,1)
       shape = self.wheels.shape
       rows = shape[0]
       cols = shape[1]
       for k in range(nb_changes):
           for i in range(rows - 1):
               j = randint(0, cols - 1)
               self.wheels[i,j] += uniform(0.1, 2.0)
        