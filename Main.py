import pygame
from Board import Board
from Color import Color
from Screen import Screen
from Show import Show
from Player import player
from AI.original_kk import next


class Main:
    pygame.init()

    # マスの設定
    size = 8
    square_size = Screen.BASE_WIDTH // size
    square_centers = None

    # スクリーンの設定
    screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
    pygame.display.set_caption("オセロ")

    # FPSの設定
    FPS = 60
    clock = pygame.time.Clock()

    # 関数-------------------------------------------------------------------------
    def __init__(self):
        """コンストラクタで初期化"""

        # マスの中心の設定
        self.square_centers = [
            [
                ((col_index * self.square_size) + self.square_size // 2 + Screen.START_X,
                 (row_index * self.square_size) + self.square_size // 2 + Screen.START_Y)
                for col_index in range(self.size)
            ] for row_index in range(self.size)
        ]

    def init_data(self):
        """バトルを行う初期化"""

        menu = self.show_start_menu()  # メニューの選択
        board = Board()  # boardを初期化
        cur_color = "black"  # 黒が先行
        game_end = False  # ゲームは始まったばかり

        return menu, board, cur_color, game_end

    def show_start_menu(self):
        """メニューの表示"""

        self.screen.fill(Color.GREEN)
        self.screen.blit(Show.PVP_SURFACE, Show.PVP_RECT)  # pvp用の表示
        self.screen.blit(Show.PVC_SURFACE, Show.PVC_RECT)  # cpu用の表示
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if Show.PVP_RECT.collidepoint(mx, my):
                        return "pvp"
                    elif Show.PVC_RECT.collidepoint(mx, my):
                        return "pvc"

    def draw_screen(self, board):
        """画面にボードを表示する"""

        self.screen.fill(Color.GREEN)  # 背景の塗りつぶし
        self.screen.blit(Show.WAIT_SURFACE, Show.WAIT_RECT)  # 待ったのボタンを描画
        self.screen.blit(Show.RESET_SURFACE, Show.RESET_RECT)  # やり直しボタンを描画
        self.draw_grid()  # グリッド線の描画
        self.draw_board(board)  # 盤面の描画

    def draw_grid(self):
        """グリッド線の描画"""

        start_x = Screen.START_X
        start_y = Screen.START_Y
        end_x = Screen.WIDTH - Screen.START_X
        end_y = Screen.HEIGHT - Screen.START_Y
        for i in range(self.size + 2):
            change = i * self.square_size
            x = start_x + change
            y = start_y + change
            pygame.draw.line(self.screen, Color.BLACK, (start_x, y), (end_x, y), 3)
            pygame.draw.line(self.screen, Color.BLACK, (x, start_y), (x, end_y), 3)

    def draw_board(self, board):
        """盤面の描画"""

        for i in range(self.size ** 2):

            # ビットボードから行と列のインデックスを計算し、マスの中心位置を設定
            row_index = (self.size ** 2 - 1 - i) // self.size
            col_index = (self.size ** 2 - 1 - i) % self.size
            center = self.square_centers[row_index][col_index]

            # マスクを使用して特定の位置に石があるかを確認
            is_black = (1 << i) & board.black_disc_bit
            is_white = (1 << i) & board.white_disc_bit

            if is_black:
                pygame.draw.circle(self.screen, Color.BLACK, (center[0], center[1]), 45)
            elif is_white:
                pygame.draw.circle(self.screen, Color.WHITE, (center[0], center[1]), 45)

    def draw_legal(self, legal_bit):
        """石を置ける場所の色付け"""

        for i in range(self.size ** 2):
            # ビットボードから行と列のインデックスを計算し、マスの中心位置を設定
            row_index = (self.size ** 2 - 1 - i) // self.size
            col_index = (self.size ** 2 - 1 - i) % self.size
            center = self.square_centers[row_index][col_index]

            # マスクを使用して特定の位置に石を置けるかを確認
            legal_mask = (1 << i) & legal_bit
            if legal_mask:
                pygame.draw.circle(self.screen, Color.GRAY, (center[0], center[1]), 30)

    def draw_put_disc(self, col_index, row_index):
        """直前に置いた石を描画"""

        center = self.square_centers[row_index][col_index]  # 置いた石の中心
        pygame.draw.circle(self.screen, Color.LIGHT_GRAY, (center[0], center[1]), 15)

    def draw_stone_score(self, color, score):
        """石の数を描画する"""

        # 石のイラストを描画
        if color == "black":
            stone_surface = Show.BLACK_STONE_SURFACE
        else:
            stone_surface = Show.WHITE_STONE_SURFACE

        # 数字のテキストを描画
        stone_color = Color.BLACK if color == "black" else Color.WHITE
        text_surface = Show.BASE_FONT.render(f" × {score}", True, stone_color)

        # 合成するための新しいサーフェスを作成
        combined_surface = pygame.Surface(
            (
                stone_surface.get_width() + text_surface.get_width(),
                stone_surface.get_height()
            ), pygame.SRCALPHA
        )

        # 石とテキストを合成
        combined_surface.blit(stone_surface, (0, 0))
        combined_surface.blit(text_surface, (stone_surface.get_width(), 0))

        # 合成したサーフェスを指定位置に描画
        if color == "black":
            y = Screen.START_Y + Screen.BASE_HEIGHT
            y += (Screen.START_Y - Show.STONE_SIZE * 2) // 2
            self.screen.blit(combined_surface, (Screen.WIDTH // 2, y))
        else:
            y = (Screen.START_Y - Show.STONE_SIZE * 2) // 2
            self.screen.blit(combined_surface, (Screen.WIDTH // 2, y))

    def draw_pass(self):
        """passを描画"""

        self.screen.blit(Show.PASS_SURFACE, Show.PASS_RECT)  # 中央に表示
        pygame.display.update()  # 画面を更新
        pygame.time.delay(250)  # 一定時間待機

    def judge_game_end(self, board, next_color):
        """ゲーム終了チェック"""

        next_legal_bit = board.legal_bit(next_color)
        if next_legal_bit == 0:
            game_end = True
        else:
            game_end = False
        return game_end

    def judge_winner(self, board):
        """勝敗チェック"""

        if board.black_score > board.white_score:
            self.screen.blit(Show.BLACK_WIN_SURFACE, Show.BLACK_WIN_RECT)
        elif board.black_score < board.white_score:
            self.screen.blit(Show.WHITE_WIN_SURFACE, Show.WHITE_WIN_RECT)
        else:
            self.screen.blit(Show.DROW_SURFACE, Show.DROW_RECT)

    # メインループ==================================================================

    def play_game(self):
        """オセロを行うメイン"""

        col_index = None
        row_index = None
        menu, board, cur_color, game_end = self.init_data()  # バトルを行う初期化
        run = True
        while run:
            self.draw_screen(board)  # 画面にボードを表示する

            legal_bit = board.legal_bit(cur_color)  # 石を置ける場所の取得
            self.draw_legal(legal_bit)  # 石を置ける場所の色付け
            if col_index:
                self.draw_put_disc(col_index, row_index)  # 直前に置いた石を描画
            self.draw_stone_score("black", board.black_score)  # 黒石の数を描画
            self.draw_stone_score("white", board.white_score)  # 白石の数を描画

            # 置ける場所がない場合、パスかゲーム終了
            if legal_bit == 0:
                cur_color = "black" if cur_color == "white" else "white"
                if game_end == True or self.judge_game_end(board, cur_color):
                    game_end = True
                    self.judge_winner(board)  # 勝敗チェック
                    self.screen.blit(Show.ONEMORE_SURFACE, Show.ONEMORE_RECT)  # リセット表示
                else:
                    self.draw_pass()  # パスを描画する

            self.clock.tick(self.FPS)
            pygame.display.update()

            # AI対戦でAIの色ならばAIが選択
            if menu == "pvc" and cur_color == player.color and game_end == False:
                pygame.time.delay(500)  # 一定時間待機
                (col_index, row_index) = next(board)  # 次に置く石の場所を決定する
                board.put_disc(cur_color, col_index, row_index)  # 石を置く
                cur_color = "black" if cur_color == "white" else "white"

            else:
                for event in pygame.event.get():

                    # windowを閉じる
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False

                    # マウスクリック
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()

                        # ゲーム終了していない場合、ゲーム進行
                        if game_end == False:
                            col_index = (mx - Screen.START_X) // self.square_size
                            row_index = (my - Screen.START_Y) // self.square_size
                            if board.put_disc(cur_color, col_index, row_index):  # 石を置く
                                cur_color = "black" if cur_color == "white" else "white"

                        # もう一度ゲームを行う
                        if (Show.ONEMORE_RECT.collidepoint(mx, my) and game_end == True) or Show.RESET_RECT.collidepoint(mx, my):
                            menu, board, cur_color, game_end = self.init_data()  # バトルを行う初期化

                        # 待ったを行う
                        if Show.WAIT_RECT.collidepoint(mx, my) and game_end == False:
                            if menu == "pvp" and len(board.black_disc_bit_list) >= 2:
                                board.undo()  # 1手戻る
                                cur_color = "black" if cur_color == "white" else "white"
                            elif menu == "pvc" and len(board.black_disc_bit_list) >= 3:
                                board.pvc_undo()  # 2手戻る

    # ==============================================================================


if __name__ == "__main__":
    main = Main()  # Mainクラスをインスタンス化
    main.play_game()
    pygame.quit()
