public class Generador extends Thread{

    public void run() {
        while(true){
            Recurso.permiso.lock();
            try {
                this.generarDato();
             } finally {
                Recurso.permiso.unlock();
             }
        }
    }

    private void generarDato() {
        if (Recurso.leido){
            Recurso.dato = Recurso.alAzar.nextInt(101);
            System.out.println("El hilo "+Thread.currentThread().getName()+" generó el dato: "+Integer.toString(Recurso.dato));
            Recurso.leido = false;
        }
    }
}