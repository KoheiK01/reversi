import pygame
from Color import Color
from Screen import Screen

pygame.init()


class Show:
    """表示用の設定"""

    # フォントの設定
    BASE_FONT = pygame.font.SysFont(None, 100)

    # 勝利表示
    x = Screen.CENTER_X
    y = Screen.HEIGHT // 3
    BLACK_WIN_SURFACE = BASE_FONT.render("Black Win!", False, Color.BLACK, Color.WHITE)
    WHITE_WIN_SURFACE = BASE_FONT.render("White Win!", False, Color.BLACK, Color.WHITE)
    DROW_SURFACE = BASE_FONT.render("drow", False, Color.BLACK, Color.WHITE)
    BLACK_WIN_RECT = BLACK_WIN_SURFACE.get_rect(center=(x, y))
    WHITE_WIN_RECT = WHITE_WIN_SURFACE.get_rect(center=(x, y))
    DROW_RECT = DROW_SURFACE.get_rect(center=(x, y))

    # ゲーム終了用
    x = Screen.CENTER_X
    y = Screen.HEIGHT // 3 * 2
    ONEMORE_SURFACE = BASE_FONT.render("Click here to start!", False, Color.BLACK, Color.WHITE)
    ONEMORE_RECT = ONEMORE_SURFACE.get_rect(center=(x, y))

    # 石のイラスト
    STONE_SIZE = 35
    BLACK_STONE_SURFACE = pygame.Surface((STONE_SIZE * 2, STONE_SIZE * 2), pygame.SRCALPHA)  # 透明なサーフェスを作成
    pygame.draw.circle(BLACK_STONE_SURFACE, Color.BLACK, (STONE_SIZE, STONE_SIZE), STONE_SIZE)
    WHITE_STONE_SURFACE = pygame.Surface((STONE_SIZE * 2, STONE_SIZE * 2), pygame.SRCALPHA)  # 透明なサーフェスを作成
    pygame.draw.circle(WHITE_STONE_SURFACE, Color.WHITE, (STONE_SIZE, STONE_SIZE), STONE_SIZE)

    # 待ったの設定
    REVERSE_FONT = pygame.font.SysFont(None, 50)
    x = 10
    y = Screen.START_Y + Screen.BASE_HEIGHT
    y += (Screen.START_Y - STONE_SIZE * 2) // 2
    WAIT_SURFACE = REVERSE_FONT.render("Wait", False, Color.BLACK, Color.LIGHT_GREEN)
    WAIT_RECT = WAIT_SURFACE.get_rect(topleft=(x, y))

    # ゲームやり直しの設定
    x = Screen.WIDTH - 10
    y = Screen.START_Y + Screen.BASE_HEIGHT
    y += (Screen.START_Y - STONE_SIZE * 2) // 2
    RESET_SURFACE = REVERSE_FONT.render("Reset", False, Color.BLACK, Color.LIGHT_GREEN)
    RESET_RECT = RESET_SURFACE.get_rect(topright=(x, y))

    # パスの設定
    x = Screen.CENTER_X
    y = Screen.CENTER_Y
    PASS_SURFACE = BASE_FONT.render("Pass", True, Color.BLACK, Color.GRAY)
    PASS_RECT = PASS_SURFACE.get_rect(center=(x, y))

    # start_menuの設定
    START_FONT = pygame.font.SysFont(None, 50)
    PVP_SURFACE = BASE_FONT.render("Two Player Game", False, Color.BLACK, Color.WHITE)  # 対人対戦画像
    PVC_SURFACE = BASE_FONT.render("Play Against CPU", False, Color.BLACK, Color.WHITE)  # CPU対戦画像
    PVP_RECT = PVP_SURFACE.get_rect(center=(Screen.WIDTH // 2, Screen.HEIGHT // 3))
    PVC_RECT = PVC_SURFACE.get_rect(center=(Screen.WIDTH // 2, Screen.HEIGHT // 2))
