import pygame

from dungeon.generation import generation_dungeon_grid, create_dungeon_sprites
from settings import *

def main():

    pygame.init()
    pygame.display.set_caption('Roguelike')
    screen = pygame.display.set_mode((SCREEN_WEIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    grid_rows = 10
    grid_cols = 10
    room_count = 15
    grid, rooms = generation_dungeon_grid(grid_rows, grid_cols, room_count)
    floor_group = create_dungeon_sprites(rooms)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND_COLOR)
        floor_group.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()