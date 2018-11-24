from pynput.keyboard import Key, Controller, KeyCode
import time

KEYS = {
    'up': Key.up,
    'down': Key.down,
    'left': Key.left,
    'right': Key.right,
    'jab': KeyCode.from_char('c'),
    'strong_attack': KeyCode.from_char('v'),
    'teleport': KeyCode.from_char('b')
}

keyboard = Controller()

def press_key(key):
    keyboard.press(KEYS[key])

def release_key(key):
    keyboard.release(KEYS[key])

def tap_key(key):
    press_key(key)
    time.sleep(0.03)
    release_key(key)

def hadoken(is_facing_right):
    if is_facing_right:
        tap_key('down')
        tap_key('right')
        tap_key('jab')
    else:
        tap_key('down')
        tap_key('left')
        tap_key('jab')

def shoryuken(is_facing_right):
    if is_facing_right:
        tap_key('right')
        tap_key('down')
        tap_key('right')
        tap_key('strong_attack')
    else:
        tap_key('left')
        tap_key('down')
        tap_key('left')
        tap_key('strong_attack')


if __name__ == '__main__':
    for i in list(range(2))[::-1]:
        print(i+1)
        time.sleep(1)

    shoryuken(True)
