import pygame

# Размеры окна
SCREEN_WEIDTH = 800
SCREEN_HEIGHT = 600

# Основной цвет фона
BACKGROUND_COLOR = (220, 220, 220)

# Цвета для элементов подземелья
FLOOR_COLOR = (200, 200, 200)
WALL_COLOR = (50, 50, 50)

# Размер одного тайтла
TITLE_SIZE = 32

# Масштаб карты: например, каждый квадрат сетки теперь состоит из 2x2 тайтлов,
# то есть для одного квадрата нужно 4 тайтла.
ROOM_SCALE = 2
ROOM_SIZE = TITLE_SIZE * ROOM_SCALE

# Частота обновления экрана
FPS = 60

# Загрузка изображения для пола подземелья
try:
    image = pygame.image.load('resurses/sprites/danj/dungeon_floor.png')
except Exception as e:
    print("Ошибка загрузки изображения dungeon_floor:", e)
    image = pygame.Surface((TITLE_SIZE, TITLE_SIZE))
    image.fill(FLOOR_COLOR)

def load_sprites(path, width, height):
    sprite_sheet = pygame.image.load(path)
    sprite_width, sprite_height = sprite_sheet.get_size()
    frames = []
    for y in range(0, sprite_height, height):
        row = []
        for x in range(0, sprite_width, width):
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
            row.append(frame)
        frames.append(row)
    return frames