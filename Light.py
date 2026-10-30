import pygame # import
import random
import time
import math

pygame.init()

screen = pygame.display.set_mode((800, 600)) # set screen size
clock = pygame.time.Clock() # set clock
running = True

block = pygame.Rect(700,300,50,50)
background = pygame.Rect(0,0,800,600)

def movesteps(direction,amount,x,y):
    radians = math.radians(direction)
    return (x + amount * math.cos(radians),y + amount * math.sin(radians))

class Ray:
    def __init__(self,Dir,x,y):
        self.start = (x,y)
        self.x = x
        self.y = y
        self.medium = (self.start)
        self.end = ()
        self.dir = Dir
    
    def Rtick(self):
        self.medium = movesteps(
            self.dir, 20, self.medium[0], self.medium[1]
        )

        if block.collidepoint(self.medium) or not background.collidepoint(self.medium):
            self.end = self.medium
            return "STOP"

        self.end = self.medium
        return None

rays = []
ray1 = 0
for i in range(10):
    ray1 += 10
    rays.append(Ray(ray1,400,300))
    
while running: # start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    rays = []
    ray1 = 0
    for i in range(12):
        ray1 += 3
        rays.append(Ray(ray1,400,(300)))
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]: #movement/player conditioning
        block.y -= 3
    if keys[pygame.K_s]:
        block.y += 3
    if keys[pygame.K_a]:
        block.x -= 3
    if keys[pygame.K_d]:
        block.x += 3
    
    for i in rays:
        while i.Rtick() != "STOP":
            pass
    
    screen.fill((0,0,0)) 
    
    for i in rays:
        pygame.draw.line(screen,(255,255,255),(i.start),(i.end),3)
    
    pygame.draw.rect(screen,(255,255,255),block)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()