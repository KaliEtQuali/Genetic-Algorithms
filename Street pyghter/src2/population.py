import pygame
import threading
import time
import random
import os
import json
import copy
import multiprocessing as mp
import numpy as np
from math import floor
from operator import itemgetter, add
from gene import Gene
from Train_Round import Player, Game, Background
from neural_net import simplest_neural_net_ever
from internal_bot import Internal_bot
from color_constants import colors

alt_colors = []
for (root_dir, dir_names, file_names) in os.walk('../res/Char/Ken/KenClones'):
    for file_name in file_names:
        if file_name.endswith('png'):
            alt_colors.append('Clones/' + file_name.split('.')[0])

def ismember(A, B):
    return np.sum([ a == B for a in A ])

class Population:

    def __init__(self, nb_gene, genes=None):
        self.nb_gene = nb_gene
        self.population_number = 0
        if genes:
            self.genes = genes
        else:
            self.genes = []

            for i in range(nb_gene):
                self.genes.append(self.generate_random_gene(i, list(colors)[i]))


    def generate_random_gene(self, index_in_population, color_name):
        nn = simplest_neural_net_ever()
        return Gene('Ken', 120, 100, nn, index_in_population, color_name)


    def select_color(self):
        current_colors = [gene.color_name for gene in self.genes]
        color_name = random.choice(list(colors.items()))[0]
        while ismember(current_colors, color_name):
            color_name = random.choice(list(colors.items()))[0]
        return color_name


    def destroy_layers(self, hidden_layers):
        # Construire une liste avec tous les coefficients de tous les weights du nn1
        weights_list = []
        for layer in hidden_layers:
            for line in layer['weights']:
                for coeff in line:
                    weights_list.append(coeff)
        # Transformer cette liste en array
        weights_list = np.asarray(weights_list[:])

        # Faire de meme pour les bias
        bias_list = []
        for layer in hidden_layers:
            for line in layer['bias']:
                for coeff in line:
                    bias_list.append(coeff)
        bias_list = np.asarray(bias_list[:])

        # Retourner les listes sous forme de array
        return weights_list, bias_list



    def reform_layers(self, weights_vector, bias_vector, input_length, nb_hidden_layers, hidden_layers_length, output_length, return_in_layers_form=True):
        list_of_weights_matrices = []
        list_of_bias_vectors = []
        for i in range(nb_hidden_layers):
            if i == 0:
                weights = np.reshape(weights_vector[:input_length*hidden_layers_length], (input_length, hidden_layers_length))
                list_of_weights_matrices.append(weights)
                bias = np.reshape(bias_vector[:hidden_layers_length], (1, hidden_layers_length))
                list_of_bias_vectors.append(bias)
            elif i == nb_hidden_layers - 1:
                weights = np.reshape(weights_vector[input_length*hidden_layers_length + (nb_hidden_layers - 2)*hidden_layers_length*hidden_layers_length:], (hidden_layers_length, output_length))
                list_of_weights_matrices.append(weights)
                bias = np.reshape(bias_vector[(nb_hidden_layers-1)*hidden_layers_length:], (1,output_length))
                list_of_bias_vectors.append(bias)
            else:
                weights = np.reshape(weights_vector[input_length*hidden_layers_length + (i - 1)*hidden_layers_length*hidden_layers_length:input_length*hidden_layers_length + i*hidden_layers_length*hidden_layers_length], (hidden_layers_length, hidden_layers_length))
                list_of_weights_matrices.append(weights)
                bias = np.reshape(bias_vector[i*hidden_layers_length:(i+1)*hidden_layers_length], (1, hidden_layers_length))
                list_of_bias_vectors.append(bias)
            layers = []
        for i in range(len(list_of_bias_vectors)):
            layer = {}
            layer['weights'] = list_of_weights_matrices[i]
            layer['bias'] = list_of_bias_vectors[i]
            layers.append(layer)
        if return_in_layers_form:
            return layers
        else:
            return list_of_weights_matrices, list_of_bias_vectors


    def crossover(self, gene1, gene2, child_index_in_new_population):
        nn1 = gene1.neural_net
        nn2 = gene2.neural_net
        input_length = nn1.input_length
        nb_hidden_layers = nn1.nb_hidden_layers
        hidden_layers_length = nn1.hidden_layers_length
        output_length = nn1.output_length
        # Ramener les weights et bias des deux nn a des listes pour faciliter le crossover
        weights_list1, bias_list1 = self.destroy_layers(nn1.hidden_layers)
        weights_list2, bias_list2 = self.destroy_layers(nn2.hidden_layers)

        '''
        Rapide verification du bon fonctionnement de destroy et reform
        weights1_reformed, bias1_reformed = self.reform_layers(weights_list1, bias_list1, input_length, nb_hidden_layers, hidden_layers_length, output_length, False)
        n = len(nn1.hidden_layers)
        print('weights shape  ', [weights1_reformed[i].shape == nn1.hidden_layers[i]['weights'].shape for i in range(n)])
        print('bias shape  ', [bias1_reformed[i].shape == nn1.hidden_layers[i]['bias'].shape for i in range(n)])
        print('lens  ', len(weights1_reformed) == n and len(bias1_reformed) == n)
        print('weights content  ', [weights1_reformed[i] == nn1.hidden_layers[i]['weights'] for i in range(n)])
        print('bias content  ', [bias1_reformed[i] == nn1.hidden_layers[i]['bias'] for i in range(n)])
        '''

        # Perform two points crossover on weights
        point1 = random.randint(0,len(weights_list1))
        point2 = random.randint(0,len(weights_list1))
        if point2<point1:
            point1, point2 = point2, point1
        order = random.randint(0,1)
        if order == 1:
            child_weights = np.copy(weights_list2)
            tmp = weights_list1[point1:point2].copy()
            child_weights[point1:point2] = tmp
        else:
            child_weights = np.copy(weights_list1)
            tmp = weights_list2[point1:point2].copy()
            child_weights[point1:point2] = tmp
        # Perform crossover on biases
        point1 = random.randint(0,len(bias_list1))
        point2 = random.randint(0,len(bias_list1))
        if point2<point1:
            point1, point2 = point2, point1
        order = random.randint(0,1)
        if order == 1:
            child_bias = np.copy(bias_list2)
            tmp = bias_list1[point1:point2].copy()
            child_bias[point1:point2] = tmp
        else:
            child_bias = np.copy(bias_list1)
            tmp = bias_list2[point1:point2].copy()
            child_bias[point1:point2] = tmp
        # Create a neural net with those new created parameters
        child_hidden_layers = self.reform_layers(child_weights, child_bias, input_length, nb_hidden_layers, hidden_layers_length, output_length)
        child_nn = simplest_neural_net_ever(hidden_layers=child_hidden_layers)
        # Create gene based on this newly created neural network
        child_gene = Gene('Ken', 120, 100, child_nn, child_index_in_new_population, self.select_color())
        return child_gene


    def mutate(self, gene, mode='hard'):
        nn = gene.neural_net
        input_length = nn.input_length
        nb_hidden_layers = nn.nb_hidden_layers
        hidden_layers_length = nn.hidden_layers_length
        output_length = nn.output_length
        # Ramener les weights et bias du nn a des listes pour faciliter la mutation
        weights_list, bias_list = self.destroy_layers(nn.hidden_layers)
        if mode == 'hard':
            # Chaque element a une chance 1/taillle_du_vector d'etre muter
            for i in range(weights_list.shape[0]):
                mutate_or_not_mutate = random.random() > 1/weights_list.shape[0]
                if mutate_or_not_mutate:
                    weights_list[i] = random.random()*self.genes[0].neural_net.weights_output_coeff
            # de meme pour les bias
            for i in range(bias_list.shape[0]):
                mutate_or_not_mutate = random.random() > 1/bias_list.shape[0]
                if mutate_or_not_mutate:
                    bias_list[i] = random.random() + random.choice([1, -1])*self.genes[0].neural_net.bias_initial_coeff

        elif mode == 'soft':
            # on choisit d'abord au hasard le nombre d'element aui vont muter ensuite on choisit au hasard ceux aui vont muter
            nb_mutation = random.randint(4, weights_list.shape[0])
            for i in range(nb_mutation):
                mutated_index = random.randint(0, weights_list.shape[0] - 1)
                weights_list[mutated_index] = random.random()*2
            nb_mutation = random.randint(4, bias_list.shape[0])
            # de meme pour les bias
            for i in range(nb_mutation):
                mutated_index = random.randint(0, bias_list.shape[0] - 1)
                bias_list[mutated_index] = random.random()*2

        # Create a neural net with those new created parameters
        mutated_hidden_layers = self.reform_layers(weights_list, bias_list, input_length, nb_hidden_layers, hidden_layers_length, output_length)
        mutated_nn = simplest_neural_net_ever(hidden_layers=mutated_hidden_layers)
        # Create gene based on this newly created neural network
        mutated_gene = Gene('Ken', 120, 100, mutated_nn, 4, self.select_color())
        return mutated_gene


    def evolve(self, results):
        # Sort results and self.genes
        results_sorted= []
        for list in results:
            for result in list:
                results_sorted.append(result)
        results_sorted = sorted(results_sorted, key=itemgetter('score'))
        genes_sorted = []
        for gene_result in results_sorted:
            self.genes[gene_result['gene_number']].score = gene_result['score']
            genes_sorted.append(self.genes[gene_result['gene_number']].copy())
        self.genes = genes_sorted
        print('Parent population:\n', self.genes)

        # 40% bests as the winners
        n40 = floor(self.nb_gene*40/100)
        winners = []
        for i in range(1,n40 + 1):
            winners.append(self.genes[-i].copy())

        # 10% crossover of the 2 best of the bests
        n10 = floor(self.nb_gene*10/100)
        for i in range(n10):
            winners.append(self.crossover(winners[0], winners[1], 4))

        # 30% random crossover among the bests
        n30 = floor(self.nb_gene*30/100)
        for i in range(n30):
            index1 = random.randint(0,n40-1)
            index2 = random.randint(0,n40-1)
            while index1 == index2:
                index2 = random.randint(0,n40-1)
            winners.append(self.crossover(winners[index1], winners[index2], 4))

        # 20% random selection among the bests
        n20 = floor(self.nb_gene*20/100)
        for i in range(n20):
            index = random.randint(0,n40-1)
            winners.append(winners[index].copy())

        # Mutate the 4 last sets of genes
        for i in range(1,n10+n20+n30):
            winners[-i] = self.mutate(winners[-i])

        # If some genes are missing to fill the population then add some randomness
        if len(winners) < self.nb_gene:
            nb_missing = self.nb_gene - len(winners)
            for i in range(nb_missing):
                random_gene = self.generate_random_gene(4, self.select_color())
                winners.append(random_gene)
                print('random gene added')

        # Arrange the indexes_in_population and population_numbers
        self.population_number += 1
        for i in range(self.nb_gene):
            winners[i].index_in_population = i
            winners[i].population_number = self.population_number
        print('Child population:\n', winners)
        self.genes = winners


    def play_round(self, gene1, gene2, output, process_index):
        window_position = [((process_index%3)*600)%1920, ((process_index//3)*300)%1080]
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(window_position[0]) + "," + str(window_position[1])
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((320, 240), 0, 32)

        print('loading characters...')
        bot1 = Internal_bot(1, gene1.neural_net)
        player1 = Player(gene1.file, gene1.sprite_width, gene1.sprite_height, Player2=False, alt_color=gene1.alt_color)
        bot2 = Internal_bot(2, gene2.neural_net)
        player2 = Player(gene2.file, gene2.sprite_width, gene2.sprite_height, Player2=True, alt_color=gene2.alt_color)

        print('loading background...')
        background = Background('../res/Background/Bckgrnd0.png')

        print('creating game...')
        game = Game(screen, background, player1, player2)
        pygame.display.set_caption('Gene{}: {}     VS     Gene{}: {}'.format(gene1.index_in_population, gene1.color_name, gene2.index_in_population, gene2.color_name))
        game.mainloop(bot1, bot2)
        gene1.score = bot1.score
        gene2.score = bot2.score
        print('Gene{}: {}     VS     Gene{}: {} finished'.format(gene1.index_in_population, gene1.color_name, gene2.index_in_population, gene2.color_name))
        if output:
            output.put([
            {'gene_number': gene1.index_in_population, 'score': bot1.score},
            {'gene_number': gene2.index_in_population, 'score': bot2.score}
            ])


    def play_genes(self):
        output = mp.Queue()
        # Setup a list of processes that we want to run
        indexes_list = list(range(self.nb_gene))
        random.shuffle(indexes_list)
        processes = [mp.Process(target=self.play_round, args=(self.genes[indexes_list[2*i]], self.genes[indexes_list[2*i+1]], output, i)) for i in range(int(self.nb_gene/2))]
        # Run processes
        for p in processes:
            p.start()
        # Exit the completed processes
        for p in processes:
            p.join()
            print('Process finished')
        print('All processes finished')
        # Get process results from the output queue
        results = [output.get() for p in processes]
        return results


    def play_round_against_random(self, gene1, output, process_index):
        window_position = [((process_index%3)*600)%1920, ((process_index//3)*300)%1080]
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(window_position[0]) + "," + str(window_position[1])
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((320, 240), 0, 32)

        print('loading characters...')
        bot1 = Internal_bot(1, gene1.neural_net)
        player1 = Player(gene1.file, gene1.sprite_width, gene1.sprite_height, Player2=False, alt_color=gene1.alt_color)
        gene2 = self.generate_random_gene(0, list(colors)[444])
        bot2 = Internal_bot(2, gene2.neural_net)
        player2 = Player(gene2.file, gene2.sprite_width, gene2.sprite_height, Player2=True, alt_color=gene2.alt_color)

        print('loading background...')
        background = Background('../res/Background/Bckgrnd0.png')

        print('creating game...')
        game = Game(screen, background, player1, player2)
        pygame.display.set_caption('Gene{}: {}     VS     Gene{}: {}'.format(gene1.index_in_population, gene1.color_name, gene2.index_in_population, gene2.color_name))
        game.mainloop(bot1, bot2)
        gene1.score = bot1.score
        gene2.score = bot2.score
        print('Gene{}: {}     VS     Gene{}: {} finished'.format(gene1.index_in_population, gene1.color_name, gene2.index_in_population, gene2.color_name))
        if output:
            output.put([
            {'gene_number': gene1.index_in_population, 'score': bot1.score}
            ])


    def play_genes_against_random(self):
        output = mp.Queue()
        # Setup a list of processes that we want to run
        processes = [mp.Process(target=self.play_round_against_random, args=(self.genes[i], output, i)) for i in range(self.nb_gene)]
        # Run processes
        for p in processes:
            p.start()
        # Exit the completed processes
        for p in processes:
            p.join()
            print('Process finished')
        print('All processes finished')
        # Get process results from the output queue
        results = [output.get() for p in processes]
        return results


    def construct_gene_dic(self, index):
        # Construct a dict with the info of the gene
        gene_to_save = self.genes[index]
        gene_dic = {}
        gene_dic['file'] = gene_to_save.file
        gene_dic['sprite_width'] = gene_to_save.sprite_width
        gene_dic['sprite_height'] = gene_to_save.sprite_height
        gene_dic['index_in_population'] = gene_to_save.index_in_population
        gene_dic['color_name'] = gene_to_save.color_name
        gene_dic['population_number'] = gene_to_save.population_number
        ## Construct a dict with the info of the neural net
        neural_net_to_save = gene_to_save.neural_net
        neural_net_dic = {}
        neural_net_dic['input_length'] = neural_net_to_save.input_length
        neural_net_dic['output_length'] = neural_net_to_save.output_length
        neural_net_dic['nb_hidden_layers'] = neural_net_to_save.nb_hidden_layers
        neural_net_dic['hidden_layers_length'] = neural_net_to_save.hidden_layers_length
        neural_net_dic['hidden_layers'] = []
        for layer in neural_net_to_save.hidden_layers:
            tmp_layer = {}
            tmp_layer['weights'] = np.copy(layer['weights'])
            tmp_layer['bias'] = np.copy(layer['bias'])
            neural_net_dic['hidden_layers'].append(tmp_layer)
        # Add neural net infos to the gene_dic
        gene_dic['neural_net'] = neural_net_dic
        # Transform arrays of the neural net in lists so that it can be read as a json further on
        for obj in neural_net_dic['hidden_layers']:
            for key in obj:
                obj[key] = obj[key].tolist()
        return gene_dic


    def save_one_gene(self, index, dir='GeneSaved', base_name='Gene'):
        '''
            Save the gene indexed by index in self.genes
        '''
        # Construct a dict with the info of the gene
        gene_dic = self.construct_gene_dic(index)
        # Create directory if non existant yet
        dir_path = os.path.join('..',dir)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        # Write all this in a json file
        with open(os.path.join(dir_path,'{}{}.json').format(base_name, index), 'w') as f:
            json.dump(gene_dic, f)
        print('{}{} has been saved'.format(base_name, index))


    def save_all_genes(self, dir='PopulationSaved', base_name='Gene'):
        '''
            Save the genes in current population
        '''
        for index in range(len(self.genes)):
            self.save_one_gene(index, dir, base_name)
        dir_path = os.path.join('..',dir)
        with open(os.path.join(dir_path, 'Genes.txt'), 'w') as f:
            f.write(str(self.genes))

    def load_one_gene(self, index, dir='PopulationSaved', base_name='Gene'):
        '''
            Load a saved gene
        '''
        path = os.path.join('..',dir,'{}{}.json').format(base_name, index)
        # Load the json file containing the gene infos
        with open(path) as json_file:
            gene_dic = json.load(json_file)
        # Transform the lists corresponding to the hidden layers into np arrays
        for obj in gene_dic['neural_net']['hidden_layers']:
            for key in obj:
                obj[key] = np.asarray(obj[key])
        # Create a gene based on the loaded infos
        loaded_neural_net = simplest_neural_net_ever(
            input_length = gene_dic['neural_net']['input_length'],
            output_length = gene_dic['neural_net']['output_length'],
            nb_hidden_layers = gene_dic['neural_net']['nb_hidden_layers'],
            hidden_layers_length = gene_dic['neural_net']['hidden_layers_length'],
            hidden_layers = gene_dic['neural_net']['hidden_layers']
        )
        loaded_gene = Gene(
            file = gene_dic['file'],
            sprite_width = gene_dic['sprite_width'],
            sprite_height = gene_dic['sprite_height'],
            neural_net = loaded_neural_net,
            index_in_population = gene_dic['index_in_population'],
            color_name = gene_dic['color_name'],
            population_number = gene_dic['population_number']
        )
        print('{}{} has been loaded'.format(base_name, index))
        return loaded_gene


    def load_all_genes(self, dir='PopulationSaved', base_name='Gene'):
        for index in range(self.nb_gene):
            gene = self.load_one_gene(index, dir, base_name).copy()
            self.genes[index] = gene
        self.population_number = self.genes[0].population_number


    def roughly_sort_genes(self):
        for i in range(len(self.genes)):
            self.genes[i].score = 1000 - 50*i




def test_gene_savin_n_loadin(pop):
    pop.save_one_gene(-1, 0, base_name='test')
    loaded_gene = pop.load_one_gene(-1, 'GeneSaved', 'test')
    n = len(pop.genes[-1].neural_net.hidden_layers)
    print('weights shape  ', [loaded_gene.neural_net.hidden_layers[i]['weights'].shape == pop.genes[-1].neural_net.hidden_layers[i]['weights'].shape for i in range(n)])
    print('bias shape  ', [loaded_gene.neural_net.hidden_layers[i]['bias'].shape == pop.genes[-1].neural_net.hidden_layers[i]['bias'].shape for i in range(n)])
    print('weights content  ', [loaded_gene.neural_net.hidden_layers[i]['weights'] == pop.genes[-1].neural_net.hidden_layers[i]['weights'] for i in range(n)])
    print('bias content  ', [loaded_gene.neural_net.hidden_layers[i]['bias'] == pop.genes[-1].neural_net.hidden_layers[i]['bias'] for i in range(n)])


def test_round(output):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((320, 240), 0, 32)
    pygame.display.set_caption("Test") # program title

    print('loading characters...')
    gene1 = Gene(Player('Ken', 120, 100), Internal_bot(1, simplest_neural_net_ever()))
    gene2 = Gene(Player('Rick', 120, 100, Player2=True), Internal_bot(2, simplest_neural_net_ever()))

    print('loading background...')
    background = Background('../res/Background/Bckgrnd0.png')

    print('creating game...')
    game = Game(screen, background, 1, 2)
    game.mainloop(gene1.bot, gene2.bot)
    if output:
        output.put([gene1.bot.result, gene2.bot.result])

def test_processes():
    output = mp.Queue()
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=test_round, args=(output,)) for x in range(4)]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    results = [output.get() for p in processes]

    print(results)
    return 0

if __name__ == '__main__':
    '''
    start_time = time.time()
    pop_length = 2
    nb_generation = 400
    pop = Population(pop_length)

    results = pop.play_genes()
    print(results)
    '''
    start_time = time.time()
    pop_length = 12
    nb_generation = 400
    pop = Population(pop_length)

    pop.load_all_genes(dir="PopulationSavedAgainstRandom")
    #pop.roughly_sort_genes()

    for i in range(nb_generation):
        results = pop.play_genes_against_random()
        pop.evolve(results)
        print('Population {} over\n'.format(pop.population_number))
        print('Saving population\n')
        pop.save_all_genes(dir="PopulationSavedAgainstRandom")
        print('Population {} has been saved\n\n\n\n'.format(pop.population_number))
    print('All populations over\n\n')

    print('Saving the best gene')
    pop.save_one_gene(0, base_name='best_after_{}_generations_Gene'.format(pop.population_number))

    duration = (time.time() - start_time)/60
    print('\n\nTraining finished! ', "And it took ", duration, " minutes", '\n\n\nHave fun bro\' ;-)')
