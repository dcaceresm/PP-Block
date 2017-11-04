from constants import *
class Variables:

    """clase que guarda las variables del juego"""

    def __init__(self):

        self.puntaje = 1 #Puntos del jugador
        self.extraBall = 0 #Cuantas bolas extra acumulo en un nivel determ.
        self.clic = True # Determina si se pueden lanzar o no las bolas.
        self.generar = True # Determina si se puede generar un nuevo nivel.
        self.canPlay = True # Condicion para seguir jugando.
        self.savedpos = False # Pregunta si se guardo la Posicion
                              # De la primera bola que cayo.
        self.initX = SWIDTH / 2 # Posicion desde donde se lanzan las bolas.
        self.counter = 0 # Contador para agregar las bolas extras
                         # al iniciar cada nivel.

    def addPoint(self):
        self.puntaje += 1

    def addBall(self):
        self.extraBall += 1

    def switchClic(self):
        self.clic = not self.clic

    def getPoint(self):
        return self.puntaje

    def getExBall(self):
        return self.extraBall

    def getClic(self):
        return self.clic

    # Reinicia las variables para iniciar una nueva partida.
    def reset(self):
        self.puntaje = 1
        self.extraBall = 0
        self.clic = True
        self.generar = True
        self.canPlay = True
        self.savedpos = False
        self.initX = SWIDTH / 2
        self.counter = 0
