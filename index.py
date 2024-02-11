import pygame
import sys
import random
import threading
import time


# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
GRIS = (169, 169, 169)
carrilLleno = {
     0 : 0,
     1 : 0,
     2 : 0,
     3 : 0,

}
#tiempos de semaforos en verde
verde = {
    0 : 5,
    1 : 5,
    2 : 5,
    3 : 5
}
#tiempos de semaforos en rojo
rojo = 100
#tiempo en semaforos en amarillo
amarillo = 5
maximo = max(carrilLleno, key=carrilLleno.get)
numeroSemaforos = 4
fila = [maximo]
señales=[]
señalEnVerde = 0
proximaVerde = fila[0]
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
        'cruzo': 0
        }, 
    'abajo': {
        0: [],
        1: [], 
        2: [], 
        'cruzo': 0
        },
    'izquierda': {
        0: [], 
        1: [], 
        2: [], 
        'cruzo': 0
        }, 
    'arriba': {
        0: [], 
        1: [], 
        2: [], 
        'cruzo': 0
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
    'derecha': 590, 
    'izquierda': 800, 
    'arriba': 535, 
    'abajo': 330 
    }
defaultStop = {'derecha': 540, 'abajo': 280, 'izquierda': 810, 'arriba': 545}



# Inicializar Pygame
pygame.init()
simulacion = []

class Semaforos:
    def __init__(self, verde, amarillo, rojo):
        self.verde = verde
        self.amarillo = amarillo
        self.rojo = rojo



class Auto:
    def __init__(self, carril, direction): #carril en el que se generarar, direccion a la que ira
        self.carril = carril
        self.direccion = direction
        #coordenadas en las que se generarar
        self.x = x[direction][carril]
        self.y = y[direction][carril]
        self.velocidad = 1.5
        self.cruzo = 0
        self.image = pygame.Rect(self.x, self.y, 20, 20) #Rectangulo que representa el auto
        autos[direction][carril].append(self) #Esta linea almacenara el auto en el carril correspondiente 
        self.i = len(autos[direction][carril]) - 1


        #para determinar en que coordenada se debe parar el auto es necesario saber si hay mas autos en su carril
        #y si estos autos estan detenidos 
        if(len(autos[direction][carril]) > 1 and autos[direction][carril][self.i -1].cruzo == 0):

            if direction == 'derecha':
                self.stop = autos[direction][carril][self.i-1].stop - autos[direction][carril][self.i - 1].image.width - 15
            elif direction == 'izquierda':
                self.stop = autos[direction][carril][self.i-1].stop + autos[direction][carril][self.i - 1].image.width + 15
            elif direction == 'abajo':
                self.stop = autos[direction][carril][self.i-1].stop - autos[direction][carril][self.i - 1].image.height- 15
            elif direction == 'arriba':
                self.stop = autos[direction][carril][self.i-1].stop + autos[direction][carril][self.i - 1].image.height+ 15

        else:
            self.stop = defaultStop[direction]

        if direction == 'derecha':
             temp = self.image.width + 15
             x[direction][carril] -= temp
        elif direction == 'izquierda':
             temp = self.image.width + 15
             x[direction][carril] += temp
        elif direction == 'abajo':
             temp = self.image.height + 15
             y[direction][carril] -= temp
        elif direction == 'arriba':
             temp = self.image.height + 15
             y[direction][carril] += temp

        simulacion.append(self)

    

    #funcion para mover los autos
    def mover(self):

        if self.direccion == 'derecha':
            
            if (self.cruzo == 0 and self.image.x + self.image.width > paradas[self.direccion]):
                self.cruzo = 1
                
            if ((self.image.x + self.image.width <= self.stop or self.cruzo == 1 or (
                    señalEnVerde == 0 and señalEnAmarillo == 0)) and (
                    self.i == 0 or self.image.x + self.image.width < (
                    autos[self.direccion][self.carril][self.i - 1].image.x - 15))):

                                self.image.x += self.velocidad


        elif self.direccion == 'abajo':

            if (self.cruzo == 0 and self.image.y + self.image.height > paradas[self.direccion]):
                self.cruzo = 1



            if ((self.image.y + self.image.height <= self.stop or self.cruzo == 1 or (señalEnVerde == 1 and señalEnAmarillo == 0)) and (self.i == 0 or self.image.y + self.image.height < (autos[self.direccion][self.carril][self.i - 1].image.y - 15))):

                self.image.y += self.velocidad
    

        elif self.direccion == 'izquierda':


            if(self.cruzo == 0 and self.image.x + self.image.size[0] < paradas[self.direccion]):
                self.cruzo = 1
            if((self.image.x >= self.stop or self.cruzo == 1 or (señalEnVerde == 2 and señalEnAmarillo == 0)) and 
               (self.i == 0 or self.image.x + self.image.size[0] > (autos[self.direccion][self.carril][self.i - 1 ].image.x + autos[self.direccion][self.carril][self.i - 1].image.width + 15))):
                self.image.x -= self.velocidad

        
        elif self.direccion == 'arriba':
            if(self.cruzo == 0 and self.image.y + self.image.size[0] < paradas[self.direccion]):
                self.cruzo = 1
            if((self.image.y >= self.stop or self.cruzo == 1 or (señalEnVerde == 3 and señalEnAmarillo == 0)) and 
               (self.i == 0 or self.image.y + self.image.size[0] > (autos[self.direccion][self.carril][self.i - 1 ].image.y + autos[self.direccion][self.carril][self.i - 1].image.width + 15))):
                self.image.y -= self.velocidad


def inicializacionSemaforos():

    #crear semaforos
    S1 = Semaforos(verde[0],amarillo, rojo)
    señales.append(S1)
    S2 = Semaforos(verde[1], amarillo,S1.verde + S1.amarillo + S1.rojo)
    señales.append(S2)
    S3 = Semaforos(verde[2], amarillo, rojo)
    señales.append(S3)
    S4 = Semaforos(verde[3], amarillo, rojo)
    señales.append(S4)
    cicloSemaforos()


def cicloSemaforos():
    global señalEnVerde, señalEnAmarillo, proximaVerde

    while(señales[señalEnVerde].verde > 0 ):
        temporizador()
        time.sleep(1)
    señalEnAmarillo = 1

    for i in range(0, 3):
        for vehicle in autos[numeroDireccion[señalEnVerde]][i]:
              vehicle.stop = paradas[numeroDireccion[señalEnVerde]]
              
    while(señales[señalEnVerde].amarillo > 0):
        temporizador()
        time.sleep(1)
    señalEnAmarillo = 0

    #estas lineas resetean los tiempos de los semaforos actuales
    señales[señalEnVerde].verde = verde[señalEnVerde]
    señales[señalEnVerde].amarillo = amarillo
    señales[señalEnVerde].rojo = rojo

    proximoSemaforo()

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




def crearAutos():

    while True:
        carril = random.randint(1, 2)
        temp = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if temp < dist[0]:
            direction_number = 0
        elif temp < dist[1]:
            direction_number = 1
        elif temp < dist[2]:
            direction_number = 2
        elif (temp < dist[3]):
            direction_number = 3
        Auto(carril, numeroDireccion[direction_number])
        carrilLleno[direction_number] += 1

        time.sleep(1)



def proximoSemaforo():
    global proximaVerde, señalEnVerde, señalEnAmarillo

    maximo = max(carrilLleno, key=carrilLleno.get)
    
    fila.append(maximo)
    if maximo == 0:
        carrilLleno[0] = 0
    elif maximo == 1:
        carrilLleno[1] = 0
    elif maximo == 2:
        carrilLleno[2] = 0
    elif maximo == 3:
        carrilLleno[3] = 0
    proximaVerde = fila[0]
    
    señalEnVerde = proximaVerde #cambia de semaforo actual 

    fila.pop(0)
    señales[proximaVerde].rojo = señales[señalEnVerde].amarillo + señales[señalEnVerde].verde 

    


class inicio:
    
    thread_inicio = threading.Thread(name="Inicio", target= inicializacionSemaforos, args=())
    thread_inicio.daemon = True
    thread_inicio.start()

    
    # Configuración de la pantalla
    WIDTH, HEIGHT = 1400, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Tráfico")



    thread_autos = threading.Thread(name = "Creacion de autos", target=crearAutos, args=())
    thread_autos.daemon = True
    thread_autos.start()

    false = True
    AMARILLO = (240,255,0)
    ROJO = (255,0,0)
    VERDE = (0, 255, 0)

    background = BLANCO

    while false:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                false = False
                sys.exit()
                pygame.quit()

        screen.fill(background) #mostrara en la ventana el fondo blanco


        #este ciclo for mostrara los semaforos en las coordenadas declaradas
        for i in range(0, numeroSemaforos):
            if i == señalEnVerde:
                if señalEnAmarillo == 1:
                    SemaforoAmarillo = pygame.draw.circle(screen, color=AMARILLO, width= 10, center= semaforoCoordenadas[i], radius= 5)
                else:
                    SemaforoVerde = pygame.draw.circle(screen, color=VERDE,  center= semaforoCoordenadas[i], radius= 5)
            else:               
                SemaforoRojo = pygame.draw.circle(screen, color=ROJO, width= 10, center= semaforoCoordenadas[i], radius= 5)


        #mostrar los autos
        for AUTO in simulacion:
            pygame.draw.rect(screen, AZUL, AUTO.image)
            AUTO.mover()
        
        pygame.display.update()

inicio()