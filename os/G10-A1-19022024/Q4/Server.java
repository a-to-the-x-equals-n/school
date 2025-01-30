package Q4;

import java.io.IOException;
import java.net.ServerSocket;

public class Server
{
    private static final int PORT = 12345;
    private static int bytesRead;
    private static byte[] buffer;
    private static String s_buffer;

    public static void main(String[] args)
    {
        try (var server_socket = new ServerSocket(PORT))
        {
            // Server is listening
            f("\nServer is running...");

            try (var client_socket = server_socket.accept();
                    var in = client_socket.getInputStream();
                    var out = client_socket.getOutputStream())
            {
                // Connection established
                f("Client connected...");
    
                buffer = new byte[1024];
    
                // Read from input stream and write to output stream
                while ((bytesRead = in.read(buffer)) != -1) 
                {
                    // Format and print to server terminal
                    s_buffer = new String(buffer);
                    f("\nMessage from client: " + s_buffer);

                    // Echo client message
                    out.write(buffer, 0, bytesRead);
                    out.flush();
                }
    
                // Client disconnected
                System.out.println("Client disconnected.");
    
                // Close streams and sockets
                in.close();
                out.close();
                client_socket.close();
                server_socket.close();
            }
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