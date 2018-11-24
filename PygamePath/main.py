#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:44:25 2018

@author: kalenga
"""

import pygame
from pygame.locals import *
import numpy as np
from random import randint
import time
import sys
from grid import Grid
from view import View
from gene import Gene
from population import Population

def play_gene(gene, grid, view):
    res = "nothin"
    gene.sensors = grid.current_case.sensors
    gene_continue = 1
    while gene_continue:
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
            
            if event.type == KEYDOWN:
                if event.key == K_q:
                    gene_continue=0
                        
        res = grid.move(gene.determine_action())
        gene.sensors = grid.current_case.sensors
        if res == "win" or res == "lose":
            gene.score = grid.compute_score()
            grid.text_fields["Gene"].increment()
            if res == "win":
                grid.text_fields["Pop wins"].increment()
                grid.text_fields["Total wins"].increment()
            gene_continue = 0
            
        view.display_grid(grid)
        view.display_text_fields(grid)
        pygame.display.flip()
        
def play_populations(nb_populations, population_size, grid, view):
    for population_index in range(nb_populations):
        population = Population(population_index, population_size)
        for gene in population.genes:
            play_gene(gene, grid, view)
        grid.text_fields["Population"].increment()
        grid.text_fields["Gene"].display("0")
        grid.text_fields["Pop wins"].display("0")
    population.sort_genes()
    print(population.genes)
    
def play_populations_with_evolution(nb_populations, population_size, grid, view):
    population = Population(0, population_size)
    for population_index in range(nb_populations):
        for gene in population.genes:
            play_gene(gene, grid, view)
        grid.text_fields["Population"].increment()
        grid.text_fields["Gene"].display("0")
        grid.text_fields["Pop wins"].display("0")
        population = Population(population_index, population_size, population.evolve())
    return population.genes[-2]
        

#generic_grid =  Grid(20,20,60, ["Population", "Gene", "Pop wins", "Total wins"])    

best_gene = {}   
def test(width, height, nb_mines, population_size, random_gene=False, grid=None):
    if not grid:
        grid = Grid(width, height, nb_mines, ["Population", "Gene", "Pop wins", "Total wins"])
    else:
        grid.text_fields["Population"].display("0")
        grid.text_fields["Gene"].display("0")
        grid.text_fields["Pop wins"].display("0")
        grid.text_fields["Total wins"].display("0")
    view = View(width,height,24)
    view.display_text_fields(grid)
    res = "nothin"
    
    if random_gene:
        wheels = np.ndarray([4,6])
        for i in range(4):
            for j in range(6):
                wheels[i,j] = randint(0,1)
        play_gene(Gene(0,1, wheels), grid, view)
    else:
        play_gene(Gene(0,1), grid, view)
        
    #best_gene = play_populations_with_evolution(150, 50, grid, view)
    print(grid.current_case.sensors)    
    game_continue = 1
    while game_continue:
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
            
            if event.type == KEYDOWN:
                if event.key == K_q:
                    game_continue=0
                else:
                    if event.key == K_UP:
                        res = grid.move("up")
                    if event.key == K_DOWN:
                        res = grid.move("down")
                    if event.key == K_LEFT:
                        res = grid.move("left")
                    if event.key == K_RIGHT:
                        res = grid.move("right")
                if res == "win" or res == "lose":
                    grid.text_fields["Gene"].increment()
                    if res == "win":
                        grid.text_fields["Pop wins"].increment()
                        grid.text_fields["Total wins"].increment()
                if grid.text_fields["Gene"].current_string == str(population_size):
                    grid.text_fields["Population"].increment()
                    grid.text_fields["Gene"].display("0")
                    grid.text_fields["Pop wins"].display("0")
                print(grid.current_case.sensors)
        view.display_grid(grid)
        view.display_text_fields(grid)
        pygame.display.flip()
        

pygame.init()
test(20,20,60, 5, True, generic_grid)

a = [ {'x':3}, {'f': 0}]
b = {'x':3, 'f': 0}
print(type(a), type(b))