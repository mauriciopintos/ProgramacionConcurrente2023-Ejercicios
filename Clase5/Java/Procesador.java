public class Procesador extends Thread{
    
    public void run() {
        while(true){
            Recurso.permiso.lock();
            try {
                this.procesarDato();
            } finally {
                Recurso.permiso.unlock();
            }
        }
    }

    private void procesarDato() {
        if (!Recurso.leido){
            System.out.println("El hilo "+Thread.currentThread().getName()+" procesó el dato: "+Integer.toString(Recurso.dato));
            Recurso.leido = true;
            try {
                Thread.sleep(Recurso.alAzar.nextInt(5000)+1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}