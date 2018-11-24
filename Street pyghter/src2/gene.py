import numpy as np
import cv2
import os
import copy
from color_constants import colors

def generate_sprite(colorname):
    print('\nCreating a new sprite of color {}'.format(rgb))
    image_path = '/home/jrl/Street pyghter/res/Char/Ken/Ken.png'
    output_dir = '/home/jrl/Street pyghter/res/Char/Ken/KenChildClones'
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    clone = copy.copy(image)
    color = colors[colorname]
    b = color.blue
    g = color.green
    r = color.red
    for i in range(len(clone)):
        for j in range(len(clone[0])):
            if clone[i][j][2] == 247 and clone[i][j][1] == 66 and clone[i][j][0] == 0:
                clone[i][j] = np.array([b, g, r, clone[i][j][3]])
    cv2.imwrite(os.path.join(output_dir, 'KenClone-{}.png'.format(colorname)), clone)
    print('Sprite created \n')
    return 'KenClone-{}'.format(colorname)


class Gene:
    def __init__(self, file, sprite_width, sprite_height, neural_net, index_in_population, color_name='darkorchid4', population_number=0):
        self.file = file
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.color_name = color_name
        self.alt_color = 'Clones/KenClone-{}'.format(color_name)
        self.neural_net = neural_net
        self.index_in_population = index_in_population
        self.population_number = population_number
        self.score = 0

    def __repr__(self, short=True):
        if short:
            return 'Index in population: {}      Sprite: {}\n     Score: {}\n     Population: {}\n    Color: {}\n'.format(self.index_in_population, self.alt_color, self.score, self.population_number, self.color_name)


    def copy(self):
        out = Gene(self.file, self.sprite_width, self.sprite_height, self.neural_net.copy(), self.index_in_population, self.color_name, self.population_number)
        out.score = self.score
        return out
