import socket
import threading

class SimpleClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if not message:
                    break
                print(f"Received: {message.decode('utf-8')}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        self.client_socket.close()

    def send_messages(self):
        while True:
            try:
                message = input("Enter message: ")
                self.client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                break
        self.client_socket.close()

    def run(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

# Exemple d'utilisation
if __name__ == "__main__":
    client = SimpleClient('localhost', 12345)
    client.run()