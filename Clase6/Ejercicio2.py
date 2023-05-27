# Modifique el programa anterior de modo que pueda medir e imprimir el tiempo total que tomo
# ejecutarse cada hilo (en milisengundos)
# -----------------------------------------------------------------------------------------------

# Importacion de modulos requeridos para el codigo concurrente
import logging
import random
import threading
import time

# Configuracion de formato de salida de los eventos del modulo logging 
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Definicion de la funcion de impresion de cada hilo
def imprimeHilo():
    nombreHilo = threading.current_thread().name
    hilosVivos = threading.active_count() 
    msj = f'El {nombreHilo} de {hilosVivos} threads:'
    retardo = random.randint(1,5)
    duracion = time.time()
    
    logging.info(f"{msj} inicia...")
    time.sleep(retardo)
    duracion = time.time() - duracion
    logging.info(f"{msj} TERMINA! - [Tiempo de vida del hilo: {int(duracion * 1000)} ms]")



# Crear y ejecutar los hilos
if __name__ == '__main__':
    # Instancion una lista para almacenar los hilos que se vayan ejecutando
    hilos = []
    
    # Insertacion de hilos en la lista de hilos
    for i in range(10):
        hilo = threading.Thread(target=imprimeHilo)
        hilos.append(hilo)
    
    # Iniciacion de hilos de la lista de hilos
    for i in range(10):
        hilos[i].start()

    # Finalizacion de hilos de la lista de hilos
    for i in range(10):
        hilos[i].join()

