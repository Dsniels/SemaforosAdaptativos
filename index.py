import pygame
import sys
import random
import threading
import time

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Tráfico")

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
GRIS = (169, 169, 169)

verde = {
    0 : 9,
    1 : 9,
    2 : 9,
    3 : 9
}

rojo = 100

amarillo = 3

numeroSemaforos = 4

señales=[]
señalEnVerde = 0
proximaVerde = (señalEnVerde + 1) % numeroSemaforos
señalEnAmarillo = 0





# Coordenadas de creacion de los autos
x = {
    'derecha': [0, 0, 0], 
    'abajo': [755, 727, 697], 
    'izquierda': [1400, 1400, 1400], 
    'arriba': [602, 627, 657]
    }
y = {
    'derecha': [348, 370, 398], 
    'abajo': [0, 0, 0], 
    'izquierda': [498, 466, 436], 
    'arriba': [800, 800, 800]
    }

autos = {
    'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
    'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}
}

numeroDireccion = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

semaforoCoordenadas = [(530, 230), (810, 230), (810, 570), (530, 570)]

paradas = {
    'rigth': 500, 
    'left': 810, 
    'arriba': 545, 
    'abajo': 320 
    }

