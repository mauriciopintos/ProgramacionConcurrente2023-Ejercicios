# Modificar el programa anterior para que se ejecuten 2 hilos A y un hilo B. Identificar (con
# comentarios) las zonas críticas y colocar los objetos necesarios para evitar condiciones de carrera.
# -----------------------------------------------------------------------------------------------

import logging
import threading
import time
import random

x = random.randint(1, 100)
lock = threading.Lock()

# Configuración de formato de salida de los eventos del módulo logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def decrementa_A():
    global x
    logging.info(f"Inicia Hilo_A [{threading.current_thread().name}] -> con valor de X: {x}")
    while x != 0:
        # Comienzo de zona critica del Hilo_A
        lock.acquire()  # Adquirir el lock antes de acceder a x
        x -= 1
        lock.release()  # Liberar el lock después de modificar x
        # Fin de zona critica del Hilo_A

        retardo = random.randint(0, 1)
        time.sleep(retardo)
    logging.info(f"FINALIZA Hilo_A [{threading.current_thread().name}] -> con valor de X: {x}")

def imprime_B():
    global x
    logging.info(f"Inicia Hilo_B [{threading.current_thread().name}]")
    while x != 0:
        # Comienzo de zona critica del Hilo_B
        lock.acquire()  # Adquirir el lock antes de acceder a x
        logging.info(f"Hilo B -> Valor de X: {x}")
        lock.release()  # Liberar el lock después de acceder a x
        # Fin de zona critica del Hilo_B
        
        retardo = random.randint(1, 4)
        time.sleep(retardo)
    logging.info(f"FINALIZA Hilo_B")

# Crear y ejecutar los hilos
if __name__ == '__main__':
    hilo_A_1 = threading.Thread(target=decrementa_A)
    hilo_A_2 = threading.Thread(target=decrementa_A)
    hilo_B = threading.Thread(target=imprime_B)

    hilo_A_1.start()
    hilo_A_2.start()
    hilo_B.start()

    hilo_A_1.join()
    hilo_A_2.join()
    hilo_B.join()
