'''
TP2 - Monty Game Experiment
Universidad Torcuato Di Tella - MiM + Analytics
Joaquin Gonzalez - joagonzalez@gmail.com
Fecha: 19/02/2021
Referencia: https://www.analyticsvidhya.com/blog/2020/08/probability-conditional-probability-monty-hall-problem/
'''

import numpy as np
import matplotlib.pyplot as plt

class Monty:

    REPETICIONES = 1000000
    PUERTAS = 3
    INTERACTIVO = False
    conteosimelaquedo=0 # contemos cuántas veces gano si me quedo con la puerta que elegí al principio
    conteosinomelaquedo=0 # contemos cuántas veces gano si cambio la puerta que elegí al principio


    def __init__(self):
        self.descripcion()

        if self.INTERACTIVO:
            self.menu()


    def descripcion(self):
        print(f'Repeticiones: {self.REPETICIONES}')
        print(f'Puertas: {self.PUERTAS}')
        print(f'Interactivo: {self.INTERACTIVO}')


    def menu(self):
        
        try:
            self.PUERTAS = int(input(f'Ingrese el numero de puertas del problema (default: {self.PUERTAS}): '))
            self.REPETICIONES = int(input(f'Ingrese el numero se repeticiones del experimento (default: {self.REPETICIONES}): '))
        except Exception as e:
            print('Alguno de los valores ingresados es incorrecto, por favor vuelva a intentarlo...')
            self.menu()

    def run(self):
        
        if self.INTERACTIVO:
            elegimos = int(input('Ingrese una puerta donde cree que esta el auto: ')) #puerta que elegimos. Se puede cambiar.
        else:
            elegimos = 1
        
        for i in range(self.REPETICIONES + 1):           
            puertas = list(range(1, self.PUERTAS + 1)) # puertas que hay en el problema [1, 2 y 3]
            auto = np.random.randint(self.PUERTAS) + 1 # puerta que contiene al auto; se elige aleatoriamente.

            if elegimos == auto: # si la que elegimos es la del auto:
                puertas.remove(auto) # Si la que elegimos tiene el auto, entonces la puerta que deja Monty tiene que tener una cabra
                monty = np.random.choice(puertas) #Monty elije DEJAR una entre las N-1 que quedaron
            else: #sino:
                monty = auto # Si la que elegimos no tiene el auto y Monty remueve las otras, entonces elije la que tiene el auto

            
            # Ahora, momento de elegir. O me quedo con la que tenía, o elijo la otra. Veamos qué pasaría en ambos casos:
            # si me quedo con la original:
            melaquedo = elegimos #la que elegimos al principio.

            # si cambio la que elegí al principio:
            puertas = [elegimos, monty] # lista que tiene la que elegimos y vamos a decidir cambiar y la que DEJO Monty
            puertas.remove(elegimos) # saco la que elegimos (porque la cambiamos)
            nomelaquedo = puertas[0] # me quedo con alguna de las N-2 que sobra.

            # Si gano quedándomela, se suma 1 a ese conteo, y 0 al otro; si gano cambiándola, se suma 1 al otro conteo, y 0 a este.
            self.conteosimelaquedo += auto==melaquedo
            self.conteosinomelaquedo += auto==nomelaquedo


    def analyze(self):
        #Calculo las probabilidades finales:
        probaGanarConservandola=100*self.conteosimelaquedo/float(self.REPETICIONES)
        probaGanarCambiandola=100*self.conteosinomelaquedo/float(self.REPETICIONES)

        print('Proba de Ganar Conservando la Puerta: '+str(probaGanarConservandola)+'%')
        print('Proba de Ganar Cambiando la Puerta: '+str(probaGanarCambiandola)+'%')


if __name__ == '__main__':
    for i in [3, 5, 10]:
        monty = Monty()
        monty.PUERTAS = i
        monty.run()
        monty.analyze()
