import pygame
import math
import random
import time
pygame.font.init()
pygame.init()


my_font = pygame.font.SysFont('Comic Sans MS', 20)
window = pygame.display.set_mode((1000,1000),flags=pygame.SCALED, vsync=1) # Makes window

def collison(x1,y1,r1,x2,y2,r2):
    dx = x2 - x1
    dy = y2 - y1
    dist  = dx * dx + dy * dy
    dist = math.sqrt(dist)
    
    if dist > r1 + r2:
        return False
    else:
        return True

class Player:
    def __init__(self,x,y,width,height,speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
    def draw(self,window):
        pygame.draw.rect(window, pygame.Color("White"), pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, 125, 60)) # Draws a rectangle
        
    def move(self):
        
        if self.x > 87.5:
            if keys[pygame.K_a] == False:
                if keys[pygame.K_LEFT]:
                    self.x -= self.speed
                
        if self.x < 962.5:
            if keys[pygame.K_d] == False:
                if keys[pygame.K_RIGHT]:
                    self.x += self.speed
                
        if self.x > 87.5:
            if keys[pygame.K_LEFT] == False:
                if keys[pygame.K_a]:
                    self.x -= self.speed
                
        if self.x < 962.5:
            if keys[pygame.K_RIGHT] == False:
                if keys[pygame.K_d]:
                    self.x += self.speed

class Laser:
    def __init__(self,x,y,speed,width,height,color):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
    def draw(self,window):
        pygame.draw.rect(window, pygame.Color(self.color), pygame.Rect(self.x + self.width / 2, self.y + self.height / 2,self.width,self.height))
        
    def move(self):
        self.y -= self.speed
        
        
myColors = [pygame.Color("gray32"), pygame.Color("gray55"), pygame.Color("gray42")]

class Asteroid:
    def __init__(self,x,y,speed,active,rad,width,height,health):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = active
        self.rad = rad
        self.color = myColors[random.randint(0, len(myColors)-1)]
        self.width = width
        self.height = height
        self.health = health
        
    def draw(self,window):
        
        pygame.draw.circle(window, self.color, (self.x,self.y), self.rad)
        if self.health <= 0:
            return
    def move(self):
        if self.health <= 0:
            return
        self.y += self.speed

clock = pygame.time.Clock()
p1 = Player(500,900,175,25,5.5)

l_lasers = []
for i in range(1):
    laser = Laser(p1.x - 25, p1.y - 25,7.5,20,80,pygame.Color("floralwhite"))
    l_lasers.append(laser)

l_asteroids = []


a = 1
cooldown = 45


def colision1(rect1 : pygame.Rect,rect2):
    if rect1.colliderect(rect2):
        return True
    return False

while True:
    window.fill("Blue" ) # Resets window
    keys = pygame.key.get_pressed()
                
    if keys[pygame.K_ESCAPE]:
        exit()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    #moves player
    p1.move()
    if keys[pygame.K_SPACE]:
        if cooldown <= 0:
            cooldown = 45
            shoot = 1
            new_laser = Laser(p1.x - 25, p1.y - 25,7.5,20,80,pygame.Color("floralwhite"))
            l_lasers.append(new_laser)
    for i in range(len(l_lasers)):
        l_lasers[i].move()
        l_lasers[i].draw(window)
        if l_lasers[i].y == 40:
            del l_lasers[i]
    
    for asteroid in l_asteroids:
        if asteroid.health >= 1:
            asteroid.move()
    ranasteroid = random.randint(0,4000)
    if ranasteroid <= 100:
        asteroid = Asteroid(random.randint(60,940),random.randint(60,160),4.5,0,60,120,120,1)
        l_asteroids.append(asteroid)
    
    
    for asteroid in l_asteroids:
        rect_asteroid = pygame.Rect(asteroid.x - asteroid.width / 2,asteroid.y - asteroid.height / 2,
                            asteroid.width, asteroid.height)
        
        for laser in l_lasers:
            rect_laser =  pygame.Rect(l_lasers[i].x,l_lasers[i].y,l_lasers[i].width,l_lasers[i].height)
 
            if colision1(rect_asteroid,rect_laser):
                asteroid.health -= 1
        
        if asteroid.health >= 1:
            asteroid.draw(window)
        if asteroid.y >= 1060 or asteroid.health <= 0:
            del asteroid
    #draws player
    p1.draw(window)
    
    cooldown -= 1
    #time.sleep(0.1)
    pygame.display.update() # Updates window
    clock.tick(60)