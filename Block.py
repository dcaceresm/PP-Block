from constants import *
from centered_figure import *
import pygame
class Block:

    def __init__(self,center,surface,color,resistencia,fuente):
        self.center = center
        self.figure = CenteredFigure(
            [(-23, 23), (23, 23), (23, -23), (-23, -23)], center=self.center,
            color=color, pygame_surface=surface)
        self.resistencia = resistencia
        self.fuente = fuente
        self.surface = surface

    def draw(self):
        # METODO QUE DIBUJA EL BLOQUE EN PANTALLA
        V = self.figure.get_vertices()
        self.figure.draw()
        pygame.draw.rect(self.surface, COLOR_BLACK,(V[3][0]+2,V[3][1]+2,43,43))
        text = self.fuente.render(str(self.resistencia), 1, COLOR_WHITE)
        self.surface.blit(text,(self.center[0]-10,self.center[1]-10))

    def lowRes(self):
        # DISMINUYE EN UN PUNTO LA RESISTENCIA DEL BLOQUE
        self.resistencia -= 1

    def getRes(self):
        # ENTREGA LA RESISTENCIA DEL BLOQUE
        return self.resistencia
