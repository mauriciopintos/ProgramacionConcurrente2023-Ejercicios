# Importacion de modulos requeridos para el codigo concurrente
import logging
import random
import threading
import time

# Configuracion de formato de salida de los eventos del modulo logging 
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Definicion de las variables que se utilizaran en las clases Generador y Procesador
dato = None
lock = threading.Lock()
leido = True

# Definicion de clase Generador
class Generador(threading.Thread):
    def __init__(self):
        super().__init__()
    
    #Definicion del metodo run de Generador
    def run(self):
        while True:
            with lock:
                global leido
                if leido:
                    global dato
                    dato = random.randint(0,100)
                    logging.info(f"El {threading.current_thread().name} generó el dato: "+str(dato))
                    leido = False


# Definicion de clase Procesador
class Procesador(threading.Thread):
    def __init__(self):
        super().__init__()

    #Definicion del metodo run de Procesador
    def run(self):
        while True:
            with lock:
                global leido
                if not leido:
                    global dato
                    logging.info(f"El {threading.current_thread().name} procesó el dato: "+str(dato))
                    leido = True
            time.sleep(random.randint(1,5))

# Definicion de la funcion generarProcesadores()
def generarProcesadores(cantidad):
    for i in range(cantidad):
        # Instanciacion de un objeto de la clase Procesador
        procesador = Procesador()
        procesador.start()

# Instanciacion de un objeto de la clase Generador
gen1 = Generador()


# Definicion de la funcion main() que corre el codigo
def main():
    gen1.start()
    generarProcesadores(2)

# Llamada a la funcion main()
main()