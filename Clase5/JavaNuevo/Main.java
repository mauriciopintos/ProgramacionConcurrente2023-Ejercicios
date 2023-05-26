import java.util.logging.Handler;
import java.util.logging.*;

public class Main {
    public static void generarProcesadores(int cantidad) {
        for (int i = 0; i < cantidad; i++) {
            Procesador procesador = new Procesador();
            procesador.start();
        }
    }

    public static void main(String[] args) {
        Handler consoleHandler = new ConsoleHandler();
        consoleHandler.setFormatter(new SimpleFormatter() {
            private static final String format = "%1$tH:%1$tM:%1$tS.%1$tL [%2$s] - %3$s %n";

            @Override
            public synchronized String format(LogRecord lr) {
                return String.format(format, lr.getMillis(), lr.getThreadID(), lr.getMessage());
            }
        });

        Logger.getLogger("").addHandler(consoleHandler);

        Generador gen1 = new Generador();
        gen1.start();
        generarProcesadores(2);
    }
}