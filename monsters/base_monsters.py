import pygame
import random
from settings import TITLE_SIZE, load_sprites

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

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, speed=100):
        super().__init__()
        self.animation = load_sprites('resurses/sprites/monstr/enemy.png', 32, 32)
        self.image = pygame.transform.scale(self.animation[0][1], (32, 32))
        self.animation_speed = 10
        self.moving = False
        self.frame_index = 0
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.move_timer = 0
        self.move_interval = random.uniform(0.5, 1.5)
        self.shoot_timer = 0
        self.shoot_interval = random.uniform( 2, 3)

    def update(self, dt, walls):
        self.move_timer += dt
        self.moving = False
        if self.move_timer >= self.move_interval:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.move_timer = 0
        dx, dy = 0, 0
        if self.direction == 'left':
            dx = -self.speed * dt
            self.moving = True
        elif self.direction == 'right':
            dx = self.speed * dt
            self.moving = True
        elif self.direction == 'up':
            dy = -self.speed * dt
            self.moving = True
        elif self.direction == 'down':
            dy = self.speed * dt
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

        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            if random.random() < 0.8:
                bullet = self.shoot()
                self.shoot_timer = 0
                self.shoot_interval = random.uniform(1, 2)
                return bullet
        self.animate( )
        return None

    def animate(self):
        direction_map = {
            'down': 0,
            'left': 1,
            'right': 2,
            'up': 3
        }
        row = direction_map[self.direction]
        if self.moving :
            self.frame_index += self.animation_speed * 0.1
            if self.frame_index >= len(self.animation[row]):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = pygame.transform.scale(self.animation[row][int(self.frame_index)], (32, 32))

    def shoot(self):
        return Bullet(self.rect.center, self.direction, speed=300, owner="monster")

