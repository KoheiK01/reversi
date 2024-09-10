import requests
from Player import player
import tensorflow as tf
import numpy as np

size = 8
model = None


def next(board):
    """次に置く石の場所を決定する"""

    global model

    class Bias(tf.keras.layers.Layer):
        def __init__(self, input_shape, **kwargs):
            super(Bias, self).__init__(**kwargs)  # 親クラスのコンストラクタを呼び出す
            self.W = tf.Variable(initial_value=tf.zeros(input_shape[1:]), trainable=True)

        def call(self, inputs):
            return inputs + self.W

    # 残り8手は全探索する
    if (board.black_score + board.white_score >= size * size - 8):
        # プレイヤーの色や相手の色、プレイヤーが置くことができる座標を取得
        pl_color = player.color
        op_color = "white" if player.is_black else "black"
        pl_legal = board.legal(pl_color)
        best_move = endgame_serch(board, pl_legal, pl_color, op_color)
        return best_move

    # if not model:
    #     url = 'https://github.com/KoheiK01/reversi/raw/master/AI/wthor_model/model.h5'
    #     response = requests.get(url)
    #     with open('model.h5', 'wb') as f:
    #         f.write(response.content)
    #     with tf.keras.utils.custom_object_scope({'Bias': Bias}):
    #         model = tf.keras.models.load_model('model.h5')

    if not model:
        with tf.keras.utils.custom_object_scope({'Bias': Bias}):
            model = tf.keras.models.load_model('AI/wthor_model/all_model.h5')

    legal = board.legal(player.color)
    black_disc = board.black_disc
    white_disc = board.white_disc

    if player.color == "black":
        x = np.array([black_disc, white_disc], dtype=np.int8)
    else:
        x = np.array([white_disc, black_disc], dtype=np.int8)
    x = np.expand_dims(x, axis=0)

    predictions = model.predict(x)
    sorted_predictions = np.argsort(predictions)[0][::-1]

    for i in sorted_predictions:
        row_index = int(i) // 8
        col_index = int(i) % 8
        move = (col_index, row_index)
        if move in legal:
            return move


def endgame_serch(board, pl_legal, pl_color, op_color):
    max_score = -size * size
    for move in pl_legal:
        board.put_disc(pl_color, move[0], move[1])
        next_legal = board.legal(op_color)
        score = exhaustive_search(board, next_legal, op_color)
        player.debug("move =>", move, "score= >", score)
        if (score > max_score):
            max_score = score
            best_move = move
        board.undo()
    return best_move


def exhaustive_search(board, legal, color):
    if not legal:
        next_color = "white" if color == "black" else "black"
        next_legal = board.legal(next_color)
        if not next_legal:
            return board.black_score - board.white_score if player.is_black else board.white_score - board.black_score
        else:
            return exhaustive_search(board, next_legal, next_color)

    max_score = -size * size
    min_score = size * size
    for move in legal:
        board.put_disc(color, move[0], move[1])
        next_color = "white" if color == "black" else "black"
        next_legal = board.legal(next_color)
        score = exhaustive_search(board, next_legal, next_color)
        board.undo()
        if player.color == color:
            max_score = max(max_score, score)
        else:
            min_score = min(min_score, score)
    return max_score if player.color == color else min_score
