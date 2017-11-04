# coding=utf-8
import pygame
from constants import *
class Sounds:

    def __init__(self):
        self._sound_pong = pygame.mixer.Sound(SND_PONG) # Sonido de rebote.
        self._sound_laser = pygame.mixer.Sound(SND_LASER) # Sonido de laser
        self._sound_bgm = pygame.mixer.Sound(SND_BGM) # Musica de fondo.

    def pong(self):
        self._sound_pong.play(0)

    def wall(self):
        self._sound_pong.play(0)

    def laser(self):
        self._sound_laser.play(0)

    def music(self):
        self._sound_bgm.play(-1)

    def music_stop(self):
        self._sound_bgm.stop()
