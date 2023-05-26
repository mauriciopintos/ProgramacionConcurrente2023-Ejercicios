import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

class Procesador extends Thread {
    private static Integer dato;
    private static boolean leido = true;
    private static final Object lock = new Object();
    private static final Logger logger = Logger.getLogger(Procesador.class.getName());

    public void run() {
        while (true) {
            synchronized (lock) {
                if (!leido) {
                    logger.log(Level.INFO, "Se procesó el dato = {0}", dato);
                    leido = true;
                }
            }
            try {
                Thread.sleep(new Random().nextInt(5) + 1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}