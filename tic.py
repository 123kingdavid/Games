import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    """Draw the grid lines."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw the X and O figures on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                          row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)

def mark_square(row, col, player):
    """Mark a square with the player's symbol."""
    board[row][col] = player

def is_square_empty(row, col):
    """Check if a square is empty."""
    return board[row][col] is None

def check_winner():
    """Check if there's a winner."""
    # Check rows and columns
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None

def is_board_full():
    """Check if the board is full."""
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

# Main game loop
draw_lines()
player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # X coordinate
            mouseY = event.pos[1]  # Y coordinate

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if is_square_empty(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()
                winner = check_winner()
                if winner:
                    print(f"Player {winner} wins!")
                    game_over = True
                elif is_board_full():
                    print("It's a draw!")
                    game_over = True
                else:
                    player = 'O' if player == 'X' else 'X'
                    while True:  # Main game loop
                        draw_lines()
                        board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                        player = 'X'
                        game_over = False

                        while True:  # Single round loop
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                                    mouseX = event.pos[0]  # X coordinate
                                    mouseY = event.pos[1]  # Y coordinate

                                    clicked_row = mouseY // SQUARE_SIZE
                                    clicked_col = mouseX // SQUARE_SIZE

                                    if is_square_empty(clicked_row, clicked_col):
                                        mark_square(clicked_row, clicked_col, player)
                                        draw_figures()
                                        winner = check_winner()
                                        if winner:
                                            print(f"Player {winner} wins!")
                                            game_over = True
                                        elif is_board_full():
                                            print("It's a draw!")
                                            game_over = True
                                        else:
                                            player = 'O' if player == 'X' else 'X'

                                if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                    break  # Exit the round loop to restart

                            pygame.display.update()

                        # Ask if the players want to play again
                        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
                        if play_again != "yes":
                            print("Thanks for playing! Goodbye!")
                            break

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
            screen.fill(BG_COLOR)
            draw_lines()
            player = 'X'
            game_over = False

    pygame.display.update()
