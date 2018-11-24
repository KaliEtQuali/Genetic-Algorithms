import cv2
import os
import random
import copy
import numpy as np
from color_constants import colors

image_path = '/home/jrl/Street pyghter/res/Char/Ken/Ken.png'
output_dir = '/home/jrl/Street pyghter/res/Char/Ken/KenClones2'
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)



def choose_random_color_with_name():
    color = random.choice(list(colors.items()))
    b = color[1].blue
    g = color[1].green
    r = color[1].red
    colorname = color[0]
    return r, g, b, colorname

def generate_sprite(nb_sprites):
    if not os.path.exists(output_dir):
      os.mkdir(output_dir)
    for nb_clone in range(nb_sprites):
        print('Clone n°{} in process'.format(nb_clone))
        clone = copy.copy(image)
        r,g,b,colorname = choose_random_color_with_name()
        while os.path.exists(os.path.join(output_dir, 'KenClone-{}.png'.format(colorname))):
            r,g,b,colorname = choose_random_color_with_name()
        for i in range(len(clone)):
            for j in range(len(clone[0])):
                if clone[i][j][2] == 247 and clone[i][j][1] == 66 and clone[i][j][0] == 0:
                    clone[i][j] = np.array([b, g, r, clone[i][j][3]])
        cv2.imwrite(os.path.join(output_dir, 'KenClone-{}.png'.format(colorname)), clone)
        print('Clone n°{} achieved with color {}\n'.format(nb_clone, colorname))

def generate_all_sprites():
    if not os.path.exists(output_dir):
      os.mkdir(output_dir)
    nb_clone = 0
    for color in list(colors.items()):
        nb_clone += 1
        print('Clone n°{} in process'.format(nb_clone))
        clone = copy.copy(image)
        b = color[1].blue
        g = color[1].green
        r = color[1].red
        colorname = color[0]
        if not os.path.exists(os.path.join(output_dir, 'KenClone-{}.png'.format(colorname))):
            for i in range(len(clone)):
                for j in range(len(clone[0])):
                    if clone[i][j][2] == 247 and clone[i][j][1] == 66 and clone[i][j][0] == 0:
                        clone[i][j] = np.array([b, g, r, clone[i][j][3]])
            cv2.imwrite(os.path.join(output_dir, 'KenClone-{}.png'.format(colorname)), clone)
            print('Clone n°{} achieved with color {}\n'.format(nb_clone, colorname))
        else:
            print('Clone n°{} already done with color {}\n'.format(nb_clone, colorname))




generate_all_sprites()
