import random
import numpy as np
from math import floor
from color_constants import colors

def ko(list):
    li = list[:3]
    li[0] = 0
    return li

def ismember(A, B):
    return np.sum([ a == B for a in A ])

if __name__ == '__main__':
    n = 8
    print('40%: ', floor(n*40/100))
    print('30%: ', floor(n*30/100))
    print('20%: ', floor(n*20/100))
    print('10%: ', floor(n*10/100))
    l = [0,40,5,3,4,5,3,8]
    print(ismember(l, 1))
    print(ismember(l, 4))
    if ismember(l,1):
        print('ok')
    print(list(range(7)))
    x = list(range(7))
    random.shuffle(x)
    print(x)
