from game import GameOfLife
import pygame


class GUI:
    def __init__(self, game: GameOfLife, cell_size: int = 25, speed: int = 10) -> None:
        self.game = game  # Игра
        self.cell_size = cell_size  # Размер клеток
        self.speed = speed  # Скорость протекания игры
        self.screen_size = game.cols * self.cell_size, game.rows * self.cell_size  # Размер игрового окна
        self.screen = pygame.display.set_mode(self.screen_size)  # Экран игры

    def draw_lines(self) -> None:
        """
        Нарисовать линии игрового поля
        """
        width, height = self.screen_size

        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (width, y))

    def draw_grid(self) -> None:
        """
        Нарисовать клетки игрового поля
        """
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                x = i * self.cell_size + 1
                y = j * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.game.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                elif self.game.curr_generation[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))

    def run(self) -> None:
        """
        Игра
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        pause = False

        while running and self.game.is_changing and not self.game.is_max_generations_exceed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:  # Пауза на "пробел"
                    pause = not pause
                elif event.type == pygame.KEYUP and event.key == pygame.K_q:  # Выход из игры на "q"
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pause:  # Поменять состояние клетки, нажав на неё
                    self.mouse_fill_cell()

            # Отрисовка игрового поля
            self.draw_lines()
            self.draw_grid()

            if not pause:
                self.game.step()

            pygame.display.flip()
            clock.tick(self.speed)  # Условие на скорость игры

        pygame.quit()

    def mouse_fill_cell(self) -> None:
        """
        Поменять состоянии клетки кликом мыши
        """
        x, y = pygame.mouse.get_pos()
        row = x // self.cell_size
        col = y // self.cell_size
        self.game.curr_generation[row][col] = (self.game.curr_generation[row][col] + 1) % 2


if __name__ == '__main__':
    life = GameOfLife((20, 20), max_generations=150)
    # life = life.from_file("examples/01.txt")  # Пример чтения из файла
    gui = GUI(life, speed=10, cell_size=30)
    gui.run()
