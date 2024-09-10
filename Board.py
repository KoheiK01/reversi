class Board:
    """盤面変更用"""

    # マスの設定
    size = 8

    # novoc用属性
    disc = [[0] * 8 for _ in range(8)]
    white_disc = [[0] * 8 for _ in range(8)]
    white_disc_bit = 0
    white_score = 0
    black_disc = [[0] * 8 for _ in range(8)]
    black_disc_bit = 0
    black_score = 0

    # undo用
    black_disc_bit_list = []
    white_disc_bit_list = []

    # 関数--------------------------------------------------------------------------
    def __init__(self):
        """コンストラクタで盤面を初期化"""

        # 盤面（ビットボード）の初期化
        self.black_disc_bit = 0x0000000810000000        # 黒石
        self.white_disc_bit = 0x0000001008000000        # 白石

        # 盤面（ビットボード）の推移
        self.black_disc_bit_list = []  # 初期化
        self.white_disc_bit_list = []  # 初期化
        self.black_disc_bit_list.append(self.black_disc_bit)  # 履歴を更新する
        self.white_disc_bit_list.append(self.white_disc_bit)  # 履歴を更新する

        self.update_disc_ratio()  # discが更新されたときに呼び出す

    def put_disc(self, color, col_index, row_index):
        """石をひっくり返す"""

        legal_bit = self.legal_bit(color)  # 石を置ける場所の取得(bit)
        if 0 <= col_index < 8 and 0 <= row_index < 8:
            put_bit = 1 << (7 - row_index) * 8 + (7 - col_index)
            if put_bit & legal_bit:  # 有効手ならばひっくり返す
                flip_bit = self.flippable_disc_bit(color, put_bit)  # ひっくり返せる石を取得
                self.update_disc_bit(color, put_bit, flip_bit)  # 石をひっくり返す
                return self.bit_to_xy(flip_bit)

    def update_disc_bit(self, color, put_bit, flip_bit):
        """石をひっくり返す"""

        flip_bit |= put_bit
        if color == "black":
            self.black_disc_bit |= flip_bit
            self.white_disc_bit &= ~flip_bit
        else:
            self.white_disc_bit |= flip_bit
            self.black_disc_bit &= ~flip_bit

        self.black_disc_bit_list.append(self.black_disc_bit)  # 履歴を更新する
        self.white_disc_bit_list.append(self.white_disc_bit)  # 履歴を更新する
        self.update_disc_ratio()  # discが更新されたときに呼び出す

    def update_disc_ratio(self):
        """discが更新されたときに呼び出す"""

        self.update_disc()  # discを更新する
        self.black_score = self.count_score(self.black_disc_bit)  # 黒石の数を数える
        self.white_score = self.count_score(self.white_disc_bit)  # 白石の数を数える

    def undo(self):
        """1手戻る"""

        self.black_disc_bit_list = self.black_disc_bit_list[:-1]  # 最後の1つを削除
        self.white_disc_bit_list = self.white_disc_bit_list[:-1]
        self.black_disc_bit = self.black_disc_bit_list[-1]
        self.white_disc_bit = self.white_disc_bit_list[-1]
        self.update_disc_ratio()  # discが更新されたときに呼び出す

    def update_disc(self):
        """discを更新する"""

        self.disc = [[0] * 8 for _ in range(8)]
        self.black_disc = [[0] * 8 for _ in range(8)]
        self.white_disc = [[0] * 8 for _ in range(8)]

        for i in range(64):

            # ビットボードから行と列のインデックスを計算
            row_index = (i) // 8
            col_index = (i) % 8

            if (1 << (63 - i)) & self.black_disc_bit:
                self.disc[row_index][col_index] = 1  # 黒
                self.black_disc[row_index][col_index] = 1
                self.white_disc[row_index][col_index] = 0
            elif (1 << (63 - i)) & self.white_disc_bit:
                self.disc[row_index][col_index] = -1  # 白
                self.black_disc[row_index][col_index] = 0
                self.white_disc[row_index][col_index] = 1

    def count_score(self, disc_bit):
        """石の数を数える"""

        disc_bit = disc_bit - ((disc_bit >> 1) & 0x5555555555555555)
        disc_bit = (disc_bit & 0x3333333333333333) + ((disc_bit >> 2) & 0x3333333333333333)
        disc_bit = (disc_bit + (disc_bit >> 4)) & 0x0f0f0f0f0f0f0f0f
        disc_bit = disc_bit + (disc_bit >> 8)
        disc_bit = disc_bit + (disc_bit >> 16)
        disc_bit = disc_bit + (disc_bit >> 32)
        return disc_bit & 0x7f

    # 石を置ける場所の取得 --------------------------------------------------------
    def legal(self, color):
        """石を置ける場所の取得((x, y))"""

        legal_bit = self.legal_bit(color)
        return self.bit_to_xy(legal_bit)

    def legal_bit(self, color):
        """石を置ける場所の取得(bit)"""

        blank_bit, player_bit, opponent_bit = self.get_bit(color)
        op_h_masked, op_v_masked, op_all_masked = self.get_op_masked_bit(opponent_bit)

        # 各方向に対して合法手を探索
        legal_bit = self.legal_l(player_bit, op_all_masked, blank_bit, 9)  # 左上
        legal_bit |= self.legal_l(player_bit, op_v_masked, blank_bit, 8)  # 上
        legal_bit |= self.legal_l(player_bit, op_all_masked, blank_bit, 7)  # 右上
        legal_bit |= self.legal_l(player_bit, op_h_masked, blank_bit, 1)  # 左
        legal_bit |= self.legal_r(player_bit, op_h_masked, blank_bit, 1)  # 右
        legal_bit |= self.legal_r(player_bit, op_all_masked, blank_bit, 7)  # 左下
        legal_bit |= self.legal_r(player_bit, op_v_masked, blank_bit, 8)  # 下
        legal_bit |= self.legal_r(player_bit, op_all_masked, blank_bit, 9)  # 右下
        return legal_bit

    def legal_l(self, player_bit, op_masked_bit, blank_bit, shift):
        """左方向にシフトして合法手を探索"""

        tmp = (player_bit << shift) & op_masked_bit
        for _ in range(5):
            tmp |= (tmp << shift) & op_masked_bit
        legal_bit = (tmp << shift) & blank_bit
        return legal_bit

    def legal_r(self, player_bit, op_masked_bit, blank_bit, shift):
        """右方向にシフトして合法手を探索"""

        tmp = (player_bit >> shift) & op_masked_bit
        for _ in range(5):
            tmp |= (tmp >> shift) & op_masked_bit
        legal_bit = (tmp >> shift) & blank_bit
        return legal_bit
    # ------------------------------------------------------------------------------

    # ひっくり返せる石を取得 --------------------------------------------------------
    def flippable_disc_bit(self, color, put_bit):
        """ひっくり返せる石を取得"""

        _, player_bit, opponent_bit = self.get_bit(color)
        op_h_masked, op_v_masked, op_all_masked = self.get_op_masked_bit(opponent_bit)

        # 各方向に対してひっくり返る石を探索
        flip_bit = self.flip_l(player_bit, op_all_masked, put_bit, 9)  # 左上
        flip_bit |= self.flip_l(player_bit, op_v_masked, put_bit, 8)  # 上
        flip_bit |= self.flip_l(player_bit, op_all_masked, put_bit, 7)  # 右上
        flip_bit |= self.flip_l(player_bit, op_h_masked, put_bit, 1)  # 左
        flip_bit |= self.flip_r(player_bit, op_h_masked, put_bit, 1)  # 右
        flip_bit |= self.flip_r(player_bit, op_all_masked, put_bit, 7)  # 左下
        flip_bit |= self.flip_r(player_bit, op_v_masked, put_bit, 8)  # 下
        flip_bit |= self.flip_r(player_bit, op_all_masked, put_bit, 9)  # 右下
        return flip_bit

    def flip_l(self, player_bit, op_masked_bit, put_bit,  shift):
        """左方向にシフトしてひっくり返せる石を探索"""

        tmp = (put_bit << shift) & op_masked_bit
        flip_bit = tmp
        if flip_bit == 0:
            return 0
        for _ in range(6):
            tmp = tmp << shift
            if tmp & op_masked_bit == 0:  # 連続している相手の石はなくなった
                break
            else:
                flip_bit |= tmp

        if player_bit & tmp == 0:  # 自分の石がないならば挟めていない
            return 0
        else:
            return flip_bit

    def flip_r(self, player_bit, op_masked_bit, put_bit,  shift):
        """右方向にシフトしてひっくり返せる石を探索"""

        tmp = (put_bit >> shift) & op_masked_bit
        flip_bit = tmp
        if flip_bit == 0:
            return 0
        for _ in range(6):
            tmp = tmp >> shift
            if tmp & op_masked_bit == 0:  # 連続している相手の石はなくなった
                break
            else:
                flip_bit |= tmp

        if player_bit & tmp == 0:  # 自分の石がないならば挟めていない
            return 0
        else:
            return flip_bit
    # ------------------------------------------------------------------------------

    # 補助関数 ---------------------------------------------------------------------
    def get_bit(self, color):
        """指定された色に応じてビットボードをセット"""

        blank_bit = ~(self.black_disc_bit | self.white_disc_bit)  # 空きマスのビットボード
        if color == "black":
            player_bit = self.black_disc_bit
            opponent_bit = self.white_disc_bit
        else:
            player_bit = self.white_disc_bit
            opponent_bit = self.black_disc_bit
        return blank_bit, player_bit, opponent_bit

    def get_op_masked_bit(self, opponent_bit):
        """端と端がプログラム上つながるので、maskを設定"""

        horizontal_mask = 0x7e7e7e7e7e7e7e7e
        vertical_mask = 0x00ffffffffffff00
        allside_mask = 0x007e7e7e7e7e7e00

        op_horizontal_masked = opponent_bit & horizontal_mask  # 左右のマスク後
        op_vertical_masked = opponent_bit & vertical_mask  # 上下のマスク後
        op_allside_masked = opponent_bit & allside_mask  # 斜めのマスク後
        return op_horizontal_masked, op_vertical_masked, op_allside_masked

    def bit_to_xy(self, bit):
        xy = []
        for i in range(64):

            # ビットボードから行と列のインデックスを計算
            row_index = (i) // 8
            col_index = (i) % 8

            if (1 << 63 - i) & bit:
                xy.append((col_index, row_index))
        return xy
    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
