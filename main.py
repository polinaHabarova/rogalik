import pygame
import sys

from dungeon.generation import generation_dungeon_grid, create_dungeon_sprites
from settings import *
class Button(pygame.sprite.Sprite):
    def __init__(self, text, font_size=24, color=(0, 0, 0), bg_color=(220, 220, 220)):
        super().__init__()
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.render_text()

    def render_text(self):
        self.image = self.font.render(self.text, True, self.color, self.bg_color)
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.center = (x, y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
def show_start_menu(screen):
    start_button = Button("Start Game", font_size=36)
    quit_button = Button("Quit", font_size=36)
    start_button.set_pos(screen.get_width() // 2, screen.get_height() // 2 - 50)
    quit_button.set_pos(screen.get_width() // 2, screen.get_height() // 2 + 50)
    buttons = pygame.sprite.Group(start_button, quit_button)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.handle_event(event):
                return "start_game"
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND_COLOR)
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def main():

    pygame.init()
    pygame.display.set_caption('Roguelike')
    screen = pygame.display.set_mode((SCREEN_WEIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    grid_rows = 10
    grid_cols = 10
    room_count = 40
    while True:
        try:
            grid, rooms = generation_dungeon_grid(grid_rows, grid_cols, room_count)
            floor_group, walls_group = create_dungeon_sprites(rooms)
            break
        except:
            pass
    menu_choice = show_start_menu(screen)
    if menu_choice == "start_game":
        running = True
        while running:
            dt = clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill(BACKGROUND_COLOR)
            floor_group.draw(screen)
            walls_group.draw(screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    main()