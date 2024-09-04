import random
from Player import player


def next(board):
    """次に置く石の場所を決定する"""

    legal = board.legal(player.color)
    return random.choice(legal)
