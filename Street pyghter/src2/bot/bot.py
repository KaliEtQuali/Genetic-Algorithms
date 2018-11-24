#!/usr/bin/python3
import sys
import time
import socket
import pickle
from pynput.keyboard import Key, Controller
from neural_net import simplest_neural_net_ever
import random

hote = "localhost"

port = 12800


class Bot:
    def __init__(self,player, neural_net=simplest_neural_net_ever()):
        self.player = player
        self.pad = Controller()
        if int(player) == 1:
            self.jump=Key.up
            self.down=Key.down
            self.right=Key.right
            self.left=Key.left
            self.light='c'
            self.medium='v'
            self.special='b'
        else:
            self.jump='i'
            self.down='k'
            self.right='l'
            self.left='j'
            self.light='q'
            self.medium='w'
            self.special='e'
        self.selector = [self.jump, self.down, self.left, self.right, self.light, self.medium, self.special, 'hadoken', 'shoryuken']
        self.neural_net = neural_net
        self.neural_net.random_initialize()
        #Do here all you need to load and prepare your bot


    def connection(self, port):
        print("Try to connect...")
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
        	try:
        		self.server_connection.connect((hote, int(port)))
        		connected = True
        	except ConnectionRefusedError:
        		time.sleep(0.1)
        print("Connection OK")


    def start(self):
        cpt = 0
        game_info = pickle.loads(self.server_connection.recv(1024))
        while len(game_info) != 0:
            cpt += 1
            '''
            if len(game_info) < 3:
                if game_info[int(self.player)-1] == 1:
                    print("I win")
                else:
                    print("I lose")
                continue
            '''
            self.nn_stuff(game_info)
            #print("game_info ",game_info)
            game_info = pickle.loads(self.server_connection.recv(1024))
        self.server_connection.close()


    def press_key(self, key):
        self.pad.press(key)


    def release_key(self, key):
        self.pad.release(key)


    def tap_key(self, key):
        self.press_key(key)
        time.sleep(0.03)
        self.release_key(key)


    def hadoken(self, is_facing_right):
        if is_facing_right:
            tap_key(self.down)
            tap_key(self.right)
            tap_key(self.light)
        else:
            tap_key(self.down)
            tap_key(self.left)
            tap_key(self.light)


    def shoryuken(self, is_facing_right):
        if is_facing_right:
            tap_key(self.right)
            tap_key(self.down)
            tap_key(self.right)
            tap_key(self.medium)
        else:
            tap_key(self.left)
            tap_key(self.down)
            tap_key(self.left)
            tap_key(self.medium)


    def random_stuff(self, game_info):
        ###Do your stuff here
        if round(random.random())==1:
            self.pad.press(self.light)
        else:
            self.pad.release(self.light)

        if round(random.random())==1:
            self.pad.press(self.medium)
        else:
            self.pad.release(self.medium)

        if round(random.random())==1:
            self.pad.press(self.special)
        else:
            self.pad.release(self.special)

        if round(random.random())==1:
            self.pad.press(self.jump)
        else:
            self.pad.release(self.jump)

        if round(random.random())==1:
            self.pad.press(self.left)
        else:
            self.pad.release(self.left)

        if round(random.random())==1:
            self.pad.press(self.right)
        else:
            self.pad.release(self.right)

        if round(random.random())==1:
            self.pad.press(self.down)
        else:
            self.pad.release(self.down)


    def nn_stuff(self, game_info):
        res = self.neural_net.feed_forward(game_info)
        self.chose_action(res[0])
        #print("res  ", res)


    def do_action(self, action):
        if action == 'hadoken':
            self.hadoken()
        elif action == 'shoryuken':
            self.shoryuken()
        else:
            self.tap_key(action)


    def chose_action(self, nn_output):
        for i in range(len(self.selector)):
            if nn_output[i] > 0.7:
                self.do_action(self.selector[i])
                print('joueur: {} fait {}'.format(self.player, self.selector[i]))


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: bot.py <Player_num> <Port>")
        exit()
    bot = Bot(sys.argv[1])
    while True:
        bot.connection(sys.argv[2])
        bot.start()
