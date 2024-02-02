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
    'derecha': {
        0: [], 
        1: [], 
        2: [], 
        'crossed': 0
        }, 
    'abajo': {
        0: [],
        1: [], 
        2: [], 
        'crossed': 0
        },
    'izquierda': {
        0: [], 
        1: [], 
        2: [], 
        'crossed': 0
        }, 
    'arriba': {
        0: [], 
        1: [], 
        2: [], 
        'crossed': 0
        }
}

numeroDireccion = {
    0: 'derecha', 
    1: 'abajo', 
    2: 'izquierda', 
    3: 'arriba'
    }

semaforoCoordenadas = [(530, 230), (810, 230), (810, 570), (530, 570)]

paradas = {
    'derecha': 500, 
    'izquierda': 810, 
    'arriba': 545, 
    'abajo': 320 
    }


class Semaforos:
    def __init__(self, verde, amarillo, rojo):
        self.verde = verde
        self.amarillo = amarillo
        self.rojo = rojo

def valoresIniciales():
    S1 = Semaforos(verde[0], amarillo = amarillo, rojo = 0)
    señales.append(S1)
    S2 = Semaforos(verde=verde[1], amarillo=amarillo, rojo= S1.rojo + S1.amarillo + S1.verde)
    señales.append(S1)

class Auto:
    def __init__(self, carril, direction): #carril en el que se generarar, direccion a la que ira
        self.carril = carril
        self.direccion = carril
        #coordenadas en las que se generarar
        self.x = x[direction][carril]
        self.y = y[direction][carril]
        self.velocidad = 0.25
        self.cruzo = 0
        self.image = pygame.Rect(self.x, self.y, 20, 20) #Rectangulo que representa el auto
        autos[direction][carril].append(self) #Esta linea almacenara el auto en el carril correspondiente 
        self.i = len(autos[direction][carril]) - 1


        #para determinar en que coordenada se debe parar el auto es necesario saber si hay mas autos en su carril
        #y si estos autos estan detenidos 
        if(len(autos[direction][carril]) > 1 and autos[direction][carril][self.i -1].cruzo == 0):

            if direction == 'derecha':
                self.stop = autos[direction][carril][self.i-1].stop - autos[direction][carril][self.i - 1].rect.width - 15
            if direction == 'izquierda':
                self.stop = autos[direction][carril][self.i-1].stop + autos[direction][carril][self.i - 1].rect.width + 15
            if direction == 'abajo':
                self.stop = autos[direction][carril][self.i-1].stop - autos[direction][carril][self.i - 1].rect.width - 15
            if direction == 'arriba':
                self.stop = autos[direction][carril][self.i-1].stop + autos[direction][carril][self.i - 1].rect.width + 15

        





        







# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLANCO)

    # Dibujar intersección con carriles grises


    # Dibujar rectángulos azules representando autos
   
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()





























