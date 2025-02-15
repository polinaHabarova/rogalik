import pygame
from settings import TITLE_SIZE
from settings import load_sprites

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=300, owner="player"):
        super().__init__()
        self.animation = load_sprites('resurses/sprites/hero/tomato.png', TITLE_SIZE, TITLE_SIZE)
        self.image = pygame.transform.scale(self.animation[0][1], (32, 32))
        if owner == "player":
            pass
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

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed=150):
        super().__init__()
        self.animation = load_sprites('resurses/sprites/hero/character_walking.png', 64, 64)
        self.image = pygame.transform.scale(self.animation[0][2], (28, 28))
        self.animation_speed = 10
        self.moving = False
        self.frame_index = 0
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.direction = 'right'

    def update(self, dt, walls):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        self.moving = False
        if keys[pygame.K_LEFT]:
            dx = -self.speed * dt
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed * dt
            self.direction = 'right'
            self.moving = True
        elif keys[pygame.K_UP]:
            dy = -self.speed * dt
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_DOWN]:
            dy = self.speed * dt
            self.direction = 'down'
            self.moving = True

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                elif dy < 0:
                    self.rect.top = wall.rect.bottom
        self.animate()

    def animate(self):
        direction_map = {
            'up': 0,
            'right': 1,
            'down': 2,
            'left': 3
        }
        row = direction_map[self.direction]
        if self.moving :
            self.frame_index += self.animation_speed * 0.1
            if self.frame_index >= len(self.animation[row]):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = pygame.transform.scale(self.animation[int(self.frame_index)][row], (28, 28))





    def shoot(self):
        bullet = Bullet(self.rect.center, self.direction, owner="player")
        return bullet
