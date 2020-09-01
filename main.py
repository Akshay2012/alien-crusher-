import pygame
import random 
import math
from pygame import mixer

#Inititalize pygame
pygame.init()

#creating screen of width 800px and height 600px
screen= pygame.display.set_mode((800,600))

#BACKGROUND
background=pygame.image.load("bg.png")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1) # On loop

pygame.display.set_caption("Space Game")
icon=pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon) 

#(0,0) is top  left
#Player
playerImg=pygame.image.load("spaceship2.png")
playerX=380 
playerY=520

playerX_change=0
playerY_change=0.2

score=0


#Enemy
no_of_enemies=6
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change =[]
enemyY_change =[]

for x in range(no_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,720))
    enemyY.append(random.randint(0,300))
    enemyX_change.append(1.5)
    enemyY_change.append(40)



#Bullet
#Ready- bullet invisible
#fire - currently moving
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=520
bulletX_change=0
bulletY_change=4
bullet_state="ready"

font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10



#Game Over
game_over_font=pygame.font.Font('freesansbold.ttf',64)


#Displaying on screen


def game_over_text():  
    game_done=game_over_font.render("GAME OVER :"+str(score),True,(0,255,255))
    screen.blit(game_done,(300,300))



def show_score(x,y):
    score_val=font.render("Score :"+str(score),True,(0,255,255))
    screen.blit(score_val,(x,y))


def player(x,y):
    screen.blit(playerImg,(x,y))  #BLIT means to DRAW image


def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))  #BLIT means to DRAW image


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+15,y+10))

def iscollission(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(bulletX-enemyX,2)+math.pow(bulletY-enemyY,2)))
    if distance <15 :
        return True
    else :
        return False





#Everything that you think should be persistent goes in this loop.
#---GAME LOOP---GAME IS RUNNING----

running=True
while running:

    
    screen.fill((156,25,15))
    #Background Image
    screen.blit(background,(0,0))



    #Events -> closing button clicked, mouse moved,arrow keys/KeyStrokes pressed
    for event in pygame.event.get():


        #pressed quit button.
        if event.type==pygame.QUIT:
            running=False

        #Detects if any key is pressed 
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-3
                # print("Left Arrow Is pressed")

            if event.key==pygame.K_RIGHT:
                playerX_change=3

                # print("Right Arrow Is pressed")

            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX=playerX #Current X co ordinate.
                    fire_bullet(bulletX,bulletY)

        #Detects if key is released
        if event.type==pygame.KEYUP:
            
            if event.key==pygame.K_LEFT or  event.key==pygame.K_RIGHT:
                playerX_change=0
                playerX+=playerX_change
                # print("keystroke is released")
    

    playerX+=playerX_change
    #If it goes out of bound.
    if playerX<=0:
        playerX=800
    if playerX>800:
        playerX=0


    #Enemy Movement
    for i in range(no_of_enemies):
        
        
        if enemyY[i]>500:
            #Removing all enemies from the screen.
            for j in range(no_of_enemies):
                enemyY[j]=2000
            
            game_over_text()
            break
        
        enemyX[i]+=enemyX_change[i]
        
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]

        if enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        



        #Checking if bullet and enemy collided 
        collided=iscollission(enemyX[i],enemyY[i],bulletX,bulletY)
        if collided:
            explosion_sound=mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_state="ready"
            bulletY=520
            enemyY[i]=0
            score+=1
        
        enemy(enemyX[i],enemyY[i],i)





    #Bullet Movement
    if bulletY<=0:
        bullet_state="ready"
        bulletY=520

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change   #Moving Up


    player(playerX,playerY) 
    show_score(textX,textY)
    pygame.display.update() 


    
