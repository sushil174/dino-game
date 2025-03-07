import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png')
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png')
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png')
        self.image = self.player_walk[self.player_index]
        self.rect =  self.image.get_rect(midbottom = (80,300))  
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300 : self.rect.bottom = 300

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom  >= 300 : 
            self.gravity = -20
            self.jump_sound.play()

    def animation_state(self):
        if self.rect.bottom < 300 :
            self.image = self.player_jump
        else :
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk) : self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.apply_gravity()
        self.player_input()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else :
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect  = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames) : self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100 : self.kill()

def display():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    text = text_font.render(f'{current_time}',False,(64,64,64))
    text_rect = text.get_rect(center=(400,50))
    screen.blit(text,text_rect)
    return current_time

# def obstacle(obstacle_rect_list):
#     if obstacle_rect_list:
#         for obstacle_rect in obstacle_rect_list:
#             obstacle_rect.x -= 5
#             if obstacle_rect.bottom >= 300 : screen.blit(snail_surface,obstacle_rect)
#             else : screen.blit(fly_surface,obstacle_rect)
#         obstacle_rect_list = [obstacle_rect for obstacle_rect in obstacle_rect_list if obstacle_rect.x > -100]
#         return obstacle_rect_list
#     else : return []

# def player_animation() :
#     global player_index, player_surface
#     if player_rect.bottom < 300:
#         player_surface = player_jump
#     else :
#         player_index += 0.1
#         if player_index >= len(player_walk) : player_index = 0
#         player_surface = player_walk[int(player_index)]

# def collisions(player,obstacles):
#     if obstacles:
#         for rect in obstacles:
#             if player.colliderect(rect): return False
#     return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False) : 
        obstacle_group.empty()
        return False   
    else : return True

pygame.init()
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)
# player_gravity = 0
# obstacle_rect_list = []


#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf',50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# #snail
# snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_frames = [snail_frame_1,snail_frame_2]
# snail_frame_index = 0
# snail_surface = snail_frames[snail_frame_index]

# #fly
# fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
# fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
# fly_frames = [fly_frame_1,fly_frame_2]
# fly_frame_index = 0
# fly_surface = fly_frames[fly_frame_index]

# #player
# player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_1,player_walk_2]
# player_index = 0
# player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
# player_surface = player_walk[player_index]
# player_rect = player_surface.get_rect(midbottom = (80,300))

#intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = text_font.render("Pixel Runner",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,65))
intro_text = text_font.render("Press Space to run",False,(111,196,169))
intro_text_rect = intro_text.get_rect(center = (400,350))



#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# snail_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_timer, 500)

# fly_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_timer,200)


while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
        #     if event.type == pygame.KEYDOWN :
        #         if event.key == pygame.K_SPACE:
        #             if player_rect.bottom >= 300:
        #                 player_gravity = -20


        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if player_rect.collidepoint(event.pos):
        #             if player_rect.bottom >= 300:
        #                 player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                # if randint(0,2): obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1100),300)))
                # else : obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1100),210)))


            # if event.type == snail_timer :
            #     if snail_frame_index == 0 : snail_frame_index = 1
            #     else : snail_frame_index = 0
            #     snail_surface = snail_frames[snail_frame_index]

            # if event.type == fly_timer:
            #     if fly_frame_index == 0 : fly_frame_index = 1
            #     else: fly_frame_index = 0
            #     fly_surface = fly_frames[fly_frame_index]
        else :
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                game_active = True
                #obstacle_rect_list.clear()
                start_time = pygame.time.get_ticks()

            
        
    if game_active :
        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display()

        #player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300 : player_rect.bottom = 300
        # player_animation()
        player.draw(screen)
        player.update()


        obstacle_group.draw(screen)
        obstacle_group.update()
        # screen.blit(player_surface,player_rect)

        # #obstacle
        # obstacle_rect_list = obstacle(obstacle_rect_list)
       
        # #collision
        # game_active = collisions(player_rect,obstacle_rect_list)
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        # obstacle_rect_list.clear()
        # player_rect.midbottom = (80,300)
        # player_gravity = 0
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        score_text = text_font.render(f'Your Score : {score}',False,(111,196,169))
        score_text_rect = score_text.get_rect(center = (400,350))
        if score > 0 : screen.blit(score_text,score_text_rect)
        else : screen.blit(intro_text,intro_text_rect)
    pygame.display.update()
    clock.tick(60)
        