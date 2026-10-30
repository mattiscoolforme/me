import pygame # import
import random
import time

pygame.init() # always have to do to start
 
screen = pygame.display.set_mode((800, 600)) # set screen size
clock = pygame.time.Clock() # set clock

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
Money = 0
Hearts =  3
running = True
player = pygame.Rect(400, 300, 30, 60) # player arguments and rect
playerspeed = 3 # player speed
menu = False
menu_screen = pygame.Rect(50, 50, 700, 500)
Direction = "w"
bullet_cooldown = 0
zombie_spawn = 0
side = 0

Z_skin = pygame.image.load("Zombie.png").convert_alpha()
Z_skin = pygame.transform.scale(Z_skin,(30,60))

P_skin = pygame.image.load("Player.png").convert_alpha()
P_skin = pygame.transform.scale(P_skin,(30,60))

M_skin = pygame.image.load("Menu.png").convert_alpha()
M_skin = pygame.transform.scale(M_skin,(700,500))

BCKGRD = pygame.image.load("background.png").convert_alpha()
BCKGRD = pygame.transform.scale(BCKGRD,(800,600))

JUMPSCARE = pygame.image.load("jumpscare.png").convert_alpha()
JUMPSCARE = pygame.transform.scale(JUMPSCARE,(1200,600))

STARTUP = pygame.image.load("Startup.png").convert_alpha()
STARTUP = pygame.transform.scale(STARTUP,(800,600))
START = True

zombie_top_spawn = input("\nDifficulty: Easy/Medium/Hard (E/M/H)")
if zombie_top_spawn == "E":
    zombie_top_spawn = 125
elif zombie_top_spawn == "M":
    zombie_top_spawn = 55
elif zombie_top_spawn =="H":
    zombie_top_spawn = 25

print(Hearts)

font = pygame.font.Font(None, 50)
Heart_ = font.render("🟥"*Hearts, True, (0, 0, 0))

def clickrect(rectangle):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and rectangle.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False
    else:
        return False

def spawn():
    global zombie_spawn

    if zombie_spawn <= 0:
        x = 0
        y = 0
        side = random.randint(1, 4)

        if side == 1:
            y = 0
            x = random.randint(0, 800)
        elif side == 3:
            y = 600
            x = random.randint(0, 800)
        elif side == 2:
            y = random.randint(0, 600)
            x = 800
        elif side == 4:
            y = random.randint(0, 600)
            x = 0

        zombies.append(Zombie(x, y))
        zombie_spawn = zombie_top_spawn
    else:
        zombie_spawn -= 1

class Bullet:
    def __init__(self, x, y,):
        self.rect = pygame.Rect(player.x, player.y, 20, 20)
        self.direction = Direction
    
    def bmove(self):
        if self.direction =="w":
            self.rect.y -= 10
        elif self.direction =="s":
            self.rect.y += 10
        elif self.direction =="a":
            self.rect.x -= 10
        elif self.direction =="d":
            self.rect.x += 10

        for i in zombies:
            if self.rect.colliderect(i):
                pass

class Zombie: # class
    def __init__(self, x, y): # class arguments for x y
        self.rect = pygame.Rect(x, y, 30, 60)
        self.attack = 0
        self.health = 1
        self.sx = x
        self.sy = y
        self.dir = False 
    
    def zmove(self):# conditioning
        global Hearts
        if player.x > self.rect.x:
            self.rect.x +=1
        elif player.x < self.rect.x:
            self.rect.x -=1
          
        if player.y > self.rect.y:
            self.rect.y +=1
        elif player.y < self.rect.y:
            self.rect.y -=1

        if self.attack > 0:
            self.attack -= 1
        
        if self.rect.colliderect(player) and self.attack == 0:
            Hearts -=1
            print(Hearts)
            self.attack = 60
    
    def zdir(self):
        if self.rect.x < player.x:
            self.dir = False
        else:
            self.dir = True
    
    def zdeath(self):
        global Money
        for i in bullets:    
            if self.rect.colliderect(i):
                zombies.remove(self)
                Money += 1

zombies = [Zombie(0,0)]# zom (var) with class attribute
bullets = []

while running: # start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() # get the key thats pressed
    
    
    if not START:
        if not menu:
            if keys[pygame.K_w]: #movement/player conditioning
                player.y -= playerspeed
                Direction = "w"
            if keys[pygame.K_s]:
                player.y += playerspeed
                Direction = "s"
            if keys[pygame.K_a]:
                player.x -= playerspeed
                Direction = "a"
            if keys[pygame.K_d]:
                player.x += playerspeed
                Direction = "d"
            
            for i in zombies:
                i.zmove()
                i.zdeath()
                i.zdir()
            
            for i in bullets:
                i.bmove()
        
            spawn()
        
        if Direction == "a":
            P_skin = pygame.transform.flip(P_skin,True,False)        
        
        if keys[pygame.K_SPACE]:
            if bullet_cooldown == 0:
                bullets.append(Bullet(player.centerx,player.centery))
                bullet_cooldown = 30
        
        if keys[pygame.K_ESCAPE]:
            if menu:
                time.sleep(0.25)
                menu = False
            else:
                menu = True
                time.sleep(0.25)
        
        if bullet_cooldown > 0:
            bullet_cooldown -= 1
        
        screen.fill((255, 255, 255))
        screen.blit(BCKGRD,(0,0))
        screen.blit(P_skin,player)
        for i in zombies:
            Z_skin = pygame.transform.flip(Z_skin,i.dir,False)
            screen.blit(Z_skin,i.rect)
            if i.dir:
                Z_skin = pygame.transform.flip(Z_skin,i.dir,False)
        
        for i in bullets:
            pygame.draw.rect(screen,(100,100,100), i.rect)
        
        Heart_ = font.render("\u2665"*Hearts, True, (255, 0, 0))
        Money_ = font.render("Money: " + str(Money), True, (255, 255, 0))
        
        screen.blit(Heart_,(0,0)) 
        screen.blit(Money_,(100,0))
        
        if Hearts <= 0:
            print("Lose")
            running = False
  
    if menu:
        screen.blit(M_skin,(50,50))
    
    pygame.display.flip()

    if Direction == "a":
        P_skin = pygame.transform.flip(P_skin,True,False) 

    if START:
        screen.blit(STARTUP,(0,0))
    
    clock.tick(60)

print("Money:",Money)

screen = pygame.display.set_mode((1200,600))
running = True

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.blit(JUMPSCARE,(0,0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()