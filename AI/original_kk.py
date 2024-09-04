from Player import player

size = 8
corners = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
xs = [(1, 1), (1, size - 2), (size - 2, 1), (size - 2, size - 2)]

cs = [
    (0, 1), (1, 0),
    (0, size - 2), (1, size - 1),
    (size - 2, 0), (size - 1, 1),
    (size - 2, size - 1), (size - 1, size - 2)
]

corner_nears = xs + cs

corner_x_offsets = {
    corners[0]: xs[0],
    corners[1]: xs[1],
    corners[2]: xs[2],
    corners[3]: xs[3],
}

left_edge = [(0, i) for i in range(1, size)]
rev_left_edge = [(0, i) for i in range(size - 2, -1, -1)]
top_edge = [(i, 0) for i in range(1, size)]
rev_top_edge = [(i, 0) for i in range(size - 2, -1, -1)]
right_edge = [(size - 1, i) for i in range(1, size)]
rev_right_edge = [(size - 1, i) for i in range(size - 2, -1, -1)]
bottom_edge = [(i, size - 1) for i in range(1, size)]
rev_bottom_edge = [(i, size - 1) for i in range(size - 2, -1, -1)]


corner_edge_offsets = {
    corners[0]: (left_edge, top_edge),
    corners[1]: (rev_left_edge, bottom_edge),
    corners[2]: (rev_top_edge, right_edge),
    corners[3]: (rev_bottom_edge, rev_right_edge),
}


surroundings = [
    (dx, dy)
    for dx in [-1, 0, 1]
    for dy in [-1, 0, 1]
    if dx != 0 or dy != 0
]


def next(board):
    """次に置く石の座標を決定する

    Args:
        board (object): 盤面の情報を持つオブジェクト

    Returns:
        tuple: 次に置く石の座標(x, y)
    """
    # プレイヤーの色や相手の色、プレイヤーが置くことができる座標を取得
    pl_color = player.color
    op_color = "white" if player.is_black else "black"
    pl_legal = board.legal(pl_color)

    # 残り8手は全探索する
    if (board.black_score + board.white_score >= size * size - 8):
        best_move = endgame_serch(board, pl_legal, pl_color, op_color)
        return best_move

    # 隅を持っているならばX打ち，やすり攻めを優先的に行う
    taked_corners = find_taked_corners(board, pl_color)
    if taked_corners:
        best_move = choose_move_with_corners(
            board, taked_corners, pl_color, pl_legal, op_color)
        if best_move:
            return best_move

    # 通常の次の手を計算
    best_move = choose_standard_move(board, pl_color, pl_legal, op_color)
    return best_move


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


def find_taked_corners(board, color):
    """現在持っている隅を調べる
    """
    pl_color_check = 1 if color == "black" else -1
    disc = board.disc

    taked_corners = []
    for corner in corners:
        if disc[corner[1]][corner[0]] == pl_color_check:
            taked_corners.append(corner)
    return taked_corners


def choose_move_with_corners(board, taked_corners, pl_color, pl_legal, op_color):
    """隅を持っている場合の次の手を選ぶ
    """
    # 隅の周りに置けるXの座標を見つける
    put_x_position = find_put_x_position(
        board, taked_corners, pl_color, pl_legal, op_color)
    if put_x_position:
        return put_x_position

    # 辺に隣接する確定石の場所を探す
    edge_stable_position = find_put_edge_stable_position(
        board, taked_corners, pl_color, pl_legal, op_color)
    if edge_stable_position:
        return edge_stable_position

    # その他の良い手がない場合は通常の一手
    return choose_standard_move(board, pl_color, pl_legal, op_color)


def find_put_x_position(board, taked_corners, pl_color, pl_legal, op_color):
    """隅の周りに置けるXの座標を見つける
    """
    for taked_corner in taked_corners:
        taked_corner_x = corner_x_offsets[taked_corner]
        if taked_corner_x in pl_legal:
            board.put_disc(pl_color, taked_corner_x[0], taked_corner_x[1])
            op_legal = board.legal(op_color)
            board.undo()
            if not any(op_move in corners for op_move in op_legal):
                return taked_corner_x
    return None


def find_put_edge_stable_position(board, taked_corners, pl_color, pl_legal, op_color):
    """隅からやすり攻めできる場所を探す
    """
    disc = board.disc
    for taked_corner in taked_corners:
        for edges in corner_edge_offsets[taked_corner]:
            for move in edges:
                if disc[move[1]][move[0]] == 0:
                    if move in pl_legal:
                        board.put_disc(pl_color, move[0], move[1])
                        op_legal = board.legal(op_color)
                        board.undo()
                        if not any(op_move in corners for op_move in op_legal):
                            return move
                        player.debug("move =>", move, "やすり攻めして隅とられたらダメ！")
                    break
    return None


def choose_standard_move(board, pl_color, pl_legal, op_color):
    """隅をとっていない場合の標準的な次の手を選び方
    """
    # 隅に置けるならば置く
    put_corner = find_put_corner(pl_legal)
    if put_corner:
        return put_corner

    # 開放度が低い 相手の置ける場所を最小 自分の置ける場所を最大
    degrees = cal_degrees(board, pl_color, pl_legal)
    best_move = find_min_max_put(board, pl_color, pl_legal, op_color, degrees)
    return best_move


def cal_degrees(board, pl_color, pl_legal):
    """ 開放度を計算する
    """
    open_degrees = []
    for move in pl_legal:
        open_degree = 0
        disc = board.disc
        put_disc = board.put_disc(pl_color, move[0], move[1])

        for change in put_disc:
            for dx, dy in surroundings:
                nx, ny = change[0] + dx, change[1] + dy
                if 0 <= nx < size and 0 <= ny < size and disc[ny][nx] == 0:
                    disc[ny][nx] = 2
                    open_degree += 1
        open_degrees.append(open_degree)
        board.undo()
    return open_degrees


def find_min_max_put(board, pl_color, pl_legal, op_color, degrees):
    """相手の置ける場所を最小にし、自分の置ける場所を最大にする
    """
    best_move = pl_legal[0]
    op_min_priority = size * size
    index = 0
    for move in pl_legal:
        open_degree = degrees[index]
        index += 1

        # 隅の周りには普通は置かないけども、相手が隅をもっているならば、X打ちする
        if move in corner_nears:
            """taked_corners = find_taked_corners(board, op_color)
            if taked_corners:
                best_move = find_put_x_position(
                    board, taked_corners, pl_color, pl_legal, op_color)
                if best_move:
                    return best_move
                    """
            continue

        board.put_disc(pl_color, move[0], move[1])
        op_legal = board.legal(op_color)

        # 相手に隅をとられてしまうならばそれは悪手である．
        if any(op_move in corners for op_move in op_legal):
            player.debug("相手に隅をとられてしまうならばそれは悪手である．", move)
            board.undo()
            continue

        # 自分がmoveに置いた時、相手は最善の一手を打つと仮定するのでそれを求める
        # 最善手 = 自分の置ける石 - 相手の置ける石が最も大きくなる一手 + 開放度
        op_max_priority = -size * size
        for op_move in op_legal:
            board.put_disc(op_color, op_move[0], op_move[1])
            pl_new_len = cal_put_count(board.legal(pl_color))
            op_new_len = cal_put_count(board.legal(op_color))
            op_priority = op_new_len - pl_new_len + open_degree
            if (op_priority > op_max_priority):
                op_max_priority = op_priority
            board.undo()

        # moveと置いた時に相手が最善の一手を打つとする場合に，
        # 相手の優先度が最も低くなる一手にする．
        if (op_max_priority < op_min_priority):
            op_min_priority = op_max_priority
            best_move = move
        board.undo()

    return best_move


def cal_put_count(legal):
    """隅の周りを除いた置ける座標の数を求める
    """
    put_count = len(legal)
    put_count -= sum(move in corner_nears for move in legal)
    return put_count


def find_put_corner(legal):
    """置ける隅の座標を見つける
    """
    for move in legal:
        if move in corners:
            return move

    return None
