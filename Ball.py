# coding=utf-8
import pygame
import random
import math
from centered_figure import *
from constants import *


class Ball:

    def __init__(self,center,surface,blocks,pUps, sounds,variables,tipo):

        ### INICIALIZACION DE VARIABLES:
        self.tipo = tipo
        self.center = center
        self.blocks = blocks
        self.pups = pUps
        self.sounds = sounds

        if tipo == 1: #NORMAL BALL
            color = COLOR_WHITE
            forma = [(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
        elif tipo == 2: #BEER BALL
            color = COLOR_ORANGE
            forma = [(-1,0),(-2,0),(-2,4),(2,4),(2,0),(1,0),(1,-3),(-1,-3)]
        elif tipo == 3: #HARDCORE BALL
            color = COLOR_RED2
            forma = [(0,-1),(1,0),(0,1),(-1,0)]

        self.figure = CenteredFigure(
            forma, center=self.center,
            color=color, pygame_surface=surface)
        self.figure.scale(3)
        self.variables = variables
        self.surface = surface
        self.vel = [0,0] #Define veloc. inicial de la bola
        self.accelerated = False #Define si la bola esta detenida o no

    def draw(self):
        """
        dibuja la figura
        """

        self.figure.draw()


    def setVel(self,tupla):
        # LE ENTREGA VELOCIDAD A UNA BOLA DEPENDIENDO DE LA POSICION EN QUE
        # SE HAGA CLIC CON EL MOUSE
        Y = self.center[1] - tupla[1]
        X = tupla[0] - self.center[0]
        B = math.atan2(Y,X)
        if self.tipo == 2: # SI LA BOLA ES BEER BALL SE LANZA EN SENTIDO CONTR.
            self.vel[0] = -math.cos(B)*5
        else:
            self.vel[0] = math.cos(B)*5
        self.vel[1] = -math.sin(B)*5

    def getSuelo(self):
        # DETERMINA SI UNA BOLA ESTA EN EL SUELO
        return self.center[1] == FLOOR_HEIGHT-3

    def move(self):
        # MUEVE LA PELOTA Y DETERMINA LA VARIACION DE SUS PARAMETROS EN CASO
        # DE QUE COLISIONE.
        self.center[0] = self.center[0] + self.vel[0]
        self.center[1] = self.center[1] + self.vel[1]

        # COLISION CON BORDES ::::::::::::::
        # BORDE SUPERIOR (TECHO)
        if self.center[1] < CEIL_HEIGHT:
            self.center[1] = CEIL_HEIGHT
            self.vel[1] *= -1
            self.sounds.wall()
        # BORDE INFERIOR (SUELO)
        if self.center[1] > FLOOR_HEIGHT-3:
            self.center[1] = FLOOR_HEIGHT-3
            self.vel[0] = 0
            self.vel[1] = 0
            self.sounds.wall()
            if not self.variables.savedpos:
                # GUARDA LA POSICION DE LA PRIMERA BOLA QUE TOCO EL SUELO
                self.variables.initX = self.center[0]
                self.variables.savedpos = True
        # BORDE IZQUIERDO:
        if self.center[0] < 0:
            self.center[0] = 0
            self.vel[0] *= -1
            self.sounds.wall()
        # BORDE DERECHO:
        if self.center[0] > SWIDTH - 3:
            self.center[0] = SWIDTH -3
            self.vel[0] *= -1
            self.sounds.wall()

        # COLISION CON BLOQUES ::::::::::::::

        for block in self.blocks:
            #REVISA PARA TODOS LOS BLOQUES SI COLISIONO CON ALGUNO.
            if self.figure.collide(block.figure):
                V = block.figure.get_vertices()
                # COLISIONA POR LA IZQUIERDA O LA DERECHA:
                if self.center[1]<V[1][1] and self.center[1]>V[2][1]:
                    self.vel[0] *= -1
                    self.sounds.pong()
                    # COLISIONA POR LA DERECHA
                    if self.center[0] > V[1][0]:
                        self.center[0] = V[1][0] + 6
                    # COLISIONA POR LA IZQUIERDA
                    elif self.center[0] < V[0][0]:
                        self.center[0] = V[0][0] - 6
                    # SI EL BLOQUE AUN TIENE PUNTOS DE RESISTENCIA, LE RESTA.
                    if block.getRes() > 1:
                        block.lowRes()
                        block.draw()
                        break
                    # SI YA NO QUEDAN PUNTOS DE RESISTENCIA, ELIMINA EL BLOQUE
                    # DEL JUEGO.
                    else:
                        self.blocks.remove(block)
                        break

                # COLISIONA POR ARRIBA O POR ABAJO:
                elif self.center[0]>V[0][0] and self.center[0]<V[1][0]:
                    self.vel[1] *= -1
                    self.sounds.pong()
                    # CHOCA POR ARRIBA:
                    if self.center[1] <= V[2][1]:
                        self.center[1] = V[2][1] - 7
                    # CHOCA POR ABAJO
                    elif self.center[1] >= V[0][1]:
                        self.center[1] = V[0][1] + 7
                    # ANALOGO AL CHOQUE ANTERIOR:
                    if block.getRes() > 1:
                        block.lowRes()
                        block.draw()
                        break
                    else:
                        self.blocks.remove(block)
                        break

        # COLISION CON POWERUPS :::::::::::::::::
        for pup in self.pups:
            if self.figure.collide(pup.figure):
                pup.Trigger() # "ACTIVA" EL POWERUP PARA ELIMINARLO AL AVANZAR
                              # EL NIVEL ACTUAL.
                if pup.getTipo() == 0: #LASER HORIZONTAL
                    C = pup.figure.get_center()
                    pygame.draw.line(self.surface, COLOR_LASER, [0,C[1]],
                                     [SWIDTH, C[1]], 3)
                    self.sounds.laser()
                    if self.tipo!= 3: # SI LA BOLA NO ES DE TIPO HARCORE:
                        for block in self.blocks:
                            if block.center[1] == C[1]:
                                # LE QUITA 1 PUNTO DE RESISTENCIA
                                # A CADA BLOQUE EN LA FILA DEL LASER.
                                if block.getRes() > 1:
                                    block.lowRes()
                                else:
                                    self.blocks.remove(block)
                    else:
                        self.pups.remove(pup)
                elif pup.getTipo() == 1: #LASER VERTICAL
                    # ANALOGO AL LASER HORIZONTAL, PERO AFECTA A BLOQUES
                    # EN SU MISMA COLUMNA
                    C = pup.figure.get_center()
                    pygame.draw.line(self.surface, COLOR_LASER,
                        [C[0],CEIL_HEIGHT],[C[0], FLOOR_HEIGHT],3)
                    self.sounds.laser()
                    if self.tipo!= 3:
                        for block in self.blocks:
                            if block.center[0] == C[0]:
                                if block.getRes() > 1:
                                    block.lowRes()
                                else:
                                    self.blocks.remove(block)
                    else:
                        self.pups.remove(pup)


                elif pup.getTipo() == 2: #REBOTE ALEATORIO
                    theta = math.radians(random.randint(45,135))
                    self.vel[0] = math.cos(theta)*5
                    self.vel[1] = -math.sin(theta)*5
                    if self.center[1]>pup.center:
                        self.center[1] += 20
                    else:
                        self.center[1] -= 20


                elif pup.getTipo() == 3: #BOLA EXTRA
                    self.pups.remove(pup)
                    # AGREGA UNA BOLA EXTRA, QUE SERA ADJUNTADA A LA LISTA
                    # DE BOLAS AL AVANZAR DE NIVEL.
                    self.variables.extraBall += 1
