public class Main {

    public static void main(String[] args) {
        
        Thread gen1 = new Generador();
        gen1.start();
        generarProcesadores(2);
    }

    private static void generarProcesadores(int cantidad){
        for(int i=0; i<cantidad ; i++){
            Thread procesador = new Procesador();
            procesador.start();
        }
    }
}