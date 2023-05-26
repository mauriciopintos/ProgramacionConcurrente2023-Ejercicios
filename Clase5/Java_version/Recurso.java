import java.util.Random;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Recurso {

    static int dato;
    static Lock permiso = new ReentrantLock();
    static boolean leido = true;
    static Random alAzar = new Random();
    
}