import pygame
import sys
import random
from dungeon.generation import generation_dungeon_grid, create_dungeon_sprites
from settings import SCREEN_WEIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, TITLE_SIZE
from character.player import Player
from monsters.base_monsters import Monster
from save_data import save_data, get_data



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
        font = pygame.font.Font(None, 30)
        stats = get_data()
        stats_text = [
            f"Количество смертей: {stats[0]}",
            f"Количество убитых монстров: {stats[1]}",
            f"Количество пройденных уровней: {stats[2]}"
        ]
        x_pos = screen.get_width() - 400
        y_pos = screen.get_height() - 80
        for i, text in enumerate(stats_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (x_pos, y_pos + (i * 25)))
        pygame.display.flip()
        clock.tick(60)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=300, owner="player"):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        if owner == "player":
            self.image.fill((255, 0, 0))
        else:
            self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = speed
        self.owner = owner

    def update(self, dt, walls):
        if self.direction == 'right':
            self.rect.x += self.speed * dt
        elif self.direction == 'left':
            self.rect.x -= self.speed * dt
        elif self.direction == 'up':
            self.rect.y -= self.speed * dt
        elif self.direction == 'down':
            self.rect.y += self.speed * dt

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.kill()
                break

def generate_level(grid_rows, grid_cols, room_count):
    while True:
        try:
            grid, rooms = generation_dungeon_grid(grid_rows, grid_cols, room_count)
            floor_group, walls_group = create_dungeon_sprites(rooms)
            break
        except Exception as e:
            print("Проблема с генерацией карты:", e)
            continue

    start_room = None
    for room in rooms:
        if room.cell_type == 'S':
            start_room = room
            break
    if start_room is None:
        print("Не найдена комната с 'S', используем первую комнату")
        start_room = rooms[0]
    player_start_pos = (start_room.x * TITLE_SIZE, start_room.y * TITLE_SIZE)

    monster_group = pygame.sprite.Group()
    for room in rooms:
        if room.cell_type == '*' and room != start_room:
            if room.x > 0 and room.x < grid_cols - 1 and room.y > 0 and room.y < grid_rows - 1:
                if random.random() < 0.2:
                    spawn_pos = room.floor.rect.center
                    monster = Monster(spawn_pos)
                    monster_group.add(monster)

    return grid, rooms, floor_group, walls_group, start_room, player_start_pos, monster_group

def show_end_menu(screen):
    start_button = Button("Restart Game", font_size=36)
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
        font = pygame.font.Font(None, 30)
        stats = get_data()
        stats_text = [
            f"Количество смертей: {stats[0]}",
            f"Количество убитых монстров: {stats[1]}",
            f"Количество пройденных уровней: {stats[2]}"
        ]
        x_pos = screen.get_width() - 400
        y_pos = screen.get_height() - 80
        for i, text in enumerate(stats_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (x_pos, y_pos + (i * 25)))
        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    pygame.display.set_caption('Roguelike')
    screen = pygame.display.set_mode((SCREEN_WEIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    grid_rows = 20
    grid_cols = 20
    room_count = 80

    grid, rooms, floor_group, walls_group, start_room, player_start_pos, monster_group = generate_level(grid_rows,
                                                                                                        grid_cols,
                                                                                                        room_count)
    print("Стартовая позиция игрока:", player_start_pos)
    player = Player(player_start_pos)
    bullet_group = pygame.sprite.Group()
    monster_bullet_group = pygame.sprite.Group()

    menu_choice = show_start_menu(screen)
    if menu_choice == "start_game":
        running = True
        while running:
            dt = clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = player.shoot()
                        bullet_group.add(bullet)
                    if event.key == pygame.K_e:
                        grid, rooms, floor_group, walls_group, start_room, player_start_pos, monster_group = generate_level(
                            grid_rows, grid_cols, room_count)
                        player.rect.topleft = player_start_pos
                        bullet_group.empty()
                        monster_bullet_group.empty()
            player.update(dt, walls_group.sprites())
            for monster in monster_group:
                new_bullet = monster.update(dt, walls_group.sprites())
                if new_bullet:
                    monster_bullet_group.add(new_bullet)

            bullet_group.update(dt, walls_group.sprites())
            monster_bullet_group.update(dt, walls_group.sprites())

            for bullet in bullet_group:
                hits = pygame.sprite.spritecollide(bullet, monster_group, True)
                if hits:
                    bullet.kill()
                    save_data(0, 1, 0)



            if pygame.sprite.spritecollide(player, monster_bullet_group, True):
                print("Игрок погиб!")
                save_data(1, 0, 0)
                show_end_menu(screen)


            for room in rooms:
                if room.cell_type == 'E':
                    if player.rect.colliderect(room.floor.rect):
                        print("Уровень пройден! Генерация нового уровня...")
                        save_data(0, 0, 1)
                        grid, rooms, floor_group, walls_group, start_room, player_start_pos, monster_group = generate_level(
                            grid_rows, grid_cols, room_count)
                        player.rect.topleft = player_start_pos
                        bullet_group.empty()
                        monster_bullet_group.empty()
                        break

            screen.fill(BACKGROUND_COLOR)
            floor_group.draw(screen)
            walls_group.draw(screen)
            screen.blit(player.image, player.rect)
            bullet_group.draw(screen)
            monster_bullet_group.draw(screen)
            monster_group.draw(screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    main()