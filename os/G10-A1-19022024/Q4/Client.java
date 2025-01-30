package Q4;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class Client
{
    private static final String SERVER_ADDRESS = "localhost";
    private static final int PORT = 12345;

    private static String response;
    private static String message;
    
    public static void main(String[] args)
    {
        

        try (var client_socket = new Socket(SERVER_ADDRESS, PORT);
             var in = new BufferedReader(new InputStreamReader(client_socket.getInputStream()));
             var out = new PrintWriter(client_socket.getOutputStream(), true);
             var scan = new Scanner(System.in))
        {

            f("Connection established...");

            // Create a loop to allow the user to send multiple messages
            while(true)
            {
                // Ask the user to enter a message
                f("\nEnter a message to send to the server: ");
                message = scan.nextLine();

                // Send the message to the server
                out.println(message);

                // Receive and print the response from the server
                response = in.readLine();
                f("\nResponse from server: " + response);

                // Check if the user wants to exit
                f("\n--'EXIT' TO QUIT / ANY KEY TO CONTINUE--");
                message = scan.nextLine();

                if(message.equalsIgnoreCase("exit"))
                {
                    break;
                }
            }

            // Close the streams and socket
            in.close();
            out.close();
            client_socket.close();

        }
        catch (IOException e)
        {
            // Print error message if an exception occurs
            System.err.println(e.getMessage());
        }
    }

    // Helper method to print messages
    public static void f(String s)
    {
        System.out.println(s);
    }
}