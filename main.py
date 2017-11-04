# coding=utf-8
import os
import sys
import random
import math
import pygame
from pygame.locals import *
from centered_figure import CenteredFigure
from constants import *
from Ball import *
from Sounds import *
from Block import *
from Variables import *
from PowerUp import *



def main():

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((SWIDTH,SHEIGHT))  #48*7 x 48*11
    pygame.display.set_caption("PPBlock")
    #Elementos para el funcionamiento del menu:
    menu_status = 0 # Menu Status
    key_pos = 0 # Posicion en el menu
    selected_ball = 1 #bola seleccionada

    #Listas que contienen a los elementos del juego:
    PUps = []
    Bolas = []
    Blocks = []

    # Posicion al hacer clic con el mouse
    POS = tuple()

    # Se inicializan las imágenes
    BACK_IMG = pygame.image.load(bckgrnd)
    bckmenu = pygame.image.load(bck_menu)
    PLAYER = pygame.image.load(fsjal)

    # Reloj para los FPS
    clock = pygame.time.Clock()

    # Sonidos y variables globales:
    snd = Sounds()
    var = Variables()

    # Fuentes
    font = pygame.font.Font(fuente,10)
    font_small = pygame.font.Font(fuente, 7)
    font_huge = pygame.font.Font(fuente, 36)
    cenX = 24
    cenY = CEIL_HEIGHT+72
    # Timer para el lanzamiento de las pelotas
    timer = 0


    #Variables de Texto para el Menu
    text_title = font_huge.render('PP-BLOCK!',1,COLOR_WHITE)
    text_selectball = font.render('BALL SELECT',1,COLOR_WHITE)
    text_standard_ball = font_small.render('NORMAL BALL: A REGULAR BOUNCY BALL',1,COLOR_WHITE)
    text_beer_ball = font_small.render('BEER BALL: LAUNCHES IN THE OPPOSITE DIRECTION',1,COLOR_ORANGE)
    text_hardcore_ball = font_small.render('HARDCORE BALL: SMALL, IGNORE LAZER POWERUPS',1,COLOR_RED2)
    text_play = font.render('Play Game',1,COLOR_WHITE)
    selector = font.render('...',1,COLOR_WHITE)
    instr1 = font_small.render('MOVE WITH THE UP/DOWN KEYS, SELECT WITH SPACE',1,COLOR_WHITE)
    instr2 = font_small.render("INSTRUCTIONS: USE THE MOUSE TO PLAY, ",1,COLOR_WHITE)
    instr3 = font_small.render("DON'T LET THE SQUARES TOUCH THE FLOOR",1,COLOR_WHITE)

    while True:
        clock.tick(60)
        keys = pygame.key.get_pressed() #Detecta las teclas presionadas.
        # Captura las acciones del usuario:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and menu_status == 1:
                if var.getClic():
                    POS = pygame.mouse.get_pos()
                    var.generar = False
                    for bola in Bolas:
                        bola.center[1] -= 4
                        bola.accelerated = False

                    allDown = False
                    var.clic = False
                    var.savedpos = False
                    print 'clic'
                    print 'Bloques: ',len(Blocks)
                    print 'PUPS: ',len(PUps)
                    print var.getClic()
            if keys[K_q]:
                if not var.canPlay:
                    menu_status = 0
                    snd.music_stop()
                    #Reset Variables
                    var.reset()
            if keys[K_UP]:
                key_pos -= 1
                key_pos = key_pos % 4
                snd.laser()
            if keys[K_DOWN]:
                key_pos += 1
                key_pos = key_pos % 4
                snd.laser()
            if keys[K_SPACE]:
                if menu_status == 0:
                    if key_pos > 0:
                        selected_ball = key_pos
                        snd.laser()
                    else:
                        #Inicia el juego:
                        snd.laser()
                        menu_status = 1
                        var.canPlay = True
                        snd.music()
                        Bolas.append(Ball([SWIDTH/2,FLOOR_HEIGHT-3],screen,Blocks,PUps,snd,var,selected_ball))
                        for i in range(7):
                            r = random.randint(1,4)
                            cen = [cenX,cenY]
                            if r == 1 or r == 2:
                                Blocks.append(Block(cen,screen,COLOR_RED,var.getPoint(),font))
                                cenX += 48
                                continue
                            if r == 3:
                                t = random.randint(0,3)
                                PUps.append(PowerUp(cen,screen,t,font))
                                cenX += 48
                                continue
                            else:
                                cenX += 48
                        cenX = 24
                        var.generar = False
                        allDown = True


        if menu_status == 0: #MAIN MENU
            screen.blit(bckmenu,(0,0))
            screen.blit(text_title,(SWIDTH/2-140,CEIL_HEIGHT-50))
            screen.blit(text_play,(SWIDTH/3-80,SHEIGHT/3))
            screen.blit(text_selectball,(SWIDTH/3-80, SHEIGHT/3+40))
            screen.blit(text_standard_ball,(SWIDTH/3-80,SHEIGHT/3+80))
            screen.blit(text_beer_ball,(SWIDTH/3-80,SHEIGHT/3+120))
            screen.blit(text_hardcore_ball,(SWIDTH/3-80,SHEIGHT/3+160))
            screen.blit(instr1,(SWIDTH/3-100,SHEIGHT/3+200))
            screen.blit(instr2,(SWIDTH/3-100,SHEIGHT/3+240))
            screen.blit(instr3,(SWIDTH/3-100,SHEIGHT/3+260))

            if key_pos == 0:
                screen.blit(selector,(SWIDTH/3-100,SHEIGHT/3))
            if key_pos == 1:
                screen.blit(selector,(SWIDTH/3-100,SHEIGHT/3+80))
            if key_pos == 2:
                screen.blit(selector,(SWIDTH/3-100,SHEIGHT/3+120))
            if key_pos == 3:
                screen.blit(selector,(SWIDTH/3-100,SHEIGHT/3+160))
            pygame.display.update()


        if menu_status == 1: #En juego
            timer += 1

            if not allDown:
                i = 0
                for bola in Bolas:
                    if bola.getSuelo():
                        i += 1
                        bola.center[0] = var.initX
                    if i == len(Bolas):
                        var.switchClic()
                        print 'ALLDOWN!!'
                        var.generar = True
                        print len(PUps)
                        print len(Bolas)
                        allDown = True

            if var.generar and var.clic:

                var.addPoint()
                Bolas.append(Ball([var.initX,FLOOR_HEIGHT-3],screen,Blocks,PUps,snd,var,selected_ball))
                counter = 0
                while counter < var.extraBall:
                    Bolas.append(Ball([var.initX,FLOOR_HEIGHT-3],screen,Blocks,PUps,snd,var,selected_ball))
                    counter += 1
                    continue
                var.extraBall = 0
                for block in Blocks:
                    block.center[1] += 48
                    continue
                for pup in PUps:
                    pup.center[1] += 48
                    if pup.Status():
                        PUps.remove(pup)
                    continue

                v = var.getPoint()
                if v % 10 == 0:
                    v *= 2
                    c = COLOR_NAVY
                else: c = COLOR_RED

                for i in range(7):
                    r = random.randint(1,4)
                    cen = [cenX,cenY]
                    if r == 1 or r == 2:
                        Blocks.append(Block(cen,screen,c,v,font))
                        cenX += 48
                        continue
                    elif r == 3:
                        t = random.randint(0,3)
                        PUps.append(PowerUp(cen,screen,t,font))
                        cenX += 48
                        continue
                    else:
                        cenX += 48
                cenX = 24
                var.generar = False



            for block in Blocks:
                # Determina la condicion de derrota
                if block.center[1] >= 410:
                    var.canPlay = False
            # El jugador perdio
            if not var.canPlay:
                screen.fill(COLOR_BLACK)
                gameover = font.render('GAME OVER :( ',1, COLOR_WHITE)
                points = font.render('You got '+str(var.getPoint())+' points.',1,COLOR_WHITE)
                press = font.render('Return to main menu [Q]',1,COLOR_WHITE)
                screen.blit(gameover, (SWIDTH / 2 - 50, SHEIGHT / 2 - 60))
                screen.blit(points, (SWIDTH / 2 - 80, SHEIGHT / 2 - 30))
                screen.blit(press, (SWIDTH / 2 - 80, SHEIGHT / 2 ))
                pygame.display.update()
            #El jugador aun no pierde:
            else:
                #Dibuja el fondo:
                screen.fill(COLOR_BLACK)
                screen.blit(BACK_IMG, (0, 10))
                pygame.draw.line(screen,COLOR_ORANGE,[0,CEIL_HEIGHT],[SWIDTH,CEIL_HEIGHT],2)
                pygame.draw.line(screen, COLOR_ORANGE, [0, FLOOR_HEIGHT],
                                 [SWIDTH, FLOOR_HEIGHT], 2)
                text = font.render('NIVEL: '+str(var.getPoint()), 1, COLOR_WHITE)
                screen.blit(text,(0,10))

                # Dibuja la guia de ser necesario
                if var.getClic():
                    X = var.initX
                    Y = FLOOR_HEIGHT
                    mx = pygame.mouse.get_pos()[0]
                    my = pygame.mouse.get_pos()[1]
                    pygame.draw.line(screen,COLOR_WHITE,[X,Y-3],[mx,my],2)
                # Acelera las bolas con un ligero retardo
                # para que no salgan todas juntas luego de cliquear.
                if timer%6 == 0 and not var.getClic():
                    for bola in Bolas:
                        if not bola.accelerated:
                            bola.setVel(POS)
                            timer = 0
                            bola.accelerated = True
                            break
                # Mueve las Bolas y las dibuja.
                for bola in Bolas:
                    bola.move()
                    bola.draw()
                    continue
                #Dibuja los Bloques
                for block in Blocks:
                    block.draw()
                    if block.getRes() < 1:
                        Blocks.remove(block)
                #Dibuja los PowerUps
                for pup in PUps:
                    if pup.center[1] >= 410:
                        PUps.remove(pup)
                    else:
                        pup.draw()
                #Dibuja la imagen que representa al jugador:
                screen.blit(PLAYER,(var.initX-24,FLOOR_HEIGHT-22))
                # Vuelca todo en la pantalla
                pygame.display.update()



#Inicia el Juego:---------------------------------------------------------------
main()
