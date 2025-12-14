import pygame
from classes_pl import Player, Enemy, create_coins, create_enemies, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, BLUE, RED, PINK, YELLOW, SPEED

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Полігон")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

SCORE = 0

player = Player(375, 450)

platforms = [
    pygame.Rect(300, 400, 200, 20),
    pygame.Rect(100, 300, 150, 20),
    pygame.Rect(500, 200, 100, 20)
]

coins = create_coins()
enemies = create_enemies()

running = True
while running:
    clock.tick(60)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_z:
                player.use_ryvok()


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
        player.facing_right = False
    if keys[pygame.K_RIGHT]:
        player.rect.x += current_speed
        player.facing_right = True
        

    for coin in coins[:]:
        if player.rect.colliderect(coin):
            coins.remove(coin)
            SCORE += 1
    

    for enemy in enemies:
        enemy.update()
        if player.rect.colliderect(enemy.rect):
            player.rect.x = 375
            player.rect.y = 450
            SCORE = 0
            coins = create_coins()

    if len(coins) == 0:
        coins = create_coins()

    player.update(platforms)


    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, 500, SCREEN_WIDTH, 100)) 

    if player.facing_right:
        current_image = player.image_right
    else:
        current_image = player.image_left
    screen.blit(current_image, (player.rect.x - 15, player.rect.y - 15))
    
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat)
        

    pygame.draw.rect(screen, BLACK, (20, 20, player.fuel, 20))
    
    for coin in coins:
        pygame.draw.rect(screen, YELLOW, coin)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy.rect)
        
    score_text = font.render(f"Score - {SCORE}", True, BLACK)
    screen.blit(score_text, (90, 90))
    
    pygame.display.flip()

pygame.quit()