## Echo Client-Server Application

This project consists of two Java classes, `Client` and `Server`, which together create a simple echo client-server application. The `Client` class allows users to send messages to the `Server`, which then echoes those messages back to the client.

### Client Class

The `Client` class establishes a connection to the server and sends user input to the server for echoing. It continuously prompts the user for input and displays the echoed response from the server.

#### Features:
- Connects to a server running on `localhost` at port `12345`.
- Uses `Scanner` to read user input.
- Sends user input to the server and receives the echoed response.

### Server Class

The `Server` class listens for incoming client connections and echoes back any messages it receives from clients. 

#### Features:
- Listens for client connections on port `12345`.
- Accepts incoming client connections and creates a new thread to handle each client.
- Uses `InputStream` and `OutputStream` to read from and write to clients.

### How to Run
1. Compile both classes: `javac Client.java` and `javac Server.java`.
2. Start the server: `java Server`.
3. Start the client: `java Client`.
4. Enter messages in the client console to send them to the server.
5. The server will echo the messages back to the client.

### Notes
- To exit the client, type `EXIT` when prompted for a message.
- To stop the server, press `Ctrl + C` in the terminal running the server.

This simple echo client-server application demonstrates basic socket programming in Java for communication between a client and a server.
