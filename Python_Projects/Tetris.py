import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Define the dimensions of the game grid
grid_width, grid_height = 10, 20
cell_size = 30

# Define the shapes of the Tetrominoes
SHAPES = [
    [[1, 1, 1, 1]],                                # I
    [[1, 1], [1, 1]],                              # O
    [[1, 0, 0], [1, 1, 1]],                        # T
    [[1, 1, 0], [0, 1, 1]],                        # Z
    [[0, 1, 1], [1, 1, 0]],                        # S
    [[1, 1, 1], [0, 0, 1]],                        # J
    [[1, 1, 1], [1, 0, 0]]                         # L
]

# Define the colors of the Tetrominoes
COLORS = [
    CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE
]

# Define the initial position of the Tetromino
initial_x = grid_width // 2 - 2
initial_y = 0

# Define the game grid
grid = [[BLACK] * grid_width for _ in range(grid_height)]

# Create a new Tetromino
def new_tetromino():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return shape, color, initial_x, initial_y

# Check if a position is valid for the Tetromino
def is_valid_position(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] and (x + col < 0 or x + col >= grid_width or
                                    y + row >= grid_height or
                                    grid[y + row][x + col] != BLACK):
                return False
    return True

# Place the Tetromino on the grid
def place_tetromino(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                grid[y + row][x + col] = color

# Remove completed rows from the grid
def remove_completed_rows():
    full_rows = []
    for row in range(grid_height):
        if all(cell != BLACK for cell in grid[row]):
            full_rows.append(row)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * grid_width)

# Draw the Tetromino on the grid
def draw_tetromino(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                pygame.draw.rect(window, color, (x * cell_size + col * cell_size,
                                                 y * cell_size + row * cell_size,
                                                 cell_size, cell_size))

# Draw the grid
def draw_grid():
    for row in range(grid_height):
        for col in range(grid_width):
            pygame.draw.rect(window, grid[row][col], (col * cell_size, row * cell_size, cell_size, cell_size), 1)

# Check if the game is over
def is_game_over():
    return any(cell != BLACK for cell in grid[0])

# Render text on the window
def render_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    window.blit(text_surface, text_rect)

# Game loop
def game_loop():
    clock = pygame.time.Clock()

    tetromino_shape, tetromino_color, tetromino_x, tetromino_y = new_tetromino()

    game_over = False
    score = 0
    start_time = pygame.time.get_ticks()

    # Load the font
    font = pygame.font.Font(None, 36)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_position(tetromino_shape, tetromino_x - 1, tetromino_y):
                        tetromino_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid_position(tetromino_shape, tetromino_x + 1, tetromino_y):
                        tetromino_x += 1
                elif event.key == pygame.K_DOWN:
                    if is_valid_position(tetromino_shape, tetromino_x, tetromino_y + 1):
                        tetromino_y += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = list(zip(*reversed(tetromino_shape)))
                    if is_valid_position(rotated_shape, tetromino_x, tetromino_y):
                        tetromino_shape = rotated_shape

        if is_valid_position(tetromino_shape, tetromino_x, tetromino_y + 1):
            tetromino_y += 1
        else:
            place_tetromino(tetromino_shape, tetromino_x, tetromino_y, tetromino_color)
            remove_completed_rows()
            tetromino_shape, tetromino_color, tetromino_x, tetromino_y = new_tetromino()

            if is_game_over():
                game_over = True

        # Clear the window
        window.fill(BLACK)

        # Draw the Tetromino
        draw_tetromino(tetromino_shape, tetromino_x, tetromino_y, tetromino_color)

        # Draw the grid
        draw_grid()

        # Calculate the elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        # Render score and time text on the window
        render_text(f"Score: {score}", font, WHITE, 20, 20)
        render_text(f"Time: {elapsed_time:.1f} seconds", font, WHITE, 20, 60)

        # Update the display
        pygame.display.update()

        # Set the frames per second
        clock.tick(5)

    # Quit pygame
    pygame.quit()

# Run the game
game_loop()
