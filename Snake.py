import collections
import random
import tkinter as tk
from tkinter import messagebox

import pygame

Direction = collections.namedtuple('Directions', ['x', 'y'])
Position = collections.namedtuple('Position', ['x', 'y'])


class Cube:
    rows = 20
    w = 500

    def __init__(self, start, color=pygame.color.THECOLORS['red']):
        self.pos = Position(*start)
        self.direction = Direction(0, 0)
        self.color = color

    def move(self, direction):
        self.direction = direction
        new_x = (self.pos.x + direction.x) % self.rows
        new_y = (self.pos.y + direction.y) % self.rows

        self.pos = Position(new_x, new_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        x, y = self.pos

        pygame.draw.rect(surface, self.color, (x * dis + 1, y * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (x * dis + centre - radius, y * dis + 8)
            circle_middle2 = (x * dis + dis - radius * 2, y * dis + 8)
            pygame.draw.circle(surface, pygame.color.THECOLORS['black'], circle_middle, radius)
            pygame.draw.circle(surface, pygame.color.THECOLORS['black'], circle_middle2, radius)


class Snake:
    body = []
    turns = {}

    def __init__(self, pos):
        self.head = Cube(pos)
        self.body.append(self.head)
        self.direction = Direction(0, 1)

    def move(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                return False

            directions = {
                pygame.K_LEFT: Direction(-1, 0),
                pygame.K_RIGHT: Direction(1, 0),
                pygame.K_UP: Direction(0, -1),
                pygame.K_DOWN: Direction(0, 1),
            }
            for key in directions.keys():
                if keys[key]:
                    self.turns[self.head.pos[:]] = directions[key]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(Direction(turn[0], turn[1]))
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.direction)
        return True

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction = Direction(0, 1)

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.direction

        self.body.append(Cube((tail.pos[0] - dx, tail.pos[1] - dy)))
        self.body[-1].direction = Direction(dx, dy)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=i == 0)


class SnakeGame:
    def __init__(self, window_size, grid_lines):
        self.window_size = window_size
        self.grid_lines = grid_lines
        self.square_size = window_size // grid_lines
        self.surface = pygame.display.set_mode((self.window_size, self.window_size))
        self.snake = Snake(Position(grid_lines // 2, grid_lines // 2))
        self.snack = Cube((0, 0))

    def draw_grid(self):
        line_color = pygame.color.THECOLORS['white']
        x = 0
        y = 0
        for _ in range(self.grid_lines):
            x += self.square_size
            y += self.square_size
            pygame.draw.line(self.surface, line_color, (x, 0), (x, self.window_size))
            pygame.draw.line(self.surface, line_color, (0, y), (self.window_size, y))

    def redraw_window(self):
        self.surface.fill(pygame.color.THECOLORS['black'])
        self.snake.draw(self.surface)
        self.snack.draw(self.surface)
        self.draw_grid()
        pygame.display.update()

    def random_snack(self):
        x = random.randrange(self.grid_lines)
        y = random.randrange(self.grid_lines)
        while (x, y) in [z.pos for z in self.snake.body]:
            x = random.randrange(self.grid_lines)
            y = random.randrange(self.grid_lines)
        self.snack = Cube((x, y), color=pygame.color.THECOLORS['green'])

    @staticmethod
    def message_box(subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        root.destroy()

    def run(self):
        self.random_snack()
        game_running = True

        clock = pygame.time.Clock()

        while game_running:
            pygame.time.delay(50)
            clock.tick(10)
            game_running = self.snake.move()
            if self.snake.body[0].pos == self.snack.pos:
                self.snake.add_cube()
                self.random_snack()

            for x in range(len(self.snake.body)):
                if self.snake.body[x].pos in list(map(lambda z: z.pos, self.snake.body[x + 1:])):
                    print('Score: ', len(s.body))
                    self.message_box('You Lost!', 'Play again...')
                    self.snake.reset((self.grid_lines // 2, self.grid_lines // 2))
                    break

            self.redraw_window()
        pygame.quit()


if __name__ == '__main__':
    game = SnakeGame(window_size=500, grid_lines=10)
    game.run()
