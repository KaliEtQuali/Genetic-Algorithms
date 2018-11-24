#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:06:33 2018

@author: kalenga
"""
import pygame

class View:
    def __init__(self, width, height, case_size):
        self.width = width
        self.height = height
        self.case_size = case_size
        self.width_pixel = self.case_size*width
        self.height_pixel= self.case_size*height
        self.window = pygame.display.set_mode((self.width_pixel + 200, self.height_pixel))
        self.cells = {
                "up": pygame.image.load("./assets/Cell.png").convert(),
                "down": pygame.image.load("./assets/CellDown.png").convert(),
                "mine": pygame.image.load("./assets/RevealedMineCell.png").convert(),
                "flag": pygame.image.load("./assets/FlaggedCell.png").convert(),
                "sense_empty": pygame.image.load("./assets/EmptyCell.png").convert(),
                "sense_mine": pygame.image.load("./assets/ExplodedMineCell.png").convert()}
        
        
    def __repr__(self):
        return "View__ window({}x{})".format(self.width_pixel, self.height_pixel)
        
        
    def display_grid(self, grid):
        for line in grid.grid:
            for case in line:
                self.window.blit(self.cells[case.state],(case.j_pixel,case.i_pixel))
                
    def display_text_fields(self, grid):
        if grid.text_fields:
            for key, text_field in grid.text_fields.items():
                fontobject = pygame.font.Font(None,18)
                pygame.draw.rect(self.window, (0,0,0),(text_field.left,text_field.top,150,20), 0)
                pygame.draw.rect(self.window, text_field.border_color,(text_field.left-2,text_field.top-2,154,24), 1)
                if len(text_field.message) != 0:
                    self.window.blit(fontobject.render(text_field.message, 1, (255,255,255)),(text_field.left, text_field.top))
                    
    def update_text_fields(self, grid):
        for key, text_field in grid.text_fields.items():
            fontobject = pygame.font.Font(None,18)
            if len(text_field.message) != 0:
                self.window.blit(fontobject.render(text_field.message, 1, (255,255,255)),(text_field.left, text_field.top))