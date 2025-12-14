import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

GRAVITY = 0.5
JUMP_POWER = -12
SPEED = 5

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vy = 0 
        self.on_ground = False
        self.ryvok_timer = 0
        self.ryvok_reload = 0
        self.fuel = 100
        self.double_jumps = 2
        self.facing_right = True
        
        raw_image = pygame.image.load("player.png").convert_alpha()
        scaled_image = pygame.transform.scale(raw_image, (80, 80))
        
        self.image_right = scaled_image
        self.image_left = pygame.transform.flip(scaled_image, True, False)

    def jump(self):
        if self.double_jumps > 0:
            self.vy = JUMP_POWER
            self.on_ground = False
            self.double_jumps -= 1

    def use_ryvok(self):
        if self.ryvok_reload == 0:
            self.ryvok_timer = 10
            self.ryvok_reload = 60

    def use_jetpack(self):
        if self.fuel > 0:
            self.fuel -= 1
            self.vy -= 1
        return True

    def update(self, platforms):
        if self.ryvok_reload > 0:
            self.ryvok_reload -= 1
        if self.ryvok_timer > 0:
            self.ryvok_timer -= 1
            
        if self.ryvok_timer == 0:
            self.vy += GRAVITY
            self.rect.y += self.vy
        else:
            self.vy = 0
            
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.vy = 0
                    self.on_ground = True
                    self.rect.bottom = plat.top
                    self.double_jumps = 2
                elif self.vy < 0:
                    self.vy = 0
                    self.rect.top = plat.bottom

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vy = 0
            self.on_ground = True
            self.double_jumps = 2
            if self.fuel < 100:
                self.fuel += 1

class Enemy:
    def __init__(self, x, y, dist):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.start_x = x
        self.max_dist = dist
        self.direction = 1
        self.speed = 2
        raw_image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (100, 100))

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.max_dist:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

def create_coins():
    return [
        pygame.Rect(400, 350, 20, 20),
        pygame.Rect(150, 250, 20, 20),
        pygame.Rect(520, 150, 20, 20)
    ]

def create_enemies():
    return [
        Enemy(320, 360, 120), 
        Enemy(120, 260, 80)
    ]