import threading
import socket as socket_
from database import Database, Cosmetic, Weapon


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket_.socket(
            socket_.AF_INET, socket_.SOCK_STREAM
        )
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.clients = []
        self.db = Database('../data.db')

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def send(self, client_socket, message):
        message = message.encode('utf-8')
        client_socket.send(message)

    def lobby(self, client_socket):
        print('Lobby started')
        user = -1
        login_form = client_socket.recv(1024)
        login_form = login_form.decode('utf-8')
        login_form = login_form.strip().split()
        email = login_form[0]
        password = login_form[1]
        print(login_form)
        user = self.db.login(email, password)
        if user == -1:
            self.send(client_socket, 'LOGIN ERROR')
        else:
            self.send(client_socket, 'LOGIN OK')
        print(f'[DBG] from server.py.36 : {user=}')
        while user == -1:
            print(f'starting login loop for client {client_socket}')
            login_form = client_socket.recv(1024)
            login_form = login_form.decode('utf-8')
            login_form = login_form.strip().split()
            email = login_form[0]
            password = login_form[1]
            print(login_form)
            user = self.db.login(email, password)
            if user == -1:
                self.send(client_socket, 'LOGIN ERROR')
            else:
                self.send(client_socket, 'LOGIN OK')

        while True:
            message = client_socket.recv(1024)
            message = message.decode('utf-8')
            message = message.strip().split()
            if not message:
                continue
            head = message[0]
            body = message[1:]
            match head:
                case 'HOTBAR':
                    option = body.pop(0)
                    match option:
                        case 'OPEN':
                            self.send(client_socket, 'HOTBAR OPEN')
                        case 'SET':
                            slot = body.pop(0)
                            item = body.pop(0)
                            try:
                                user.inventory[slot] = Weapon(item)
                            except ValueError as e:
                                self.send(
                                    client_socket, f'ERROR ({repr(e)}) HOTBAR '
                                )
                            except TypeError as e:
                                self.send(
                                    client_socket, f'ERROR ({repr(e)}) HOTBAR '
                                )
                            self.send(client_socket, 'OK HOTBAR SET')
                        case 'CLOSE':
                            self.send(client_socket, 'HOTBAR CLOSE')
                case 'SHOP':
                    pass
                case 'FRIENDS':
                    pass
                case 'WEAPONS':
                    pass
                case 'COSMETICS':
                    pass
                case 'FIGHT':
                    pass
                case 'QUIT':
                    print(f'Client {client_socket} disconnected')
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                case _:
                    pass

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(self.clients)
            threading.Thread(target=self.lobby, args=(client_socket,)).start()


server = Server('localhost', 5555)
server.run()
