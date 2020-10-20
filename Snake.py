import random
import tkinter as tk
from tkinter import messagebox

import pygame


class Cube:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=pygame.color.THECOLORS['red']):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, pygame.color.THECOLORS['black'], circle_middle, radius)
            pygame.draw.circle(surface, pygame.color.THECOLORS['black'], circle_middle2, radius)


class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                return False

            directions = {
                pygame.K_LEFT: (-1, 0),
                pygame.K_RIGHT: (1, 0),
                pygame.K_UP: (0, -1),
                pygame.K_DOWN: (0, 1),
            }
            for key in directions.keys():
                if keys[key]:
                    self.dirnx, self.dirny = directions[key]
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)
        return True

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        self.body.append(Cube((tail.pos[0] - dx, tail.pos[1] - dy)))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=i == 0)


def draw_grid(width, rows, surface):
    square_size = width // rows
    line_color = pygame.color.THECOLORS['white']
    x = 0
    y = 0
    for _ in range(rows):
        x += square_size
        y += square_size
        pygame.draw.line(surface, line_color, (x, 0), (x, width))
        pygame.draw.line(surface, line_color, (0, y), (width, y))


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body
    x = random.randrange(rows)
    y = random.randrange(rows)

    while (x, y) in [z.pos for z in positions]:
        x = random.randrange(rows)
        y = random.randrange(rows)
    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake(pygame.color.THECOLORS['red'], (10, 10))
    snack = Cube(random_snack(rows, s), color=pygame.color.THECOLORS['green'])
    game_running = True

    clock = pygame.time.Clock()

    while game_running:
        pygame.time.delay(50)
        clock.tick(10)
        game_running = s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color=pygame.color.THECOLORS['green'])

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((rows // 2, rows // 2))
                break

        redraw_window(win)
    pygame.quit()


if __name__ == '__main__':
    main()
