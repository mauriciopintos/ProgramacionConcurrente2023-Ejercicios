# Implemente un programa que ejecute 10 hilos que impriman un mensaje identificando al hilo,
# luego esperen un tiempo aleatorio entre 1 y 5 segundos y luego impriman un mensaje indicando
# que terminaron (identificando al hilo)
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

    logging.info(f"{msj} inicia...")
    time.sleep(retardo)
    logging.info(f"{msj} TERMINA!")    

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
        