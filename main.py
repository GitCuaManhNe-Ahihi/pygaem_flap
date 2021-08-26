import pipes
import random
import pygame,sys
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.init()
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))
def creat_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (432,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(432, random_pipe_pos-650))
    return bottom_pipe,top_pipe
def delete_pipe(pipes):
        if len(pipes)>3 and pipes[0].centerx <= 0 :
            pipes.pop(0)
        return pipes
def rotate_bird(bird):
    bird_rote = pygame.transform.rotozoom(bird,bird_movement*2,1)
    return bird_rote
def move_of_pipe(pipes) :
     for pipe in pipes:
         pipe.centerx -=5
     return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_react.colliderect(pipe) or (bird_react.top <= -75 or bird_react.bottom >=650):
            hit.play()
            return False
    return True
def caculator_grade(pipes):
    soccer =0
    for pipe in pipes :
        if bird_react.centerx == pipe.centerx:
            soccer+=1
    return soccer
def soccer_display(dis):
    if dis:
        score_surface = g_font.render('Soccer: '+str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (200,50))
        screen.blit(score_surface,score_rect)
    else:
        score_surface = g_font.render('Soccer: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(200, 50))
        screen.blit(score_surface, score_rect)
        hight_score_surface = g_font.render('Hight_Soccer: ' + str(hight_score), True, (255, 255, 255))
        hight_score_rect = hight_score_surface.get_rect(center=(200, 620))
        screen.blit(hight_score_surface, hight_score_rect)
def scale2xpy(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale2x(img)
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
#tao bien
grav = 0.25
bird_movement = 0
score = 0
hight_score = 0
flap = pygame.mixer.Sound('sound/sfx_wing.wav')
point = pygame.mixer.Sound('sound/sfx_point.wav')
hit = pygame.mixer.Sound('sound/sfx_hit.wav')
mess = pygame.mixer.Sound('sound/sfx_swooshing.wav')

game_active = True
soccer = 0
g_font = pygame.font.Font('04B_19.TTF',40)
count_down =100
mess_screen = scale2xpy('assets/message.png')
mess_rect = mess_screen.get_rect(center=(216,384))

action_bird = ['assets/yellowbird-downflap.png','assets/yellowbird-midflap.png','assets/yellowbird-upflap.png']
bg = scale2xpy('assets/background-night.png')
floor = scale2xpy('assets/floor.png')
floor_x_pos = 0 #tọa độ sàn
bird = scale2xpy(action_bird[0])
bird_react =bird.get_rect(center=(100,384))
pipe_surface= scale2xpy('assets/pipe-green.png')
#tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,3000)
pipe_list=[]
pipe_height =[200,300,400]
#song

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                flap.play()
                bird_movement=0
                bird_movement =-11
                bird = scale2xpy(action_bird[1])
                bird = scale2xpy(action_bird[0])

            if event.key == pygame.K_SPACE and game_active == False:
                bird_react.center = (100, 384)
                game_active=True
                pipe_list.clear()
                score=0
                mess.stop()

        if event.type == pygame.KEYUP:
            bird = scale2xpy(action_bird[1])
            bird = scale2xpy(action_bird[2])
            flap.stop()
        if event.type == spawnpipe:
            pipe_list.extend(creat_pipe())

    if bird_react.centery < 30:
        bird_react.centery = 30
    screen.blit(bg,(0,0))
    if game_active:
        bird_movement+=grav
        rotated_bird = rotate_bird(bird)
        bird_react.centery += bird_movement
        screen.blit(rotated_bird,bird_react)
        pipe_list = move_of_pipe(pipe_list)
        draw_pipes(pipe_list)
        pipe_list = delete_pipe(pipe_list)
        score+=0.01
        if count_down ==0:
            point.play()
            count_down=100
        count_down-=1
        point.stop()
        soccer_display(game_active)
        game_active = check_collision(pipe_list)
    else:
        mess.play()
        screen.blit(mess_screen,mess_rect)
        if int(score) > int(hight_score):
            hight_score = int(score)
        soccer_display(game_active)
    if(floor_x_pos == -432):
        floor_x_pos=0
    floor_x_pos-=1
    draw_floor()
    pygame.display.update()
    clock.tick(120)