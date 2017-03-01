# -*- coding: cp1252 -*-
#Hoja de Trabajo 5
#Daniel Rodriguez 15796
#Alejandro Vasquez  
import simpy
import random
import math

def proceso(env, nombre, CPU, memoriaRAM, inputOutput, memoria, instrucciones):
    global tiempoDelProceso
    global tiempoInicio
    global tiempoTotal
    
    #Crea un nuevo proceso
    creacion = env.now #Presenta el momeno en el cual se crea un nuevo proceso
    print('%s este se creo a las %s unidades de tiempo' % (nombre, creacion))
    with memoriaRAM.get(memoria) as req:
        yield req
        ready=env.now
        print('%s cambio a estado ready en %s' % (nombre,ready))
        
        while(instrucciones>0):
            with CPU.request() as req1:
                yield req1
                procesando=env.now
                print ('Comenzo a procesar %s en %s' % (nombre, procesando))
                yield env.timeout(tiempoDelProceso)
                procesando=env.now
                print ('Finalizo de procesar %s en %s' % (nombre, procesando))

                if (instrucciones-3)<0:
                    terminated = env.now
                    tiempoProceso = terminated - creacion
                    tiempoTotal = tiempoTotal + tiempoProceso
                    print('%s finalizo en %s' % (nombre, terminated))
                    memoriaRAM.put(memoria)
                    instrucciones = 0
                else:
                    instrucciones = instrucciones - 3
                    if random.randint(0,1) == 0:
                        with inputOutput.request() as req2:
                            yield req2
                            print(' %s comenzo el proceso Input/Output en %s' % (nombre, env.now))
                            tib = random.randint(1, tiempoInicio)
                            yield env.timeout(tib)
                            print(' %s finalizo el proceso Input/Output en %s' % (nombre, env.now))
                    
def source(env, numero, intervalo, CPU, inputOutput, memoriaRAM):
    global InstruccionesMax
    global MemoriaMax
    for i in range(numero):
        p= proceso(env, 'proceso %s' % i, CPU, memoriaRAM, inputOutput, random.randint(1,MemoriaMax), random.randint(1,InstruccionesMax)) 
        env.process(p)
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)

semilla = 42
procesos = 25
intervalo = 5.0
global tiempoDelProceso #Tiempo utilizado en el CPU para cada proceso
tiempoDelProceso = 2

global tiempoInicio 
tiempoInicio = 3

global InstruccionesMax 
InstruccionesMax = 10

global MemoriaMax
MemoriaMax = 10

global tiempoTotal
tiempoTotal = 0

random.seed(semilla)
env = simpy.Environment()

# Incia los procesos y corre el programa
CPU = simpy.Resource(env, capacity=1)
inputOutput = simpy.Resource(env, capacity=1)
memoriaRAM =simpy.Container(env, 10000, init=10000)
env.process(source(env, procesos, intervalo, CPU, inputOutput, memoriaRAM))
env.run()

promedio = tiempoTotal/procesos


print('\n\n')
print('El CPU se tardó %s en unidades de tiempo en realizar la cola de todos los procesos' % (tiempoTotal))
print ('El promedio de tiempo tomado operacion fue de: %s en unidades de tiempo' % (promedio))
print('\n\n')
