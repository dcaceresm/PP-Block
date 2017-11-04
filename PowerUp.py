from constants import *
from centered_figure import *
import pygame
import copy




class PowerUp:

    def __init__(self,center,surface,tipo,fuente):
        self.center = center
        if tipo == 0: #LASER HORIZONTAL
            self.figure = CenteredFigure([(-10,10),(10,10),(10,-10),(-10,-10)],
            center = self.center,color = COLOR_LASER, pygame_surface = surface)
            self.texto = 'H'
        elif tipo == 1: #LASER VERTICAL
            self.figure = CenteredFigure(
                [(-10, 10), (10, 10), (10, -10), (-10, -10)],
                center=self.center, color=COLOR_LASER, pygame_surface=surface)
            self.texto = 'V'
        elif tipo == 2: #REBOTE ALEATORIO
            self.figure = CenteredFigure(
                [(-10, 10), (10, 10), (10, -10), (-10, -10)],
                center=self.center, color=COLOR_REBOTE, pygame_surface=surface)
            self.texto = 'R'
        elif tipo == 3: #BOLA EXTRA
            self.figure = CenteredFigure(
                [(-10, 10), (10, 10), (10, -10), (-10, -10)],
                center=self.center, color=COLOR_NEWBALL, pygame_surface=surface)
            self.texto = 'B'

        self.surface = surface
        self.tipo = tipo
        self.triggered = False
        self.fuente = fuente

    def getTipo(self):
        return self.tipo

    def getCenter(self):
        return self.center

    def draw(self):
        V = self.figure.get_vertices()
        self.figure.draw()
        text = self.fuente.render(self.texto,1,COLOR_BLACK)
        self.surface.blit(text,(self.center[0]-4,self.center[1]-15))

    def Trigger(self):
        # ACTIVA UN POWER UP PARA DESACTIVARLO AL AVANZAR DE NIVEL
        if not self.triggered:
            self.triggered = True

    def Status(self):
        return self.triggered
