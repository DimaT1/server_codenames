import constants
import random


def game_generator():
    with open(constants.words_source_csv, 'r') as fin:
        arr = [tuple(s.split(',')) for s in fin.read().split('\n')][:-1]
        random.shuffle(arr)
        red = arr[:8]
        blue = arr[8:17]
        white = arr[17:24]
        black = [arr[24]]

        red = list(map(lambda x: x[0] + '_' + x[1], red))
        blue = list(map(lambda x: x[0] + '_' + x[1], blue))
        white = list(map(lambda x: x[0] + '_' + x[1], white))
        black = list(map(lambda x: x[0] + '_' + x[1], black))

        return {
            "red": red,
            "blue": blue,
            "white": white,
            "black": black
        }
