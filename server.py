import socket
import threading

class SimpleServer:
    def __init__(self, host, port, max_connections):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)
        print(f"Server started on {self.host}:{self.port}, waiting for connections...")

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Error sending message to client: {e}")
                    self.clients.remove(client)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                print(f"Received message: {message.decode('utf-8')}")
                if message.decode('utf-8') == "exit":
                    break
                if message.decode('utf-8') == "kill":
                    self.broadcast("Server is shutting down", client_socket)
                    self.server_socket.close()
                    break
                self.broadcast(message, client_socket)
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()
        self.clients.remove(client_socket)
        print("Client disconnected")

    def run(self):
        while True:
            if len(self.clients) == self.max_connections:
                print("Maximum number of connections reached")
                break
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            

# Exemple d'utilisation
if __name__ == "__main__":
    server = SimpleServer('localhost', 12345, 5)
    server.run()