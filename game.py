import pygame
from sys import exit
from random import randint


def obstacles(obstacle_list):
    if obstacle_list : 
        for obstacle in obstacle_list :
            obstacle.left -= 6
            if obstacle.bottom >= 300 :
                screen.blit(snail_surf,obstacle)
            else : screen.blit(fly_surf,obstacle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else : return []

def display():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_text = text_font.render(f'Score : {score}',False,(64,64,64))
    score_text_rect = score_text.get_rect(center = (400,50))
    screen.blit(score_text,score_text_rect)
    return current_time


def collisions(player,obstacle_list) :
    if obstacle_list : 
        for obstacle in obstacle_list :
            if player.colliderect(obstacle) : return False
    return True

def player_animation():
    global player_index, player_surf
    if player_rect.bottom < 300:
        player_surf = player_jump
    else : 
        player_index += 0.1
        if player_index >= len(player_walk) : player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
gravity = 0
game_active = False
start_time = 0
score = 0
obstacle_list = []
#font 
text_font = pygame.font.Font('font/Pixeltype.ttf',50)

#player
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_surf  = player_walk[0]
player_rect = player_surf.get_rect(midbottom = (80,300))


#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_index = 0
snail_surf = snail_frames[snail_index]
snail_rect = snail_surf.get_rect(midbottom = (600,300))


#fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]
fly_rect = fly_surf.get_rect(midbottom = (600,210))

#intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = text_font.render("Pixel Runner",False,((111,196,169)))
game_name_rect = game_name.get_rect(center = (400,50))

game_msg = text_font.render("Press Space to start",False,((111,196,169)))
game_msg_rect = game_msg.get_rect(center = (400,350))

#background
sky = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()

#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,500)
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,200)

while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active : 
            if event.type ==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_rect.bottom >= 300: gravity = -20

            if event.type == obstacle_timer : 
                if randint(0,2) :  obstacle_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                else : obstacle_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),210)))

            if event.type == snail_timer :
                if snail_index == 0 : snail_index = 1
                else : snail_index = 0
                snail_surf = snail_frames[snail_index]

            if event.type == fly_timer :
                if fly_index == 0 : fly_index = 1
                else : fly_index = 0
                fly_surf = fly_frames[fly_index]

        else : 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                obstacle_list.clear()
                game_active = True



    if game_active : 


        #background
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))

        #score
        score = display()

        #player
        player_animation()
        screen.blit(player_surf,player_rect)
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= 300 : player_rect.bottom = 300

        #obstacles
        obstacle_list = obstacles(obstacle_list)
        game_active = collisions(player_rect,obstacle_list)

    else : 
        screen.fill((94,129,162))
        obstacle_list.clear()
        player_rect.bottom = 300
        screen.blit(player_stand,player_stand_rect)
        if score <= 0 : screen.blit(game_name,game_name_rect)
        else : 
            score_msg = text_font.render(f'Your Score : {score}',False,((111,196,169)))
            screen.blit(score_msg,game_name_rect)
        screen.blit(game_msg,game_msg_rect)

    pygame.display.update()
    clock.tick(60)