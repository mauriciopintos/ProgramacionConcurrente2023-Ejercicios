#Importa módulos para Interfaz Gráfica de usuario (tkinter)
import multiprocessing
import tkinter as tk
from tkinter import ttk
import time

#Crea la ventana principal
main_window = tk.Tk()
main_window.title("Ejemplo")
main_window.configure(width=350, height=200)

#Función que crea y posiciona el botón "Salir"
def opcionFinalizar(window):
    # boton = ttk.Button(main_window, text="Salir", command=main_window.destroy)
    boton = ttk.Button(window, text="Salir", command=window.destroy)
    boton.place(x=170, y=170)
    

#Función que crea una etiqueta (label) de texto en la posición (x,y) de la pantalla.
def createLabel(a,b):
    label = ttk.Label(text="")
    label.place(x=a,y=b)
    return label

#Función que crea una etiqueta (llamando a createLabel()) y luego anima texto dentro de la misma.
# def crearAnimacion(a, b, char, cola):
def crearAnimacion(a, b, char):
    mylabel = createLabel(a,b)
    texto="Etiqueta " + char
    retardo: float=0.25
    for i in range(0,35):
        time.sleep(retardo)
        texto += char
        mylabel.config(text = texto)
        main_window.update_idletasks()
        main_window.update()
    opcionFinalizar(mylabel)
    # cola.put(None) # Indica que el proceso ha terminado

# Ejecuta tres animaciones en procesos separados
# processes = []
# colas = []
# for char, pos_y in [('X', 10), ('Y', 30), ('Z', 50)]:
#     cola = Queue()
#     proc = Process(target=crearAnimacion, args=(10, pos_y, char, cola))
#     proc.start()
#     processes.append(proc)
#     colas.append(cola)
if __name__ == '__main__':
    # cola_1 = multiprocessing.Queue()
    # cola_2 = multiprocessing.Queue()
    # cola_3 = multiprocessing.Queue()

    # proceso_1 = multiprocessing.Process(target=crearAnimacion, args=(10, 10, 'X', cola_1))
    # proceso_2 = multiprocessing.Process(target=crearAnimacion, args=(10, 30, 'Y', cola_2))
    # proceso_3 = multiprocessing.Process(target=crearAnimacion, args=(10, 50, 'Z', cola_3))

    proceso_1 = multiprocessing.Process(target=crearAnimacion, args=(10, 10, 'X'))
    proceso_2 = multiprocessing.Process(target=crearAnimacion, args=(10, 30, 'Y'))
    proceso_3 = multiprocessing.Process(target=crearAnimacion, args=(10, 50, 'Z'))

    proceso_1.start()
    proceso_2.start()
    proceso_3.start()

# colas.append(cola_1)
# colas.append(cola_2)
# colas.append(cola_3)

# Espera a que todos los procesos terminen
# for cola in colas:
#     cola.get()



#Coloca la opcion "Salir"
    # opcionFinalizar(proceso_1)
    proceso_1.join()
    proceso_2.join()
    proceso_3.join()
    
#Bucle principal de la ventana
# main_window.mainloop()