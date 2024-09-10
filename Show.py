import pygame
import pygame.gfxdraw
from Color import Color
from Screen import Screen

pygame.init()


class Show:
    """表示用の設定"""

    # フォント
    BIG_FONT = pygame.font.SysFont(None, 100)
    SMALL_FONT = pygame.font.SysFont(None, 50)

    # start_menuの設定
    # タイトル表示
    TITLE_IMAGE = pygame.image.load('image/title_reversi.jpg')
    TITLE_IMAGE = pygame.transform.scale(TITLE_IMAGE, (Screen.WIDTH, Screen.CENTER_Y * 2))
    # 対人対戦
    PVP_SURFACE = BIG_FONT.render("Two Player Game", False, Color.WHITE, Color.DARK_RED)
    PVP_RECT = PVP_SURFACE.get_rect(center=(Screen.CENTER_X, Screen.HEIGHT - Screen.HEIGHT // 3))
    # CPU対戦
    PVC_SURFACE = BIG_FONT.render("Play Against CPU", False, Color.WHITE, Color.DARK_RED)
    PVC_RECT = PVP_SURFACE.get_rect(center=(Screen.CENTER_X, Screen.HEIGHT - Screen.HEIGHT // 5))

    # 勝利表示
    x = Screen.CENTER_X
    y = Screen.HEIGHT // 3
    BLACK_WIN_SURFACE = BIG_FONT.render("Black Win!", False, Color.BLACK, Color.WHITE)
    BLACK_WIN_RECT = BLACK_WIN_SURFACE.get_rect(center=(x, y))
    WHITE_WIN_SURFACE = BIG_FONT.render("White Win!", False, Color.BLACK, Color.WHITE)
    WHITE_WIN_RECT = WHITE_WIN_SURFACE.get_rect(center=(x, y))
    DROW_SURFACE = BIG_FONT.render("drow", False, Color.BLACK, Color.WHITE)
    DROW_RECT = DROW_SURFACE.get_rect(center=(x, y))

    # ゲーム終了用
    x = Screen.CENTER_X
    y = Screen.HEIGHT // 3 * 2
    ONEMORE_SURFACE = BIG_FONT.render("Click here to start!", False, Color.BLACK, Color.WHITE)
    ONEMORE_RECT = ONEMORE_SURFACE.get_rect(center=(x, y))

    # 石のイラスト
    STONE_R = 35
    BLACK_STONE_SURFACE = pygame.Surface((STONE_R * 2, STONE_R * 2), pygame.SRCALPHA)  # 透明なサーフェスを作成
    pygame.gfxdraw.aacircle(BLACK_STONE_SURFACE, STONE_R, STONE_R, STONE_R, Color.BLACK)
    pygame.gfxdraw.filled_circle(BLACK_STONE_SURFACE,  STONE_R, STONE_R, STONE_R, Color.BLACK)
    WHITE_STONE_SURFACE = pygame.Surface((STONE_R * 2, STONE_R * 2), pygame.SRCALPHA)  # 透明なサーフェスを作成
    pygame.gfxdraw.aacircle(WHITE_STONE_SURFACE, STONE_R, STONE_R, STONE_R, Color.WHITE)
    pygame.gfxdraw.filled_circle(WHITE_STONE_SURFACE,  STONE_R, STONE_R, STONE_R, Color.WHITE)

    # オプション表示
    # 待ったの設定
    y = Screen.START_Y + Screen.BASE_HEIGHT
    y += Screen.OPTION_HEIGHT // 2 - STONE_R
    WAIT_SURFACE = SMALL_FONT.render("Wait", False, Color.BLACK, Color.LIGHT_GREEN)
    x = Screen.WIDTH // 4 - WAIT_SURFACE.get_width() // 2
    WAIT_RECT = WAIT_SURFACE.get_rect(topleft=(x, y))
    # ヒントの設定
    HINT_SURFACE = SMALL_FONT.render("Hint", False, Color.BLACK, Color.LIGHT_GREEN)
    x = Screen.WIDTH // 2 - HINT_SURFACE.get_width() // 2
    HINT_RECT = HINT_SURFACE.get_rect(topleft=(x, y))
    # ゲームやり直しの設定
    RESET_SURFACE = SMALL_FONT.render("Reset", False, Color.BLACK, Color.LIGHT_GREEN)
    x = Screen.WIDTH * 3 // 4 - RESET_SURFACE.get_width() // 2
    RESET_RECT = RESET_SURFACE.get_rect(topleft=(x, y))

    # パスの設定
    x = Screen.CENTER_X
    y = Screen.CENTER_Y
    PASS_SURFACE = BIG_FONT.render("Pass", True, Color.BLACK, Color.GRAY)
    PASS_RECT = PASS_SURFACE.get_rect(center=(x, y))
