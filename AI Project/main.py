import pygame
import sys
from algorithm import minimax, AI, PLAYER, EMPTY, check_winner

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6, 7
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 5

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (180, 180, 180)

pygame.init()
# ขนาดกระดานแต่ละช่อง
SQUARE_SIZE = 100
# ขนาดกระดาน
ROWS = 6
COLS = 7
# คำนวณขนาดหน้าต่างให้พอดีกับกระดาน
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bingo Four Star")
FONT = pygame.font.SysFont("arial", 60)
SMALL_FONT = pygame.font.SysFont("arial", 30)

class BingoGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.player_turn = True
        self.winner = None
        self.running = True
        self.ai_thinking = False
        self.difficulty = 2  # Set Default to normal
        self.current_thinking_pos = None

    def draw_board(self):
        WIN.fill((0, 0, 0))

        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(WIN, (0, 0, 255), rect)

                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                radius = SQUARE_SIZE // 2 - 5

                if self.board[row][col] == PLAYER:
                    pygame.draw.circle(WIN, (255, 0, 0), center, radius)
                elif self.board[row][col] == AI:
                    pygame.draw.circle(WIN, (255, 255, 0), center, radius)
                else:
                    pygame.draw.circle(WIN, (0, 0, 0), center, radius)

        # แสดงตำแหน่งที่ AI กำลังคิด (ถ้ามี)
        if self.current_thinking_pos:
            row, col = self.current_thinking_pos
            rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(WIN, (255, 255, 255), rect, 3)

        pygame.display.update()


    def get_clicked_pos(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def is_valid_move(self, row, col):
        if self.board[row][col] != EMPTY:
            return False
        if row == ROWS - 1:
            return True
        return self.board[row + 1][col] != EMPTY

    def is_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = self.get_clicked_pos(pos)
                if self.is_valid_move(row, col):
                    self.board[row][col] = PLAYER
                    self.player_turn = False
                    self.winner = check_winner(self.board)

    def set_difficulty(self, difficulty):
        if difficulty == 'easy':
            self.difficulty = 1
        elif difficulty == 'normal':
            self.difficulty = 2
        elif difficulty == 'hard':
            self.difficulty = 3
        elif difficulty == 'expert':
            self.difficulty = 4
        elif difficulty == 'master':
            self.difficulty = 8
                 

    # ai_move
    def ai_move(self):
        self.ai_thinking = True
        self.current_thinking_pos = None

        def visualize_thinking(temp_board, pos):
            self.current_thinking_pos = pos
            self.board = temp_board
            self.draw_board()
            pygame.time.delay(0) # ระยะเวลาที่เห็น ai ประเมิณ

        self.draw_board()
        pygame.time.delay(500)

        _, new_board = minimax(self.board, self.difficulty, True, callback=visualize_thinking)

        self.board = new_board
        self.player_turn = True
        self.winner = check_winner(self.board)
        self.ai_thinking = False
        self.current_thinking_pos = None

    def run_game(self):
        while self.running:
            self.draw_board()

            if self.winner:
                print("Winner:", "Player" if self.winner == PLAYER else "AI")
                pygame.time.delay(2000)
                self.running = False
                continue

            if self.is_full():
                print("Draw!")
                pygame.time.delay(2000)
                self.running = False
                continue

            self.handle_events()

            if not self.player_turn and not self.winner:
                self.ai_move()

        pygame.quit()

if __name__ == '__main__':
    game = BingoGame()
    game.set_difficulty('master')
    game.run_game()