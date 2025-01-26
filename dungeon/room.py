import pygame

TITLE_SIZE = 32
FLOOR_COLOR = (200, 200, 200)
WALL_COLOR = (50, 50, 50)

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TITLE_SIZE, TITLE_SIZE))
        self.image.fill(FLOOR_COLOR)
        self.rect = self.image.get_rect(topleft = (x,y))


class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TITLE_SIZE, TITLE_SIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

class Room:
    def __init__(self, grid, x, y, cell_type):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.floor = Floor(x * TITLE_SIZE, y * TITLE_SIZE)



