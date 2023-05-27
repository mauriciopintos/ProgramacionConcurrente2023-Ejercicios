# Implemente un programa que tenga dos hilos A y B, los dos con acceso a una variable X (global)
# inicializa la variable en un valor entero aleatorio (entre 1 y 100). 
# El hilo A decrementa X en 1 hasta llegar a 0 intercalando un retardo aleatorio entre 0 y 1 segundo
# entre cada decremento de X. 
# El hilo B hará iteraciones cada un tiempo aleatorio entre 1 y 4 segundos, imprimiendo el valor de
# X en cada iteración hasta que X sea 0. 
# Tanto A como B deberán imprimir mensajes al arrancar y al terminar, identificando al hilo. El hilo
# A deberá también indicar el valor inicial de X en el mensaje de arranque o final. 
# Pregunta: Hay condiciones de carrera? Como las evitaría?
# -----------------------------------------------------------------------------------------------
import logging
import threading
import time
import random

x = random.randint(1,100)
# lock = threading.Lock

# Configuracion de formato de salida de los eventos del modulo logging 
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def decrementa_A():
    global x
    logging.info(f"Inicia Hilo_A -> con valor de X: {x}")
    while x != 0:
        retardo = random.randint(0,1)
        x-=1
        time.sleep(retardo)
    logging.info(f"FINALIZA Hilo_A -> con valor de X: {x}")
        

def imprime_B():
    global x
    logging.info(f"Inicia Hilo_B")
    while x != 0:
        retardo = random.randint(1,4)
        logging.info(f"Hilo B -> Valor de X: {x}")
        time.sleep(retardo)
    logging.info(f"FINALIZA Hilo_B")

# Crear y ejecutar los hilos
if __name__ == '__main__':
    hilo_A = threading.Thread(target=decrementa_A)
    hilo_B = threading.Thread(target=imprime_B)

    hilo_A.start()
    hilo_B.start()

    hilo_A.join()
    hilo_B.join()