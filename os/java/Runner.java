package _me.java;

public class Runner implements Runnable 
{
    // The run method is required to implement the Runnable interface
    public void run() 
    {
        // This loop runs for 5 iterations
        for(int i = 0; i < 5; i++) 
        {
            // Print a message indicating that the child thread is running along with the value of i
            System.out.println("Child thread is running: " + i);
            try 
            {
                // Pause the execution of the thread for 1000 milliseconds (1 second)
                Thread.sleep(1000);
            } 
            catch (InterruptedException e) 
            {
                // If an InterruptedException is thrown, print the exception
                System.err.println(e);
            }
        }
    }

    // The entry point of the program
    public static void main(String[] args) 
    {
        // Create an instance of the Runner class
        var threader = new Runner();

        // Create a new Thread object, passing the Runner instance as a Runnable target
        var t = new Thread(threader);
        
        // Start the newly created thread
        t.start();
    }
}
