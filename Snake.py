import collections
import random
import tkinter as tk
from tkinter import messagebox

import pygame

Direction = collections.namedtuple('Directions', ['x', 'y'])
Position = collections.namedtuple('Position', ['x', 'y'])


class Cube:
    grid_lines = 20
    window_size = 500

    def __init__(self, start, color=pygame.color.THECOLORS['red']):
        self.pos = Position(*start)
        self.direction = Direction(0, 0)
        self.color = color

    def move(self, direction):
        self.direction = direction
        new_x = (self.pos.x + direction.x) % self.grid_lines
        new_y = (self.pos.y + direction.y) % self.grid_lines

        self.pos = Position(new_x, new_y)

    def draw(self, surface, eyes=False):
        dis = self.window_size // self.grid_lines
        x, y = self.pos

        pygame.draw.rect(surface, self.color, (x * dis + 1, y * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = (x + 0.5) * dis
            radius = 6 * dis // 50
            y_offset = 8 * dis // 50

            left_eye = (centre - 1.5 * radius, y * dis + y_offset)
            right_eye = (centre + 1.5 * radius, y * dis + y_offset)
            pygame.draw.circle(surface, pygame.color.THECOLORS['black'], left_eye, radius)
            pygame.draw.circle(surface, pygame.color.THECOLORS['black'], right_eye, radius)


class Snake:
    body = []
    turns = {}

    def __init__(self, pos):
        self.head = Cube(pos)
        self.body.append(self.head)
        self.direction = Direction(0, 1)

    def move(self):
        self.turns[self.head.pos[:]] = self.direction
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn)
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

        self.body.append(Cube((tail.pos.x - dx, tail.pos.y - dy)))
        self.body[-1].direction = Direction(dx, dy)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=i == 0)

    def has_collision(self):
        positions = [c.pos for c in self.body]
        return len(set(positions)) != len(positions)

    @property
    def score(self):
        return len(self.body)

    def eats_snack(self, snack):
        return self.body[0].pos == snack.pos


class SnakeGame:
    CONTROLS = {
        pygame.K_LEFT: Direction(-1, 0),
        pygame.K_RIGHT: Direction(1, 0),
        pygame.K_UP: Direction(0, -1),
        pygame.K_DOWN: Direction(0, 1),
    }

    def __init__(self, window_size, grid_lines):
        self.window_size = window_size
        self.grid_lines = grid_lines
        Cube.window_size = window_size
        Cube.grid_lines = grid_lines
        self.square_size = window_size // grid_lines
        self.surface = pygame.display.set_mode((self.window_size, self.window_size))
        self.snake = Snake(Position(grid_lines // 2, grid_lines // 2))
        self.snack = Cube((0, 0))

    def draw_grid(self):
        line_color = pygame.color.THECOLORS['white']
        loc = 0
        for _ in range(self.grid_lines):
            loc += self.square_size
            pygame.draw.line(self.surface, line_color, (loc, 0), (loc, self.window_size))
            pygame.draw.line(self.surface, line_color, (0, loc), (self.window_size, loc))

    def redraw_window(self):
        self.surface.fill(pygame.color.THECOLORS['black'])
        self.snake.draw(self.surface)
        self.snack.draw(self.surface)
        self.draw_grid()
        pygame.display.update()

    def spawn_new_snack(self):
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
        self.spawn_new_snack()
        game_running = True

        clock = pygame.time.Clock()

        while game_running:
            pygame.time.delay(50)
            clock.tick(10)
            game_running = self.process_events()
            self.snake.move()
            if self.snake.eats_snack(self.snack):
                self.snake.add_cube()
                self.spawn_new_snack()

            if self.snake.has_collision():
                message = f'Score: {self.snake.score}\nPress OK to play again.'
                self.message_box('You Lost!', message)
                self.snake.reset((self.grid_lines // 2, self.grid_lines // 2))
            self.redraw_window()
        pygame.quit()

    def process_events(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            elif event.type == pygame.KEYDOWN and event.key in self.CONTROLS.keys():
                self.snake.direction = self.CONTROLS.get(event.key, self.snake.direction)
        return True


if __name__ == '__main__':
    game = SnakeGame(window_size=1000, grid_lines=10)
    game.run()
