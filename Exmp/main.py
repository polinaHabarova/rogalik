import sys
import pygame
from pygame.locals import *
import random

TILE_SIZE = 32
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 50)
RED = (200, 0, 0)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.x_velocity = 2
        self.direction = 1
        self.change_direction_time = 3000
        self.last_change_time = pygame.time.get_ticks()

    def check_and_change_direction(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_change_time >= self.change_direction_time:
            self.direction *= -1
            self.last_change_time = current_time

    def update(self, player, tiles):
        self.check_and_change_direction()
        self.rect.x += self.x_velocity * self.direction
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.direction > 0:
                    self.rect.right = tile.rect.left
                elif self.direction < 0:
                    self.rect.left = tile.rect.right
                self.direction *= -1
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.walk_frames = [
            pygame.image.load('sprites/player_walk_right_1.png').convert_alpha(),
            pygame.image.load('sprites/player_walk_right_2.png').convert_alpha(),
            pygame.image.load('sprites/player_walk_right_3.png').convert_alpha(),
            pygame.image.load('sprites/player_walk_right_4.png').convert_alpha()
        ]
        self.idle_frame = pygame.image.load('sprites/player.png').convert_alpha()
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.x_velocity = 0
        self.y_velocity = 0
        self.on_ground = False
        self.can_jump = False
        self.bullets = pygame.sprite.Group()
        self.animation_speed = 0.2
        self.last_update = pygame.time.get_ticks()

    def animate(self):
        now = pygame.time.get_ticks()
        if self.x_velocity != 0:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame]
                if self.x_velocity < 0:
                    self.image = pygame.transform.flip(self.image, True, False)
                else:
                    self.image = self.image
        else:
            self.image = self.idle_frame
            if self.x_velocity < 0:
                self.image = pygame.transform.flip(self.idle_frame, True, False)
            else:
                self.image = self.idle_frame

    def update(self, tiles):
        self.animate()
        self.rect.x += self.x_velocity
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.x_velocity > 0:
                    self.rect.right = tile.rect.left
                elif self.x_velocity < 0:
                    self.rect.left = tile.rect.right
                break
        self.rect.y += self.y_velocity
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.y_velocity > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.can_jump = True
                elif self.y_velocity < 0:
                    self.rect.top = tile.rect.bottom
                self.y_velocity = 0
                break
        if not self.on_ground:
            self.y_velocity += 0.4
            if self.y_velocity > 6:
                self.y_velocity = 6
        self.flip_image()

    def jump(self):
        if self.can_jump:
            self.y_velocity = -8
            self.can_jump = False

    def shoot(self, direction):
        if self.x_velocity < 0:
            direction = 'left'
        else:
            direction = 'right'
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
        self.bullets.add(bullet)

    def reset_position(self, start_x, start_y):
        self.rect.topleft = (start_x * TILE_SIZE, start_y * TILE_SIZE)
        self.x_velocity = 0
        self.y_velocity = 0

    def flip_image(self):
        if self.x_velocity < 0:
            self.original_image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.original_image = self.original_image
class Wall_Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
class Ice_Wall_Tile(Wall_Tile):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/plat_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
class Stone_Wall_Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/stone_wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/spike.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/exit.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.original_image = pygame.image.load('sprites/bullet.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self, tiles, enemies):
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(self.original_image, True, False)

        hit_enemies = pygame.sprite.spritecollide(self, enemies, True)
        if hit_enemies:
            self.kill()

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.kill()

def load_level(filename):
    with open(f'levels/{filename}', 'r') as f:
        lines = f.readlines()
    rows = len(lines)
    cols = max(len(line.strip()) for line in lines)
    tiles = []
    spikes = []
    enemies = []
    player = None
    exit_tile = None
    enemies_group = pygame.sprite.Group()
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == '#':
                tiles.append(Wall_Tile(x, y))
            elif char == '@':
                tiles.append(Ice_Wall_Tile(x, y))
            elif char == '$':
                tiles.append(Stone_Wall_Tile(x, y))
            elif char == 'P':
                player = Player(x, y)
            elif char == 'E':
                exit_tile = Exit(x, y)
            elif char == 'S':
                spikes.append(Spike(x, y))
            elif char == 'V':
                enemy = Enemy(x, y)
                enemies.append(enemy)
                enemies_group.add(enemy)
    return tiles, player, exit_tile, rows, cols, spikes, enemies_group
def draw_level(screen, tiles, player, exit_tile, spikes, enemies):
    screen.fill(WHITE)
    for tile in tiles:
        screen.blit(tile.image, tile.rect)
    for spike in spikes:
        screen.blit(spike.image, spike.rect)
    screen.blit(player.image, player.rect)
    if exit_tile is not None:
        screen.blit(exit_tile.image, exit_tile.rect)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)
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
        if event.type == MOUSEBUTTONDOWN:
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
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if start_button.handle_event(event):
                return "start_game"
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(60)
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    current_level = 1
    menu_choice = show_start_menu(screen)
    if menu_choice == "start_game":
        running = True
        while running:
            tiles, player, exit_tile, rows, cols, spikes, enemies_group = load_level(
                f'level_{current_level}.txt'
            )
            start_x, start_y = (
                player.rect.x // TILE_SIZE,
                player.rect.y // TILE_SIZE,
            )
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key == K_LEFT:
                            player.x_velocity -= 2
                        elif event.key == K_RIGHT:
                            player.x_velocity += 2
                        elif event.key == K_SPACE:
                            player.jump()
                        elif event.key == K_f:
                            if player.x_velocity > 0:
                                player.shoot('right')
                            else:
                                player.shoot('left')
                    elif event.type == KEYUP:
                        if event.key == K_LEFT or event.key == K_RIGHT:
                            player.x_velocity = 0

                player.update(tiles)
                for enemy in enemies_group:
                    enemy.update(player, tiles)
                player.bullets.update(tiles, enemies_group)
                for spike in spikes:
                    if player.rect.colliderect(spike.rect):
                        player.reset_position(start_x, start_y)
                        break
                if exit_tile is not None and player.rect.colliderect(exit_tile.rect):
                    print("Вы прошли уровень!")
                    current_level += 1
                    break

                draw_level(screen, tiles, player, exit_tile, spikes, enemies_group)
                player.bullets.draw(screen)
                pygame.display.flip()
                clock.tick(60)

if __name__ == "__main__":
    main()