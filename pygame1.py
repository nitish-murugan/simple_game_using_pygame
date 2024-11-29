import pygame
from pygame.locals import *
import sys

import pygame.tests

pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Game")

walkRight = [pygame.image.load("R1.png"),pygame.image.load("R2.png"),pygame.image.load("R3.png"),pygame.image.load("R4.png"),pygame.image.load("R5.png"),pygame.image.load("R6.png"),pygame.image.load("R7.png"),pygame.image.load("R8.png"),pygame.image.load("R9.png")]
walkLeft = [pygame.image.load("L1.png"),pygame.image.load("L2.png"),pygame.image.load("L3.png"),pygame.image.load("L4.png"),pygame.image.load("L5.png"),pygame.image.load("L6.png"),pygame.image.load("L7.png"),pygame.image.load("L8.png"),pygame.image.load("L9.png")]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
sound = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.isJump = False
        self.jumpCount = 10

        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        
        self.hitBox = (self.x + 10,self.y,40,70)
        

    def draw(self,win):
        if self.walkCount+1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitBox = (self.x+20,self.y+13,28,50)
        
    def hit(self):
        self.x = 10
        self.y = 350
        self.jumpCount = 10
        self.isJump = False
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans",50)
        text1 = font1.render('-5',1,(255,0,0))
        win.blit(text1,(200,250))
        pygame.display.update()
        i = 0
        while i <= 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    i = 301
                    pygame.quit
            
                
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x,self.end]
        self.walkCount = 0
        self.vel = 3
        
        self.hitBox = (self.x + 10,self.y,40,70)
        
        self.health = 10
        self.visible = True
        
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount+1 >= 33:
                self.walkCount = 0
            if self.vel < 0:
                win.blit(self.walkLeft[self.walkCount //3],(self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkRight[self.walkCount //3],(self.x,self.y))
                self.walkCount += 1
            self.hitBox = (self.x + 10,self.y,40,70)
            pygame.draw.rect(win,(255,0,0),(self.hitBox[0],self.hitBox[1]-20,50,10))
            pygame.draw.rect(win,(0,200,0),(self.hitBox[0],self.hitBox[1]-20,50-(5*(10-self.health)),10))
            #pygame.draw.rect(win,(255,0,0),self.hitBox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
            
    def hit(self):
        if self.health >0:
            self.health -= 1
        else:
            self.visible = False

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

def redrawScreen():
    win.blit(bg,(0,0))
    text = font.render("Score : "+str(score),1,(0,0,0))
    win.blit(text,(380,10))
    man.draw(win)
    ene.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

man = player(10,350,50,50)
ene = enemy(70,350,60,60,400)
shootLoop = 0
bullets = []
font = pygame.font.SysFont("comicsans",20,True)
while True:
    if ene.visible:
        if man.hitBox[1] < ene.hitBox[1] + ene.hitBox[3] and man.hitBox[1] + man.hitBox[3] > ene.hitBox[1]:
            if man.hitBox[0] + man.hitBox[2] > ene.hitBox[0] and man.hitBox[0] < ene.hitBox[0] + ene.hitBox[2]:
                man.hit()
                score -= 5
    else:
        ene = enemy(70,350,60,60,400)
    if shootLoop > 0:
        shootLoop+=1
    if shootLoop > 3:
        shootLoop = 0
    clock.tick(27)
    for event in pygame.event.get():
        if(event.type == QUIT):
            pygame.quit()
            sys.exit()
    for bullet in bullets:
        if(bullet.y + bullet.radius > ene.hitBox[1] and bullet.y - bullet.radius < ene.hitBox[1]+ ene.hitBox[3]):
            if(bullet.x + bullet.radius > ene.hitBox[0] and bullet.x - bullet.radius < ene.hitBox[0] + ene.hitBox[2]):
                ene.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        
        
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()
    
    if(keys[pygame.K_SPACE] and shootLoop == 0):
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2),round(man.y + man.height //2),6,(0,0,0),facing))
        
        shootLoop = 1
    if(keys[pygame.K_LEFT] and man.x > 5):
        man.x -= 5
        man.left = True
        man.right = False
        man.standing = False
    elif(keys[pygame.K_RIGHT] and man.x < 500-5-man.width):
        man.x += 5
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if(keys[pygame.K_UP]):
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else: 
            man.jumpCount = 10
            man.isJump = False
            
    redrawScreen()