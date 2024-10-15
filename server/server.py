"""
Server module

This module contains the server class that will be used to handle the
communication between the clients and the server.

Classes:
    Server: This class will be used to handle the communication between the
    clients and the server.
    
"""

from __future__ import annotations

# Standard library imports
import threading
import socket as socket_

# Local imports
from database import Database, Cosmetic, Weapon


class Server:
    """
    Server class

    This class will be used to handle the communication between the clients and
    the server.

    ## Attributes:
    - host:str - The host of the server.
    - port:int - The port of the server.
    - server_socket:socket - The socket of the server.
    - clients:list - The list of the clients connected to the server.
    - db:Database - The database of the server.

    ## Methods:
    - broadcast(self, message:str) -> None: This method will broadcast the
    message to all the clients.
    - send(self, client_socket:socket, message:str) -> None: This method will
    send the message to the client.
    - lobby(self, client_socket:socket) -> None: This method will handle the
    lobby of the client.
    - run(self) -> None: This method will run the server.
    """
    def __init__(self, host:str, port:int) -> None:
        """
        Constructor of the Server class.
        
        ## Parameters:
        - host:str - The host of the server.
        - port:int - The port of the server.
        """

        self.host = host
        self.port = port
        self.server_socket = socket_.socket(
            socket_.AF_INET, socket_.SOCK_STREAM
        )
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.clients =  list()
        self.db = Database('../data.db')

    def broadcast(self, message:str) -> None:
        """
        This method will broadcast the message to all the clients.
        
        ## Parameters:
        - message:str - The message to be broadcasted.
        
        ## Returns:
        - None
        """
        message = message.encode('utf-8')
        for client in self.clients:
            client.send(message)

    def send(self, client_socket:socket_.socket, message:str) -> None:
        """
        This method will send the message to the client.
        
        ## Parameters:
        - client_socket:socket - The socket of the client.
        - message:str - The message to be sent.
        
        ## Returns:
        - None
        """
        message = message.encode('utf-8')
        client_socket.send(message)

    def lobby(self, client_socket:socket_.socket) -> None:
        """
        This method will handle the lobby of the client.
        
        ## Parameters:
        - client_socket:socket - The socket of the client.
        
        ## Returns:
        - None
        """
        print(f'[DBG] from server.py.Server.lobby : Lobby started for client {client_socket}')

        user = -1 # -1 means the user is not logged in
        login_form = client_socket.recv(1024) # Message recieving from the client
        login_form = login_form.decode('utf-8') # Decoding the message
        login_form = login_form.strip().split() # Splitting the message
        # REGISTER NEW USER
        print(f'[DBG] from server.py.Server.lobby : {login_form=}')
        if login_form == ["quit"]:
            print(f'[DBG] from server.py.Server.lobby : Client {client_socket} disconnected')
            self.clients.remove(client_socket)
            client_socket.close()
            return
        if login_form[0] == 'REGISTER':
            username = login_form[1]
            email = login_form[2]
            password = login_form[3]
            print(f'[DBG] from server.py.Server.lobby : {email=}, {password=}')
            self.db.add_player(username, email, password)
            user = self.db.login(email, password)
            if user == -1:
                self.send(client_socket, 'REGISTER ERROR')
            else:
                self.send(client_socket, 'REGISTER OK')
            print(f'[DBG] from server.py.Server.lobby : {user=}')
        else:
            # error handling
            if not login_form:
                return
            if len(login_form) != 2:
                self.send(client_socket, 'LOGIN ERROR')
                return
        
            # Getting the email and password from the message, and trying to login
            email = login_form[0]
            password = login_form[1]
            print(f'[DBG] from server.py.Server.lobby : {email=}, {password=}')
            user = self.db.login(email, password)
            if user == -1:
                self.send(client_socket, 'LOGIN ERROR')
            else:
                self.send(client_socket, 'LOGIN OK')
            print(f'[DBG] from server.py.Server.login : {user=}')

            # Loop for the client if the authentication is not successful at first
            while user == -1:
                print(f'[DBG] from server.py.Server.lobby : starting login loop for client {client_socket}')
                login_form = client_socket.recv(1024)
                login_form = login_form.decode('utf-8')
                login_form = login_form.strip().split()

                # error handling
                if not login_form:
                    return
                if len(login_form) != 2:
                    self.send(client_socket, 'LOGIN ERROR')
                    return

                email = login_form[0]
                password = login_form[1]
                print(f'[DBG] from server.py.Server.lobby : {email=}, {password=}')
                user = self.db.login(email, password)
                if user == -1:
                    self.send(client_socket, 'LOGIN ERROR')
                else:
                    self.send(client_socket, 'LOGIN OK')
                print(f'[DBG] from server.py.Server.login : {user=}')
        
        # Loop for the client if the user is logged in
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
                    print(f'[DBG] from server.py.Server.lobby : Client {client_socket} disconnected')
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                case _:
                    pass

    def run(self) -> None:
        """
        This method will run the server.

        ## Parameters:
        - None

        ## Returns:
        - None
        """
        print(f'[DBG] from server.py.Server.run : Server started at {self.host}:{self.port}')
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"[DBG] from server.py.Server.run : Connection from {addr} has been established!")
            print(f"[DBG] from server.py.Server.run : {self.clients=}")
            threading.Thread(target=self.lobby, args=(client_socket,)).start()


server = Server('localhost', 5555)
server.run()
