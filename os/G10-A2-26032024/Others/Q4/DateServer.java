import java.net.*;
import java.io.*;

public class DateServer 
{
    public static void main(String[] args) 
    {
        try 
        {
            ServerSocket socket = new ServerSocket(6013);

            while (true) 
            {
                // Accept client connection
                var client = socket.accept();
                
                // Create a new thread to handle the client request
                var threader = new Runner(client);

                var t = new Thread(threader);
                t.start();
            }
        } 
        catch (IOException ioe) 
        {
            System.err.println(ioe);
        }
    }
}

class Runner implements Runnable 
{
    private Socket clientSocket;

    public Runner(Socket clientSocket) 
    {
        this.clientSocket = clientSocket;
    }

    @Override
    public void run() 
    {
        try 
        {
            PrintWriter p_out = new PrintWriter(clientSocket.getOutputStream(), true);

            // Write the Date to the socket
            p_out.println(new java.util.Date().toString());

            // Close the socket
            clientSocket.close();
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
}
