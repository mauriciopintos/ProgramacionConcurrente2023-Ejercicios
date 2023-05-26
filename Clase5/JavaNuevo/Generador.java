import java.util.Random;
import java.util.logging.*;

class Generador extends Thread {
    private static Integer dato;
    private static boolean leido = true;
    private static final Object lock = new Object();
    private static final Logger logger = Logger.getLogger(Generador.class.getName());

    public void run() {
        while (true) {
            synchronized (lock) {
                if (leido) {
                    dato = new Random().nextInt(101);
                    logger.log(Level.INFO, "Se generó un nuevo dato = {0}", dato);
                    leido = false;
                }
            }
        }
    }
}
