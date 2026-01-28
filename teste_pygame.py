import pygame, random
from pygame.locals import *
from os.path import expanduser

def on_grid_random():
    x = random.randint(0,450)
    y = random.randint(0,450)
    return (x//50 * 50, y//50 * 50)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Flash Run')


#Restart Function
def restart_game():
    restart_font = pygame.font.Font('freesansbold.ttf',50)
    restart_screen = restart_font.render('Press Space to Restart', True, (100, 100, 100))
    restart_rect = restart_screen.get_rect()
    restart_rect.midtop = (250, 250)
    
    screen.blit(restart_screen, restart_rect)
    
    while True:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game()
                    
        pygame.display.update()  
              
#The game itself
def start_game():
    snake = [(200, 200),(210, 200), (220, 200)]
    snake_skin = pygame.Surface((50,50))
    snake_skin.fill((34,139,34))
    snake_speed = 5

    food_pos = on_grid_random()
    food = pygame.Surface((50,50))
    food.fill((255,0,0))

    my_direction = LEFT

    font = pygame.font.Font('freesansbold.ttf', 18)

    game_over = False

    while not game_over:
        clock.tick(snake_speed)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            #Movements Commands 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and my_direction != DOWN:
                    my_direction = UP
                if event.key == pygame.K_DOWN and my_direction != UP:
                    my_direction = DOWN
                if event.key == pygame.K_LEFT and my_direction != RIGHT:
                    my_direction = LEFT
                if event.key == pygame.K_RIGHT and my_direction != LEFT:
                    my_direction = RIGHT
        
        #Adding points, speed and the new part of the snake        
        if collision(snake[0], food_pos):
            food_pos = on_grid_random()
        
            
        # Check if Flash has collided with the wall
        if snake[0][0] == 500 or snake[0][1] == 500 or snake[0][0] < 0 or snake [0][1] < 0:
            mur = True
            break
        
        if game_over:
            break

        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])

        #Flash movements 
        if my_direction ==  UP:
            snake[0] = (snake[0][0], snake[0][1] - 50)
        if my_direction ==  DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 50)
        if my_direction ==  RIGHT:
            snake[0] = (snake[0][0] + 50, snake[0][1])
        if my_direction ==  LEFT:
            snake[0] = (snake[0][0] - 50, snake[0][1])            
                
        screen.fill((0,0,0))
        screen.blit(food, food_pos)
        
        # Draw horizontal lines
        for x in range(0, 500, 50): 
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 500))
        # Draw vertical lines
        for y in range(0, 500, 50): 
            pygame.draw.line(screen, (40, 40, 40), (0, y), (500, y))
        
        
        for pos in snake: 
            screen.blit(snake_skin, pos)
                
        pygame.display.update()
        
    while True:
        #Displaying Game Over
        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render('Game Over', True, (255,255,255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 / 2, 100)
        
        screen.blit(game_over_screen, game_over_rect)
        restart_game()
        pygame.display.update()
        pygame.time.wait(500)
        
        
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
start_game()