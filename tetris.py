import pygame
import random

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Настройки игрового поля
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Фигуры тетрамино и их цвета
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # J
    [[1, 1, 1], [0, 0, 1]], # L
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]
COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Простой Тетрис")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {'shape': shape, 'color': color, 'x': GRID_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}

    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True

    def place_piece(self, piece):
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    if piece['y'] + i < 0:
                        self.game_over = True
                    else:
                        self.grid[piece['y'] + i][piece['x'] + j] = piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        self.lines_cleared += lines_cleared
        self.level = self.lines_cleared // 10 + 1
        
        if lines_cleared == 1:
            self.score += 100 * self.level
        elif lines_cleared == 2:
            self.score += 300 * self.level
        elif lines_cleared == 3:
            self.score += 500 * self.level
        elif lines_cleared == 4:
            self.score += 800 * self.level

    def update(self):
        if not self.game_over:
            self.current_piece['y'] += 1
            if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                self.current_piece['y'] -= 1
                self.place_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.new_piece()
                if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                    self.game_over = True

    def draw(self):
        screen.fill(BLACK)
        
        # Отрисовка сетки
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Отрисовка текущей фигуры
        if not self.game_over:
            for i, row in enumerate(self.current_piece['shape']):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece['color'], 
                                        ((self.current_piece['x'] + j) * BLOCK_SIZE, 
                                         (self.current_piece['y'] + i) * BLOCK_SIZE, 
                                         BLOCK_SIZE, BLOCK_SIZE))

        # Отрисовка информации
        info_x = GRID_WIDTH * BLOCK_SIZE + 10
        score_text = font.render(f'Счет: {self.score}', True, WHITE)
        level_text = font.render(f'Уровень: {self.level}', True, WHITE)
        lines_text = font.render(f'Линии: {self.lines_cleared}', True, WHITE)
        
        screen.blit(score_text, (info_x, 20))
        screen.blit(level_text, (info_x, 60))
        screen.blit(lines_text, (info_x, 100))

        # Управление
        controls_text = [
            "Управление:",
            "← → - двигать",
            "↑ - повернуть",
            "↓ - ускорить",
            "R - перезапуск"
        ]
        
        for i, text in enumerate(controls_text):
            control_surface = font.render(text, True, WHITE)
            screen.blit(control_surface, (info_x, 160 + i * 30))

        # Сообщение о конце игры
        if self.game_over:
            game_over_text = font.render('ИГРА ОКОНЧЕНА!', True, RED)
            restart_text = font.render('Нажми R для перезапуска', True, WHITE)
            screen.blit(game_over_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 80, GRID_HEIGHT * BLOCK_SIZE // 2 - 20))
            screen.blit(restart_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 120, GRID_HEIGHT * BLOCK_SIZE // 2 + 20))

def main():
    game = Tetris()
    fall_time = 0
    fall_speed = 500

    running = True
    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        if game.valid_move(game.current_piece, game.current_piece['x'] - 1, game.current_piece['y']):
                            game.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT:
                        if game.valid_move(game.current_piece, game.current_piece['x'] + 1, game.current_piece['y']):
                            game.current_piece['x'] += 1
                    if event.key == pygame.K_DOWN:
                        if game.valid_move(game.current_piece, game.current_piece['x'], game.current_piece['y'] + 1):
                            game.current_piece['y'] += 1
                    if event.key == pygame.K_UP:
                        rotated_shape = list(zip(*reversed(game.current_piece['shape'])))
                        old_shape = game.current_piece['shape']
                        game.current_piece['shape'] = rotated_shape
                        if not game.valid_move(game.current_piece, game.current_piece['x'], game.current_piece['y']):
                            game.current_piece['shape'] = old_shape
                if event.key == pygame.K_r:
                    game = Tetris()

        if fall_time >= fall_speed:
            fall_time = 0
            game.update()

        game.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
