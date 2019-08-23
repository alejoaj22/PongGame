# -*- coding: utf-8 -*-
import pygame
import cv2
import numpy as np
#from paddle import Paddle
#from ball import Ball
from datetime import datetime
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
VIOLET = (70,40,130)
file = "Log.txt"


class Ball(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        super().__init__()
        #rellena la superficie de la bola donde se va a dibujar con negro
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # dibula la bola como un rectangulo
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        #
        self.velocity = [randint(4,8),randint(-8,8)]
        
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
          
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)



class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
          self.rect.y = 400


def savelog(message):
    f=open(file, "a+")
    f.write("%s Time: %s\n" % (message, datetime.now()))
    f.close()



def main():
    
    ancho = 919
    alto = 541
    camera = cv2.VideoCapture(0)
    camera.set(3, ancho)
    camera.set(4,alto)
    pygame.display.set_caption("Pong Game Portable")
    screen = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
    
    Barra1 = Paddle(RED, 10, 200)
    Barra1.rect.x = 20
    Barra1.rect.y = 200
    
    
    Barra2 = Paddle(VIOLET, 10, 200)
    Barra2.rect.x = ancho-20
    Barra2.rect.y = 200
    
    
    bola = Ball(WHITE,15,15)
    bola.rect.x = ancho/2
    bola.rect.y = alto/2
    
    lista_objetos = pygame.sprite.Group()
    
    lista_objetos.add(Barra1)
    lista_objetos.add(Barra2)
    lista_objetos.add(bola)
    
    #Verdes:
    #jugador1_bajos = np.array([51,9,0])
    #jugador1_altos = np.array([125, 119, 100])
    jugador1_bajos = np.array([65,62,0]) #ESTA AL REVES ES SVH y es la azul
    jugador1_altos = np.array([141, 217, 255])
    #Azules:
    jugador2_bajos = np.array([40,81,0]) #jugador 2 es el verde
    jugador2_altos = np.array([67, 173, 255])
    
    
    
    width = camera.get(3)  # float
    height = camera.get(4) # float
    kernel = np.ones((5,5),np.uint8)
    scoreA = 0
    scoreB = 0
    
    cy1 = 0
    cy2 = 0
    f=open(file, "a+")
    f.write('Start Game. Recorded at: %s\n' %datetime.now())
    f.close()
    
    carryOn = True
    
    
    
    
    
    while carryOn:
        
            pygame.init()
            
            screen.fill([0,0,0])
            
            
            
            ret, frame = camera.read()
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
           
            screen.fill([0,0,0])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            
            
            mascara_jugador1 = cv2.inRange(hsv, jugador1_bajos, jugador1_altos)
            mascara_jugador2 = cv2.inRange(hsv, jugador2_bajos, jugador2_altos)
            
            mascara_jugador1 = cv2.erode(mascara_jugador1,kernel,iterations = 4)
            mascara_jugador2 = cv2.erode(mascara_jugador2,kernel,iterations = 4)
            
            mascara_jugador1 = cv2.dilate(mascara_jugador1,kernel,iterations = 8)
            mascara_jugador2 = cv2.dilate(mascara_jugador2,kernel,iterations = 4)
    
    
            im1, contours1, hierarchy1 = cv2.findContours(mascara_jugador1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
               # Sort by area (keep only the biggest one)
            contour1 = sorted(contours1, key=cv2.contourArea, reverse=True)[:1]
            if len(contour1) > 0:
                 M1 = cv2.moments(contour1[0])
                 # Centroid
                 cx1 = int(M1['m10']/M1['m00'])
                 cy1 = int(M1['m01']/M1['m00'])
                 cv2.circle(mascara_jugador1, (cx1, cy1), 7, (0, 255, 0), -1)
                 
            im2, contours2, hierarchy2 = cv2.findContours(mascara_jugador2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
               # Sort by area (keep only the biggest one)
            contour2 = sorted(contours2, key=cv2.contourArea, reverse=True)[:1]
            
            if len(contour2) > 0:
                 M2 = cv2.moments(contour2[0])
                 # Centroid
                 cx2 = int(M2['m10']/M2['m00'])
                 cy2 = int(M2['m01']/M2['m00'])
                 cv2.circle(mascara_jugador2, (cx2, cy2), 7, (0, 255, 0), -1)
            
            if cy1 < Barra1.rect.y-20 and cy1 > Barra1.rect.y+20:
                Barra1.rect.y = cy1
                savelog("Player1: Stay")
            elif cy1 < Barra1.rect.y:
                Barra1.moveUp(10)
                savelog("Player1: Move Up")
            elif cy1 > Barra1.rect.y:
                Barra1.moveDown(10)
                savelog("Player1: Moove Down")
                
                
                
            if cy2 < Barra2.rect.y-20 and cy2 > Barra2.rect.y+20:
                Barra2.rect.y = cy2
                savelog("Player2: Stay")
            elif cy2 < Barra2.rect.y:
                Barra2.moveUp(5)
                savelog("Player2: Move Up")
            elif cy2 > Barra2.rect.y:
                Barra2.moveDown(5)
                savelog("Player2: Move Down")
            
            #cv2.imshow('frame',hsv)
            #cv2.imshow('Mascara jugador1',mascara_jugador1)
            #cv2.imshow('Mascara jugador2',mascara_jugador2)
    
            if bola.rect.x>=ancho-10:
                scoreA+=1
                savelog("Player1: Score")
            
                bola.rect.x = ancho/2
                bola.rect.y = alto/2
                bola.velocity[0] = -bola.velocity[0]
            if bola.rect.x<=0:
                scoreB+=1
                savelog("Player2: Score")
                bola.rect.x = ancho/2
                bola.rect.y = alto/2
                bola.velocity[0] = -bola.velocity[0]
            if bola.rect.y>alto-10:
                bola.velocity[1] = -bola.velocity[1]
            if bola.rect.y<0:
                bola.velocity[1] = -bola.velocity[1]     
         
            
            
            #Detect collisions between the ball and the paddles
            if pygame.sprite.collide_mask(bola, Barra1) or pygame.sprite.collide_mask(bola, Barra2):
              bola.bounce()
              
            lista_objetos.update()
            
            lista_objetos.draw(screen)
            screen.blit(frame, (0,0))
            
            
            
    
            #Dibuja la linea central
            pygame.draw.line(screen, WHITE, [ancho/2, 0], [ancho/2, alto], 5)
            font = pygame.font.Font(None, 74)
            text = font.render(str(scoreA), 1, WHITE)
            screen.blit(text, ((ancho/3) ,10))
            text = font.render(str(scoreB), 1, WHITE)
            screen.blit(text, (ancho*(3/4),10))
            lista_objetos.draw(screen) 
            pygame.display.update()
    
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                      carryOn = False # Flag that we are done so we exit this loop
                elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_x: #Pressing the x Key will quit the game
                             carryOn=False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)
                    width, height = event.size
                    ancho = width
                    alto = height
                    camera.set(3, width)
                    camera.set(4,height)
                    Barra2.rect.x = ancho-20
    pygame.quit()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()              

