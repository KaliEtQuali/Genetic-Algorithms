#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:29:54 2017

@author: kalenga
"""
import pygame

class Input:
    def __init__(self,window,position,label):
        self.window = window
        self.position = position
        self.label = label
        self.current_string = ""
        self.message = self.label + ": " + self.current_string
        if label=="Width" or label=="Height":
            self.spaces = "             "
            self.symbol_limit=10
        else:
            self.spaces = "   "
            self.symbol_limit=6
        self.top = position*(window.get_height() / 5) - 10
        self.bottom = self.top + 20
        self.left = window.get_width() - 180
        self.right = self.left + 150
        self.border_color = (255,255,255)
        
    def __repr__(self):
        return "Input: {}, {}".format(self.label,self.message)
        
    def display(self, current_string):
        self.current_string = current_string
        self.message = self.label + ": " + self.spaces + self.current_string
        fontobject = pygame.font.Font(None,18)
        pygame.draw.rect(self.window, (0,0,0),(self.left,self.top,150,20), 0)
        pygame.draw.rect(self.window, self.border_color,(self.left-2,self.top-2,154,24), 1)
        if len(self.message) != 0:
            self.window.blit(fontobject.render(self.message, 1, (255,255,255)),(self.left, self.top))
        pygame.display.flip()
            
    def focus_yourself(self):
        self.border_color = (255,0,0)
        pygame.draw.rect(self.window, self.border_color,(self.left-2,self.top-2,154,24), 1)
        pygame.display.flip()
        
    def unfocus_yourself(self):
        self.border_color = (255,255,255)
        pygame.draw.rect(self.window, self.border_color,(self.left-2,self.top-2,154,24), 1)
        pygame.display.flip()
        
    def increment(self):
        self.current_string = str(int(self.current_string) + 1)
        self.display(str(int(self.current_string)))