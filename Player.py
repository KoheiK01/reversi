import random


class player:

    # novoc用の属性
    name = "anonymous"
    if random.choice([True, False]):
        color = "black"
        is_black = True
        is_white = False
    else:
        color = "white"
        is_black = False
        is_white = True

    color = "black"
    is_black = True
    is_white = False

    def debug(*args):
        print(*args)
