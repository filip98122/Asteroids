import pygame
import math
import random
import time
pygame.font.init()
pygame.init()


my_font = pygame.font.SysFont('Comic Sans MS', 20)
window = pygame.display.set_mode((1000,1000),flags=pygame.SCALED, vsync=1) # Makes window
#pygame.Rect(p1.x,p1.y,p1.w,p1.h)
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
        pygame.draw.rect(window, pygame.Color("White"), pygame.Rect(self.x, self.y, self.width,self.height)) # Draws a rectangle
        
    def move(self):
        
        if self.x > 0:
            if keys[pygame.K_a] == False:
                if keys[pygame.K_LEFT]:
                    self.x -= self.speed
                
        if self.x < 850:
            if keys[pygame.K_d] == False:
                if keys[pygame.K_RIGHT]:
                    self.x += self.speed
                
        if self.x > 0:
            if keys[pygame.K_LEFT] == False:
                if keys[pygame.K_a]:
                    self.x -= self.speed
                
        if self.x < 850:
            if keys[pygame.K_RIGHT] == False:
                if keys[pygame.K_d]:
                    self.x += self.speed
                    
p1 = Player(500,900,150,25,5.5)
class Laser:
    def __init__(self,x,y,speed,width,height,color,health,direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self.health = health
        self.direction = direction
    def draw(self,window):
        pygame.draw.rect(window, pygame.Color(self.color), pygame.Rect(self.x, self.y,self.width,self.height))
        
    def move(self):
        self.y += self.direction*self.speed 
        
        
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

class Power:
    def __init__(self,x,y,rad,speed,width,height,health):
        self.x = x
        self.y = y
        self.rad = rad
        self.speed = speed
        self.width = width
        self.height = height
        self.health = health
        
    def draw(self,window):
        pygame.draw.circle(window, pygame.Color("Red"), (self.x,self.y), self.rad)
        #gray65
    def move(self):
        self.y += self.speed

class Shield:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self,window):
        pygame.draw.rect(window, pygame.Color("cadetblue2"), (self.x,self.y,self.width,self.height))
        
clock = pygame.time.Clock()
shield = Shield(p1.x,p1.y -32.5,170,20)

shield_rect = pygame.Rect(shield.x,shield.y,shield.width,shield.height)

l_lasers = []
for i in range(0):
    laser = Laser(p1.x - 25, p1.y - 25,7.5,20,80,pygame.Color("floralwhite"),2,-1)
    l_lasers.append(laser)

player_rect = pygame.Rect(p1.x, p1.y, p1.width,p1.height)

l_powers = []
    
l_asteroids = []
asteroid = Asteroid(random.randint(60,940),random.randint(30,65),4.5,0,60,120,120,1)
l_asteroids.append(asteroid)

a = 1
cooldown = 30


def colision1(rect1 : pygame.Rect,rect2):
    if rect1.colliderect(rect2):
        return True
    return False

shielddraw = 0

while True:
    window.fill("Blue" ) # Resets window
    keys = pygame.key.get_pressed()
    
    shield.x = p1.x-10
    shield.y = p1.y-50
    
    if keys[pygame.K_ESCAPE]:
        exit()
    ranpower = random.randint(0,5750)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    #moves player
    p1.move()
    if keys[pygame.K_SPACE]:
        if cooldown <= 0:
            cooldown = 30
            shoot = 1
            new_laser = Laser(p1.x + p1.width / 2, p1.y,7.5,20,80,pygame.Color("floralwhite"),1,-1)
            l_lasers.append(new_laser)
    for laser in l_lasers:
        if laser.health >= 1:
            laser.move()
            laser.draw(window)
            
            
    for laser in l_lasers:        
        if laser.y <= 40 or laser.health <= 0:
            l_lasers.remove(laser)
    
    for asteroid in l_asteroids:
        if asteroid.health >= 1:
            asteroid.move()
    ranasteroid = random.randint(0,4000)
    if ranasteroid <= 100:
        asteroid = Asteroid(random.randint(60,940),random.randint(30,65),4.5,0,60,120,120,1)
        l_asteroids.append(asteroid)
    

    if ranpower <= 10:
        power = Power(random.randint(60,940),random.randint(30,65),60,4.5,120,120,1)
        l_powers.append(power)   

    #Update and draw all powers
    for power in l_powers:
        power.health = 1
        rect_power = pygame.Rect(power.x - power.width / 2,power.y - power.height / 2,
        power.width, power.height)
        for laser in l_lasers:
            rect_laser =  pygame.Rect(laser.x,laser.y,laser.width,laser.height)
            
            if colision1(rect_power,rect_laser) == True:
                power.health -= 1
                laser.health -= 1
                shielddraw = 1
        if power.health == 1:
            power.move()
    
    #delets dead powers
    for power in l_powers:
        if power.health <= 0:
            l_powers.remove(power)
    for asteroid in l_asteroids:
        rect_asteroid = pygame.Rect(asteroid.x - asteroid.width / 2,asteroid.y - asteroid.height / 2,
        asteroid.width, asteroid.height)
    
        player_rect = pygame.Rect(p1.x, p1.y, p1.width,p1.height)    
        if colision1(player_rect,rect_asteroid):
            exit()
    
    if shielddraw == 1:
        shield.draw(window)
    
    for asteroid in l_asteroids:
        rect_asteroid = pygame.Rect(asteroid.x - asteroid.width / 2,asteroid.y - asteroid.height / 2,
        asteroid.width, asteroid.height)
        shield_rect = pygame.Rect(shield.x,shield.y,shield.width,shield.height)
        if shielddraw == 1:
            if colision1(shield_rect,rect_asteroid) == True:
                shielddraw = 0
                l_asteroids.remove(asteroid)
        
    # Update and draw all asteroids
    for asteroid in l_asteroids:
        rect_asteroid = pygame.Rect(asteroid.x - asteroid.width / 2,asteroid.y - asteroid.height / 2,
        asteroid.width, asteroid.height)

        for laser in l_lasers:
            rect_laser =  pygame.Rect(laser.x,laser.y,laser.width,laser.height)
 
            if colision1(rect_asteroid,rect_laser) == True:
                asteroid.health -= 1
                laser.health -= 1
                
        if asteroid.health >= 1:
            asteroid.draw(window)
        
    # Delete asteroids that are dead
    for asteroid in l_asteroids:
        if asteroid.y >= 1060 or asteroid.health <= 0:
            l_asteroids.remove(asteroid)
            
    #draws player
    p1.draw(window)
    for power in l_powers:
        if power.health == 1:
            power.draw(window)
    
    for power in l_powers:
        power.draw(window)
    
    cooldown -= 1
    #time.sleep(0.1)
    pygame.display.update() # Updates window
    clock.tick(60)