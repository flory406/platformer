import pygame
from classes_pl import Player, create_coins, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, BLUE, RED, PINK, YELLOW, SPEED

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Полігон")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

SCORE = 0

player = Player(100, 300)

platforms = [
    pygame.Rect(300, 400, 200, 20),
    pygame.Rect(100, 300, 150, 20),
    pygame.Rect(500, 200, 100, 20)
]

coins = create_coins()

running = True
while running:
    clock.tick(60)
    
    # 1. ПОДІЇ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_z:
                player.use_ryvok()

    # 2. УПРАВЛІННЯ
    keys = pygame.key.get_pressed()
    player_color = BLUE
    current_speed = SPEED
    
    if player.ryvok_timer > 0:
        current_speed = 20
        player_color = BLACK
    elif keys[pygame.K_LSHIFT]:
        current_speed = 10
        player_color = RED
        
    if keys[pygame.K_UP]:
        player.use_jetpack()
        player_color = PINK
    if keys[pygame.K_LEFT]:
        player.rect.x -= current_speed
    if keys[pygame.K_RIGHT]:
        player.rect.x += current_speed
        
    # Збір монет
    for coin in coins[:]:
        if player.rect.colliderect(coin):
            coins.remove(coin)
            SCORE += 1

    if len(coins) == 0:
        coins = create_coins()

    # Оновлення фізики (передаємо список платформ!)
    player.update(platforms)

    # 3. МАЛЮВАННЯ
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, 500, SCREEN_WIDTH, 100)) # Земля
    pygame.draw.rect(screen, player_color, player.rect) # Гравець
    
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat)
        
    # Смужка палива
    pygame.draw.rect(screen, BLACK, (20, 20, player.fuel, 20))
    
    for coin in coins:
        pygame.draw.rect(screen, YELLOW, coin)
        
    score_text = font.render(f"Score - {SCORE}", True, BLACK)
    screen.blit(score_text, (90, 90))
    
    pygame.display.flip()

pygame.quit()