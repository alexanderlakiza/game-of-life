from typing import List, Optional, Tuple
from copy import deepcopy
import random

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(self, size: Tuple[int, int], randomize: bool = True,
                 max_generations: Optional[float] = float('inf')) -> None:
        self.rows, self.cols = size  # Размер клеточного поля
        self.prev_generation = self.create_grid()  # Предыдущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)  # Текущее поколение клеток
        self.max_generations = max_generations  # Максимальное число поколений
        self.n_generation = 1  # Текущее число поколений

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создать игровое поле
        """
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Получить состояние соседних клеток
        """
        cells = []
        x, y = cell
        n = self.rows - 1
        m = self.cols - 1
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (0 <= i <= n and 0 <= j <= m) or (i == x and j == y):
                    continue
                cells.append(self.curr_generation[i][j])
        return cells

    def get_next_generation(self) -> Grid:
        """
        Создать поле следующего шага
        """
        new_grid = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                a = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j]:
                    if a in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if a == 3:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        f = open(filename, 'r')
        lines = f.read().split('\n')
        rows = len(lines) - 1
        cols = len(lines[0].strip())
        game = GameOfLife(size=(rows, cols), randomize=False)

        for s in lines:
            line = []
            for ch in s:
                line.append(int(ch))
            grid.append(line)
        game.curr_generation = deepcopy(grid)
        return game
