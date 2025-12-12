import pygame

# --- КОНСТАНТИ ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Кольори
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Фізика
GRAVITY = 0.5
JUMP_POWER = -12
SPEED = 5

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vy = 0 # Швидкість по вертикалі
        self.on_ground = False
        self.ryvok_timer = 0
        self.ryvok_reload = 0
        self.fuel = 100
        self.double_jumps = 2

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

    # УВАГА: Я додав аргумент platforms, щоб клас знав про них
    def update(self, platforms):
        if self.ryvok_reload > 0:
            self.ryvok_reload -= 1
        if self.ryvok_timer > 0:
            self.ryvok_timer -= 1
            
        # Гравітація
        if self.ryvok_timer == 0:
            self.vy += GRAVITY
            self.rect.y += self.vy
        else:
            self.vy = 0
            
        # Перевірка колізій з платформами
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

        # Підлога
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vy = 0
            self.on_ground = True
            self.double_jumps = 2
            if self.fuel < 100:
                self.fuel += 1

def create_coins():
    return [
        pygame.Rect(400, 350, 20, 20),
        pygame.Rect(150, 250, 20, 20),
        pygame.Rect(520, 150, 20, 20)
    ]