#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 17:21:18 2018

@author: kalenga
"""
import numpy as np
from random import randint, shuffle, uniform
from gene import Gene

class Population:
    def __init__(self, Id,  size, genes=None):
        self.id = Id
        self.size = size
        self.crossover_methods = ["one point crossover", "uniform crossover", "two points crossover"]
        if genes:
            self.genes = genes
        else:
            self.genes = []
            for gene_index in range(size):
                wheels = np.ndarray([4,6])
                for i in range(4):
                    for j in range(6):
                        wheels[i,j] = randint(0,1)
                self.genes.append(Gene(gene_index, Id, wheels))
            
    def __repr__(self):
        return "Population {}  size {}".format(self.id, self.size)

    def sort_genes(self):
        self.quickSort(self.genes)
        
        
    def quickSort(self, alist):
       self.quickSortHelper(alist,0,len(alist)-1)
    
    
    def quickSortHelper(self, alist,first,last):
       if first<last:
    
           splitpoint = self.partition(alist,first,last)
    
           self.quickSortHelper(alist,first,splitpoint-1)
           self.quickSortHelper(alist,splitpoint+1,last)
           
    def parent_selection(self):
        n = 0
        picking_list = []
        for gene in self.genes:
            n += -gene.score
        for gene in self.genes:
            number = int((-100*gene.score)/n)
            for i in range(number):
                picking_list.append(gene)
        shuffle(picking_list)
        return picking_list
    
    
    def evolve(self, picking_list=None):
        if not picking_list:
            picking_list = self.parent_selection()
        next_genes = []
        nb_crossover_children = self.size - 6
        # Crossover children
        for i in range(int(nb_crossover_children/2)):
            parent1 = picking_list[randint(0,len(picking_list) - 1)]
            parent2 = picking_list[randint(0,len(picking_list) - 1)]
            crossover_method = self.crossover_methods[randint(0,len(self.crossover_methods) - 1)]
            wheels1, wheels2 = self.crossover(parent1, parent2, crossover_method)
            next_genes.append(Gene(len(next_genes), self.id + 1, wheels1))
            next_genes.append(Gene(len(next_genes), self.id + 1, wheels2))
        # Creating two random genes to insure fresh genes occurance
        next_genes.append(self.create_random_gene(len(next_genes), self.id + 1))
        next_genes.append(self.create_random_gene(len(next_genes), self.id + 1, 100))
        # Keeping the two best of previous population
        self.sort_genes()
        self.genes.reverse()
        best_mom = Gene(len(next_genes),self.id + 1, self.genes[0].wheels)
        next_genes.append(best_mom)
        for gene in self.genes[1:]:
            best_dad = Gene(len(next_genes),self.id + 1, gene.wheels)
            if best_dad.wheels.all() != best_mom.wheels.all():
                break
        next_genes.append(best_dad)
        # Slightly change the two best genes of previous population
        best_mom_changed = Gene(len(next_genes),self.id + 1, best_mom.wheels)
        best_mom_changed.slightly_change_gene()
        next_genes.append(best_mom_changed)
        best_dad_changed = Gene(len(next_genes),self.id + 1, best_dad.wheels)
        best_dad_changed.slightly_change_gene()
        next_genes.append(best_dad_changed)
        
        return next_genes
         
        
    
    @staticmethod
    def create_random_gene(gene_id, gene_population, upper_wheel_limit=2.0):
        wheels = np.ndarray([4,6])
        for i in range(4):
            for j in range(6):
                wheels[i,j] = uniform(0.0,upper_wheel_limit)
        return Gene(gene_id, gene_population, wheels)
    
     
    @staticmethod
    def crossover(gene1, gene2, method="one point crossover"):
        shape = gene1.wheels.shape
        rows = shape[0]
        cols = shape[1]
        if method == "one point crossover":
            choices = ["from start", "from end"]
            choice = randint(0,1)
            choice = choices[choice]
            if choice == "from start":
                for i in range(rows - 1):
                    limit = randint(0,cols - 1)
                    for j in range(limit):
                        temp = gene1.wheels[i,j]
                        gene1.wheels[i,j] = gene2.wheels[i,j]
                        gene2.wheels[i,j] = temp
            else:
                for i in range(rows - 1):
                    limit = randint(0,cols - 1)
                    for j in range(limit, cols - 1):
                        temp = gene1.wheels[i,j]
                        gene1.wheels[i,j] = gene2.wheels[i,j]
                        gene2.wheels[i,j] = temp
            return gene1.wheels, gene2.wheels
        
        elif method == "uniform crossover":
            for i in range(rows - 1):
                for j in range(cols - 1):
                    if randint(0,1):
                        temp = gene1.wheels[i,j]
                        gene1.wheels[i,j] = gene2.wheels[i,j]
                        gene2.wheels[i,j] = temp
                    else:
                        continue
            return gene1.wheels, gene2.wheels
        
        elif method == "two points crossover":
            for i in range(rows - 1):
                first_point = randint(0,cols - 2)
                second_point = randint(first_point + 1, cols - 1)
                temp = gene1.wheels[first_point:second_point + 1]
                gene1.wheels[first_point:second_point + 1] = gene2.wheels[first_point:second_point + 1]
                gene2.wheels[first_point:second_point + 1] = temp
            return gene1.wheels, gene2.wheels
        
            
    @staticmethod
    def partition(alist,first,last):
       pivotvalue = alist[first].score
    
       leftmark = first+1
       rightmark = last
    
       done = False
       while not done:
    
           while leftmark <= rightmark and alist[leftmark].score <= pivotvalue:
               leftmark = leftmark + 1
    
           while alist[rightmark].score >= pivotvalue and rightmark >= leftmark:
               rightmark = rightmark -1
    
           if rightmark < leftmark:
               done = True
           else:
               temp = alist[leftmark]
               alist[leftmark] = alist[rightmark]
               alist[rightmark] = temp
    
       temp = alist[first]
       alist[first] = alist[rightmark]
       alist[rightmark] = temp
    
    
       return rightmark

        