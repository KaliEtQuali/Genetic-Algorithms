#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:23:37 2018

@author: kalenga
"""
from case2 import Case
from text_field import TextField
from random import randint
from math import sqrt

class Grid:
    def __init__(self, width, height, nb_mines, boxes=[]):
        self.width = width
        self.height = height
        self.nb_mines = nb_mines
        self.grid=[]
        self.mines = []
        if nb_mines == 0:
            for i in range(height):
                line=[]
                for j in range(width):
                    line.append(Case(i,j, "Empty"))
                self.grid.append(line)
        elif nb_mines>width*height:
            for i in range(height):
                line=[]
                for j in range(width):
                    line.append(Case(i,j, "RevealedMine"))
                self.grid.append(line)
        else:
            if width*height>2*nb_mines:
                for i in range(height):
                    line=[]
                    for j in range(width):
                        line.append(Case(i,j, "Empty"))
                    self.grid.append(line)
                mines_posed=0
                while mines_posed<nb_mines:
                    i = randint(0,height-1)
                    j = randint(0,width-1)
                    if self.grid[i][j].value == "Empty" and i*j != 0 and i+j != height + width - 2:
                        self.grid[i][j].set_value("RevealedMine")
                        self.mines.append({"i":i,"j":j})
                        mines_posed+=1
            else:
                for i in range(height):
                    line=[]
                    for j in range(width):
                        line.append(Case(i,j, "RevealedMine"))
                    self.grid.append(line)
                    empty_posed=0
                while empty_posed<width*height-nb_mines:
                    i = randint(0,height-1)
                    j = randint(0,width-1)
                    if self.grid[i][j].value == "RevealedMine":
                        self.grid[i][j].set_value("Empty")
                        empty_posed+=1
        # Ici la grid est crée, chaque case a une valeur qui est soit Empty soit RevealedMine
        # Donc on set le state pour que les images correspondent
        for line in self.grid:
            for case in line:
                if case.value == "RevealedMine":
                    case.set_state("mine")
                else:
                    case.set_state("up")
        self.current_case = self.grid[0][0]
        self.previous_case = self.grid[0][0]
        self.current_case.set_state("down")

        self.grid[-1][-1].set_value("Flagged")
        self.grid[-1][-1].set_state("flag")

        self.track = {(str(self.current_case.i) + str(self.current_case.j)): 1}
        self.track_count = 0
        
        self.current_sensors_cases = []
        self.previous_sensors_case = []
        self.set_sensors()
        self.text_fields = {}
        if len(boxes)>0:
            for i in range(len(boxes)):
                self.text_fields[boxes[i]] = TextField(i + 1, len(boxes), boxes[i], 24*self.width + 200, 24*self.height)
        
        
        
    def __repr__(self):
        return "Grid({}x{}) - Mines: {} - Current case : {}".format(self.width, self.height, self.nb_mines, self.current_case)



    def expose_sensors(self, case):
        sensors_cases = []
        # To the front
        if case.i + 1 <= self.height - 1:
            if self.grid[case.i + 1][case.j].value == "RevealedMine":
                sensors_cases.append(self.grid[case.i + 1][case.j])
                case.set_sensors("front", 1)
            else:
                if case.i + 2 <= self.height - 1:
                    if self.grid[case.i + 2][case.j].value == "RevealedMine":
                        sensors_cases.append(self.grid[case.i + 2][case.j])
                        case.set_sensors("front", 2)
                    else:
                        if case.i + 3 <= self.height - 1:
                            sensors_cases.append(self.grid[case.i + 3][case.j])
                            case.set_sensors("front", 3)
                        else:
                            sensors_cases.append(self.grid[case.i + 2][case.j])
                            case.set_sensors("front", 2)
                else:
                    sensors_cases.append(self.grid[case.i + 1][case.j])
                    case.set_sensors("front", 1)
        else:
            case.set_sensors("front", 0)

        # To the left
        if case.j + 1 <= self.width - 1:
            if self.grid[case.i][case.j + 1].value == "RevealedMine":
                sensors_cases.append(self.grid[case.i][case.j + 1])
                case.set_sensors("left", 1)
            else:
                if case.j + 2 <= self.width - 1:
                    if self.grid[case.i][case.j + 2].value == "RevealedMine":
                        sensors_cases.append(self.grid[case.i][case.j + 2])
                        case.set_sensors("left", 2)
                    else:
                        if case.j + 3 <= self.width - 1:
                            sensors_cases.append(self.grid[case.i][case.j + 3])
                            case.set_sensors("left", 3)
                        else:
                            sensors_cases.append(self.grid[case.i][case.j + 2])
                            case.set_sensors("left", 2)
                else:
                    sensors_cases.append(self.grid[case.i][case.j + 1])
                    case.set_sensors("left", 1)
        else:
            case.set_sensors("left", 0)

        # To the right
        if case.j - 1 >= 0:
            if self.grid[case.i][case.j - 1].value == "RevealedMine":
                sensors_cases.append(self.grid[case.i][case.j - 1])
                case.set_sensors("right", 1)
            else:
                if case.j - 2 >= 0:
                    if self.grid[case.i][case.j - 2].value == "RevealedMine":
                        sensors_cases.append(self.grid[case.i][case.j - 2])
                        case.set_sensors("right", 2)
                    else:
                        if case.j - 3 >= 0:
                            sensors_cases.append(self.grid[case.i][case.j - 3])
                            case.set_sensors("right", 3)
                        else:
                            sensors_cases.append(self.grid[case.i][case.j - 2])
                            case.set_sensors("right", 2)
                else:
                    sensors_cases.append(self.grid[case.i][case.j - 1])
                    case.set_sensors("right", 1)
        else:
            case.set_sensors("right", 0)

        for sense_case in sensors_cases:
            yield sense_case

    def set_sensors(self):
        for case in self.expose_sensors(self.previous_case):
            self.grid[case.i][case.j].up()
        for case in self.expose_sensors(self.current_case):
            self.grid[case.i][case.j].sense()


    def back_to_zero(self):
        self.previous_case = self.current_case
        self.current_case=self.grid[0][0]
        self.current_case.down()
        self.previous_case.up()
        self.set_sensors()
        self.track = {(str(self.current_case.i) + str(self.current_case.j)): 1}
        self.track_count = 0
        
        
    def update_track(self, i,j):
        is_new = True
        for place in self.track:
            if place == str(i) + str(j):
                self.track[place] += 1
                is_new = False
        if is_new:
            self.track[str(i) + str(j)] = 1
    
    def is_circling(self):
        is_circling = False
        for place, count in self.track.items():
            if count >= 15:
                is_circling = True
        return is_circling
    
    def compute_score(self):
        return -int((sqrt((self.previous_case.i - self.height + 1)**2 + (self.previous_case.j - self.width + 1)**2))*100)/100


    def move(self, move):
        if move == "up":
            if self.current_case.i > 0:
                self.previous_case = self.current_case
                self.current_case=self.grid[self.previous_case.i - 1][self.previous_case.j]
                self.current_case.down()
                self.previous_case.up()
                self.set_sensors()
        if move == "down":
            if self.current_case.i < len(self.grid) - 1:
                self.previous_case = self.current_case
                self.current_case=self.grid[self.previous_case.i + 1][self.previous_case.j]
                self.current_case.down()
                self.previous_case.up()
                self.set_sensors()
        if move == "left":
            if self.current_case.j > 0:
                self.previous_case = self.current_case
                self.current_case=self.grid[self.previous_case.i][self.previous_case.j - 1]
                self.current_case.down()
                self.previous_case.up()
                self.set_sensors()
        if move == "right":
            if self.current_case.j < len(self.grid[0]) - 1:
                self.previous_case = self.current_case
                self.current_case=self.grid[self.previous_case.i][self.previous_case.j + 1]
                self.current_case.down()
                self.previous_case.up()
                self.set_sensors()
                
        self.update_track(self.current_case.i, self.current_case.j)
        
        if self.current_case.value == "RevealedMine":
            self.back_to_zero()
            print("mine")
            return "lose"
        elif self.current_case.value == "Flagged":
            self.back_to_zero()
            print("win")
            return "win"
        elif self.is_circling():
            self.back_to_zero()
            print("circling")
            return "lose"
        else:
            return "nothin"
    
    