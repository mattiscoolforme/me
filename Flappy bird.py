import pygame
import random
import time 

pygame.init()

print(pygame.font.get_fonts())   

pygame.display.set_caption("FlappyBird")
running = True
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)

player = pygame.Rect(75,0,30,30)
Bird = pygame.image.load("Flappy bird.png").convert_alpha()
Bird = pygame.transform.scale(Bird,(45,45))
Bird = pygame.transform.flip(Bird,True,False)


velocity = 0
cooldown = 0
pipe_make = 0
Score = 0
Score_ = ""

def make_pipe():
    global pipe_make
    if pipe_make == 0:
        pipes.append(Pipe())
        pipe_make = 90
    
    if pipe_make > 0:
        pipe_make -= 1

class Pipe:
    def __init__(self):
        self.random = random.randint(150,450)
        self.bottomrect = pygame.Rect(850,(self.random),75,600)
        self.toprect = pygame.Rect(850,(self.random)-800,75,600)
        self.timer = 200
    
    def Ptick(self):
        global Score
        self.bottomrect.x -= 5
        self.toprect.x -= 5
        self.timer -= 1
        if self.timer ==0:
            pipes.remove(self)
            Score += 1

pipes = []

time.sleep(1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if cooldown == 0:
            velocity += 25
            cooldown = 14
    
    if cooldown > 0:
        cooldown -= 1
    
    player.y -= velocity
    velocity -= 1
    velocity *= 0.95  
    
    font.render(str(1*Score), True, (255, 0, 0))
    
    make_pipe()
    
    screen.fill((175, 175, 255))    
    pygame.draw.rect(screen,(255,255,0),player)
    screen.blit(Bird,(player.x-7,player.y-7))
    
    for i in pipes:
        pygame.draw.rect(screen,(0,175,0),i.bottomrect)
        pygame.draw.rect(screen,(0,175,0),i.toprect)
        i.Ptick()
        if i.bottomrect.colliderect(player) or i.toprect.colliderect(player):
            running = False
    Score_ = font.render(str(1*Score), True, (255, 0, 0))
    screen.blit(Score_,(400,0))
    
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
print(Score)