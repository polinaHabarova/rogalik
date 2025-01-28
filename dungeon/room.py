import pygame

TITLE_SIZE = 32
FLOOR_COLOR = (200, 200, 200)
WALL_COLOR = (50, 50, 50)
image = pygame.image.load('resurses//sprites//danj//dungeon_floor.png')

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_type):
        super().__init__()
        self.image = pygame.Surface((TITLE_SIZE, TITLE_SIZE), pygame.SRCALPHA)
        if cell_type == 'S':
            self.image.fill((55, 105, 25))
        elif cell_type == 'E':
            self.image.fill((240, 30, 80))
        else:
            title_x, title_y = 1, 0
            title_rect = pygame.Rect(title_x * TITLE_SIZE, title_y * TITLE_SIZE, TITLE_SIZE, TITLE_SIZE)
            self.image.blit(image, (0,0), title_rect)
        self.rect = self.image.get_rect(topleft = (x,y))


class Wall(pygame.sprite.Sprite):
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
        self.floor = Floor(x * TITLE_SIZE, y * TITLE_SIZE, self.cell_type)
        self.walls = self.create_walls(grid)

    def create_walls(self, grid):
        walls = pygame.sprite.Group()
        neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0,), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in neighbours:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= ny < len(grid) and 0 <= nx <= len(grid[0]):
                if grid[ny][nx] is None:
                    wall = Wall(nx * TITLE_SIZE, ny * TITLE_SIZE)
                    walls.add(wall)
            else:
                wall = Wall(nx * TITLE_SIZE, ny * TITLE_SIZE)
                walls.add(wall)
        return walls







