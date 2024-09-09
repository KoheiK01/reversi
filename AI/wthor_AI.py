import random
from Player import player
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np


def next(board):
    """次に置く石の場所を決定する"""

    class Bias(keras.layers.Layer):
        def __init__(self, input_shape, **kwargs):
            super(Bias, self).__init__(**kwargs)  # 親クラスのコンストラクタを呼び出す
            self.W = tf.Variable(initial_value=tf.zeros(input_shape[1:]), trainable=True)

        def call(self, inputs):
            return inputs + self.W

    # カスタムレイヤーを登録してモデルをロード
    with keras.utils.custom_object_scope({'Bias': Bias}):
        model = load_model('AI/wthor_model/model.h5')

    legal = board.legal(player.color)
    black_disc = board.black_disc
    white_disc = board.white_disc

    x = np.array([black_disc, white_disc], dtype=np.int8)
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)
    sorted_predictions = np.argsort(predictions)[0][::-1]

    for i in sorted_predictions:
        row_index = int(i) // 8
        col_index = int(i) % 8
        move = (col_index, row_index)
        if move in legal:
            return move
