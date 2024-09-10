class Screen:
    """スクリーンの設定"""

    # 縦
    BASE_HEIGHT = 800
    SCORE_HEIGHT = 100
    OPTION_HEIGHT = 100
    HEIGHT = BASE_HEIGHT + SCORE_HEIGHT + OPTION_HEIGHT

    # 横
    BASE_WIDTH = 800
    MARGIN_WIDTH = 100  # きちきちすぎると違和感がある．
    WIDTH = BASE_WIDTH + MARGIN_WIDTH

    # StartX,Y
    START_X = MARGIN_WIDTH // 2
    START_Y = SCORE_HEIGHT
    CENTER_X = WIDTH // 2
    CENTER_Y = HEIGHT // 2
