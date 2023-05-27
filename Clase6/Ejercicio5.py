# Implemente un programa que pueda lanzar 10 hilos tipo A y 2 hilos tipo B,
# todos con acceso a una variable global X incializada en 0. 
# Los Hilos A incrementan el valor de X hasta 1000000. 
# Los Hilos B imprime el valor de X cada 2 segundos. 
# Colocar líenas de comentario en el código, identificando las zonas críticas y los objetos
# utilizados para evitar condiciones de carrera.
# -----------------------------------------------------------------------------------------------

import logging
import threading
import time
import random

x = 0
# Instanciacion de un objeto lock
lock = threading.Lock()

# Configuración de formato de salida de los eventos del módulo logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def incrementa_A():
    global x
    logging.info(f"Inicia Hilo_A [{threading.current_thread().name}] -> con valor de X: {x}")
    while x <= 1000000:
        # Comienzo de zona critica del Hilo_A
        lock.acquire()  # Adquirir el lock antes de acceder a x
        if x < 1000000:
            x += 1
        lock.release()  # Liberar el lock después de modificar x
        # Fin de zona critica del Hilo_A

    logging.info(f"FINALIZA Hilo_A [{threading.current_thread().name}] -> con valor de X: {x}")

def imprime_B():
    global x
    logging.info(f"Inicia Hilo_B [{threading.current_thread().name}]")
    while x <= 1000000:
        # Comienzo de zona critica del Hilo_B
        lock.acquire()  # Adquirir el lock antes de acceder a x
        logging.info(f"Hilo B -> Valor de X: {x}")
        lock.release()  # Liberar el lock después de acceder a x
        # Fin de zona critica del Hilo_B
        
        time.sleep(2)

    logging.info(f"FINALIZA Hilo_B")

# Crear y ejecutar los hilos
if __name__ == '__main__':
    # Instanciacion dos listas para almacenar los hilos que se vayan ejecutando
    hilos_A = []
    hilos_B = []
    
    # Insertacion de hilos A y B instanciados en las listas de hilos
    for i in range(10):
        hilo_A = threading.Thread(target=incrementa_A)
        hilos_A.append(hilo_A)

    for i in range(2):
        hilo_B = threading.Thread(target=imprime_B)
        hilos_B.append(hilo_B)

    # Iniciacion de hilos de las listas de hilos
    for hilo_A in hilos_A:
        hilo_A.start()

    for hilo_B in hilos_B:
        hilo_B.start()

    # Finalizacion de hilos de las listas de hilos
    for hilo_A in hilos_A:
        hilo_A.join()

    for hilo in hilos_B:
        hilo_B.join()
