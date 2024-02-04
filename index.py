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

#tiempos de semaforos en verde
verde = {
    0 : 9,
    1 : 9,
    2 : 9,
    3 : 9
}
#tiempos de semaforos en rojo
rojo = 100
#tiempo en semaforos en amarillo
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

        else:
            self.stop = paradas[direction]

    

    #funcion para mover los autos
    def mover(self):

        if self.direccion == 'derecha':


            if(self.cruzo == 0 and self.image.x + self.image.width > paradas[self.direccion]):
                self.cruzo = 1
                #  *  ||    cruzo == 0
                #   * ||    cruzo == 0
                #     || *  cruzo == 1

            if((self.image.x + self.image.width <= self.stop or self.cruzo == 1 or (señalEnVerde == 0 and señalEnAmarillo == 0)) and 
               (self.i == 0 or self.image.x + self.image.width < (autos[self.direccion][self.carril][self.i - 1 ].image.x - 15))):
                self.image.x += self.velocidad

        elif self.direccion == 'abajo':


            if(self.cruzo == 0 and self.image.y + self.image.width > paradas[self.direccion]):
                self.cruzo = 1
                
            if((self.image.y + self.image.width <= self.stop or self.cruzo == 1 or (señalEnVerde == 1 and señalEnAmarillo == 0)) and 
               (self.i == 0 or self.image.y + self.image.width < (autos[self.direccion][self.carril][self.i - 1 ].image.y - 15))): 
                self.image.y += self.velocidad

        elif self.direccion == 'izquierda':


            if(self.cruzo == 0 and self.image.x + self.image.width < paradas[self.direccion]):
                self.cruzo = 1
            if((self.image.x >= self.stop or self.cruzo == 1 or (señalEnVerde == 2 and señalEnAmarillo == 0)) and 
               (self.i == 0 or self.image.x + self.image.width > (autos[self.direccion][self.carril][self.i - 1 ].image.x + autos[self.direccion][self.carril][self.i - 1].image.width + 15))):
                self.image.x -= self.velocidad

        
        elif self.direccion == 'arriba':
            if(self.cruzo == 0 and self.image.y + self.image.width < paradas[self.direccion]):
                self.cruzo = 1
            if((self.image.y >= self.stop or self.cruzo == 1 or (señalEnVerde == 3 and señalEnAmarillo == 0)) and 
               (self.i == 0 or self.image.y + self.image.width > (autos[self.direccion][self.carril][self.i - 1 ].image.y + autos[self.direccion][self.carril][self.i - 1].image.width + 15))):
                self.image.y -= self.velocidad


def inicializacionSemaforos():

    #crear semaforos
    S1 = Semaforos(verde[0],amarillo, rojo)
    señales.append(S1)
    S2 = Semaforos(verde[1], amarillo, rojo)
    señales.append(S2)
    S3 = Semaforos(verde[2], amarillo, rojo)
    señales.append(S3)
    S4 = Semaforos(verde[3], amarillo, rojo)
    señales.append(S4)



def cicloSemaforos():

    while(señales[señalEnVerde].verde > 0 ):
        temporizador()
        time.sleep(1)
    señalEnAmarillo = 1
    while(señales[señalEnVerde].amarillo > 0):
        temporizador()
        time.sleep(1)
    señalEnAmarillo = 0

    
    #estas lineas resetean los tiempos de los semaforos actuales
    señales[señalEnVerde].verde = verde[señalEnVerde]
    señales[señalEnVerde].amarillo = amarillo
    señales[señalEnVerde].rojo = rojo

    señalEnVerde = proximaVerde #cambia de semaforo actual 
    proximaVerde  = (señalEnVerde + 1) % numeroSemaforos #aumenta el valor para ir al proximo semaforo
    señales[proximaVerde].rojo = señales[señalEnVerde].amarillo + señalEnAmarillo[señalEnVerde].verde 
    
    cicloSemaforos()


def temporizador():
    for i in range(0, numeroSemaforos):
        if i == señalEnVerde:
            if señalEnAmarillo == 0:
                señales[i].verde -= 1
            else:
                señales[i].amarillo -= 1
        else:
            señales[i].rojo -= 1




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





























