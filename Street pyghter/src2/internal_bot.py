#!/usr/bin/python3
import sys
import time
import random
import pygame
from pygame.locals import *

class Internal_bot:
    def __init__(self,player, neural_net):
        self.player = player
        self.score = 0
        if int(player) == 1:
            self.jump=K_UP
            self.down=K_DOWN
            self.right=K_RIGHT
            self.left=K_LEFT
            self.light=K_c
            self.medium=K_v
            self.special=K_b
        else:
            self.jump=K_i
            self.down=K_k
            self.right=K_l
            self.left=K_j
            self.light=K_q
            self.medium=K_w
            self.special=K_e
        self.selector = [self.jump, self.down, self.left, self.right, self.light, self.medium, self.special, 'hadoken', 'shoryuken']
        self.actions = ['jump', 'down', 'left', 'right', 'light', 'medium', 'special', 'hadoken', 'shoryuken']
        self.result = 'Player {}: {}'
        self.neural_net = neural_net
        #self.neural_net.random_initialize()
        #Do here all you need to load and prepare your bot


    def press_key(self, key):
        event = pygame.event.Event(KEYDOWN, key=key)
        pygame.event.post(event)


    def release_key(self, key):
        event = pygame.event.Event(KEYUP, key=key)
        pygame.event.post(event)


    def tap_key(self, key):
        self.press_key(key)
        #time.sleep(0.03)
        #self.release_key(key)


    def hadoken(self, is_facing_right=True):
        if is_facing_right:
            self.tap_key(self.down)
            self.tap_key(self.right)
            self.tap_key(self.light)
        else:
            self.tap_key(self.down)
            self.tap_key(self.left)
            self.tap_key(self.light)


    def shoryuken(self, is_facing_right=True):
        if is_facing_right:
            self.tap_key(self.right)
            self.tap_key(self.down)
            self.tap_key(self.right)
            self.tap_key(self.medium)
        else:
            self.tap_key(self.left)
            self.tap_key(self.down)
            self.tap_key(self.left)
            self.tap_key(self.medium)


    def random_stuff(self, game_info):
        ###Do your stuff here
        if round(random.random())==1:
            self.press_key(self.light)
        else:
            self.release_key(self.light)

        if round(random.random())==1:
            self.press_key(self.medium)
        else:
            self.release_key(self.medium)

        if round(random.random())==1:
            self.press_key(self.special)
        else:
            self.release_key(self.special)

        if round(random.random())==1:
            self.press_key(self.jump)
        else:
            self.release_key(self.jump)

        if round(random.random())==1:
            self.press_key(self.left)
        else:
            self.release_key(self.left)

        if round(random.random())==1:
            self.press_key(self.right)
        else:
            self.release_key(self.right)

        if round(random.random())==1:
            self.press_key(self.down)
        else:
            self.release_key(self.down)


    def nn_stuff(self, game_info):
        res = self.neural_net.feed_forward(game_info)
        self.chose_action(res[0])
        #print("res  {}".format(self.player), res)


    def do_action(self, action):
        if action == 'hadoken':
            self.hadoken()
        elif action == 'shoryuken':
            self.shoryuken()
        else:
            self.tap_key(action)


    def undo_action(self, action):
        if action != 'hadoken' and action != 'shoryuken':
            self.release_key(action)


    def test_hit(self, key):
        event = pygame.event.Event(KEYDOWN, key=key)
        pygame.event.post(event)
        event = pygame.event.Event(KEYDOWN, key=key)
        pygame.event.post(event)


    def chose_action(self, nn_output):
        monitor = ['player{}'.format(self.player)]
        for i in range(len(nn_output)):
            if nn_output[i] > 0.7:
                self.do_action(self.selector[i])
                monitor.append(self.actions[i])
        #print(monitor)

    def compute_score(self, game_info, result):
        if self.player == 1:
            health_difference = game_info[1] - game_info[9]
            energy_difference = game_info[2] - game_info[10]
            health = game_info[1]
        else:
            health_difference = game_info[9] - game_info[1]
            energy_difference = game_info[10] - game_info[2]
            health = game_info[9]
        return 10*(health_difference)*(game_info[0] + 1) + energy_difference + 5*health

    def round_over(self, game_info, round_marker):
        if round_marker[self.player - 1]:
            self.result = self.result.format(self.player, 'win')
            self.score = self.compute_score(game_info, 'win')
        else:
            self.result = self.result.format(self.player, 'lose')
            self.score = self.compute_score(game_info, 'lose')
        self.tap_key(self.light)


if __name__=="__main__":
    print("J'avoue j'ai encore rien mis ici pour le moment")
