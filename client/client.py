# Description: This file contains the client side of the game.
# It is responsible for handling the user interface and sending and receiving messages from the server.
# The client is implemented using the pygame library and uses a menu to handle the login and registration process.
# The client also displays the lobby and shop interfaces, and sends and receives messages from the server to update the game state.

from __future__ import annotations

import sys
import threading
import socket

import pygame_menu
import pygame
import pygame_menu.themes

from theme import login_theme
from pgui.widget import Button
# Check if pygame is already initialized
if not pygame.get_init():
    pygame.init()

# Set the host and port for the client
HOST, PORT = 'localhost', 5555


class Client:
    """
    Client class to handle the client side of the game.
    
    Attributes:
    - host: str - The host of the server.
    - port: int - The port of the server.
    - client_socket: socket - The client socket to connect to the server.
    - state: str - The state of the client (login, lobby, shop).
    - pause: bool - The pause state of the client.
    - threads: list - The list of threads for the client.
    
    Methods:
    - send(message: str) - Send a message to the server.
    - receive() -> str - Receive a message from the server.
    - login_ui() - Display the login user interface.
    - register() - Register a new user.
    - login() - Login a user.
    - handle_inputs_from_server() - Handle inputs from the server.
    - lobby() - Display the lobby user interface.
    - run() - Run the client.
    """

    def __init__(self, host:str, port:int) -> None:
        """
        Initialize the client with the host and port of the server.
        
        Parameters:
        - host: str - The host of the server.
        - port: int - The port of the server.
        """

        self.host = host # The host of the server
        self.port = port # The port of the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The client socket to connect to the server
        self.client_socket.connect((self.host, self.port)) # Connect to the server

        self.state = 'login' # The state of the client (login, lobby, shop, etc.)
        self.pause = False # The pause state of the client
        self.threads:list[threading.Thread] = list() # The list of threads for the client

    def load_preferences(self) -> None:
        """
        Load the preferences of the client.
        
        [NIY]
        """
        raise NotImplementedError
        
    def send(self, message:str) -> None:
        """
        Send a message to the server.

        Parameters:
        - message: str - The message to send to the server.
        """
        message = message.encode('utf-8') # Encode the message to utf-8 
        self.client_socket.send(message) # Send the message to the server

    def receive(self) -> str:
        """
        Receive a message from the server.

        Returns:
        - str - The message received from the server.
        """
        response = self.client_socket.recv(1024) # Receive a message from the server
        response = response.decode('utf-8') # Decode the message from utf-8
        return response # Return the message

    def login_ui(self) -> None:
        """
        Display the login user interface.

        The login user interface allows the user to enter their email and password to login to the game.
        """
        self.state = 'login' # Set the state to login
        surface = pygame.display.set_mode((800,600)) # Set the display surface
        email = str() # The email of the user
        password = str() # The password of the user

        self.menu = pygame_menu.Menu('Microtrooopers - login',800, 600, theme=login_theme) # Create a menu for the login user interface
        self.menu.add.text_input('Email: ', default=email, maxchar=20, textinput_id='email') # Add a text input for the email
        self.menu.add.text_input('Password: ', default=password, maxchar=20, textinput_id='password', password=True) # Add a text input for the password
        self.menu.add.button('Login', self.login) # Add a button to login

        # TODO make the register button work
        self.menu.add.button('Register', self.register_ui) # * Add a button to register [NIY]

        while self.state == 'login': # While the state is login, display the login user interface
            events = pygame.event.get() # Get the events (exit manager)
            for event in events:
                if event.type == pygame.QUIT:
                    self.send('QUIT')
                    pygame.quit()
                    sys.exit()
            self.menu.update(events)
            self.menu.draw(surface)
            pygame.display.flip()

        print("[DBG] from client.py.Client.login : login_ui.done")

    def register_ui(self) -> None:
        """
        Register a new user.
        
        """
        self.state = 'register'
        surface = pygame.display.set_mode((800,600))
        username = str()
        email = str()
        password = str()
        self.menu = pygame_menu.Menu('Microtrooopers - register',800, 600, theme=login_theme)
        self.menu.add.text_input('Username: ', default=username, maxchar=20, textinput_id='username')
        self.menu.add.text_input('Email: ', default=email, maxchar=20, textinput_id='email')
        self.menu.add.text_input('Password: ', default=password, maxchar=20, textinput_id='password', password=True)
        self.menu.add.button('Register', self.register)
        self.menu.add.button('Back', self.login_ui)
        while self.state == 'register':
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.send('QUIT')
                    pygame.quit()
                    sys.exit()
            self.menu.update(events)
            self.menu.draw(surface)
            pygame.display.flip()
        self.state = 'lobby'
        
    def register(self) -> None:
        """
        Register a new user.

        The register method sends the username, email, and password to the server to register a new user.

        There is no need to have the username, email, and password as arguments because the data is already stored in the menu object.
        """
        data:dict = self.menu.get_input_data()

        if not data['username'] or not data['email'] or not data['password']:
            return
        print("[DBG] from client.py.Client.register : Registering user")
        print(f"[DBG] from client.py.Client.register : {data=}")
        self.send(f"REGISTER {data['username']} {data['email']} {data['password']}")
        response = self.receive()
        if response == 'REGISTER ERROR':
            print('[DBG] from client.py.Client.register : Register failed')
        else:   
            print('[DBG] from client.py.Client.register : Register success')
            self.menu.close()
            self.state = 'lobby'
            

    def login(self) -> None:
        """
        Login a user.

        The login method sends the email and password to the server to login the user.

        There is no need to have the email and password as arguments because the data is already stored in the menu object.
        """

        data:dict = self.menu.get_input_data() # Get the input data from the menu
        if not data['email'] or not data['password']: # case where the email or password is empty
            return
        
        self.send(f"{data['email']} {data['password']}")  # Send the email and password to the server
        response = self.receive() # Receive a response from the server, either 'LOGIN OK' or 'LOGIN ERROR'

        if response == 'LOGIN ERROR': # case where the login failed
            print('[DBG] from client.py.Client.login : Login failed')
        else: # case where the login succeeded
            print('[DBG] from client.py.Client.login : Login success')
            self.menu.close() # Close the menu
            self.state = 'lobby' # Change the state to lobby

    def handle_inputs_from_server(self) -> None:
        """
        Handle inputs from the server.
        
        The handle_inputs_from_server method listens for messages from the server and updates the game state accordingly.
        
        WARNING: This method is blocking and should be run in a separate thread.
        DO NEVER USE THIS METHOD ALONE, AS <ctrl+c> IS NOT CERTAIN TO STOP THE PROGRAM.
        """
        while self.client_socket: # While the client socket is open
            if self.done: # If the client is done
                break # Break the loop
            message = self.receive() # Receive a message from the server
            if ' '  in message: # If the message contains a space
                if len(message.split(' ')) >= 2: # If the message contains at least 2 elements
                    command, data = message.split(' ') # Split the message into command and data
                    if command == 'SHOP': # Command logic for the shop
                        if data == 'OPEN':
                            self.state = 'shop'
                        elif data == 'CLOSE':
                            self.state = 'lobby'

    def lobby(self) -> None:
        """
        Display the lobby user interface.
        
        The lobby user interface displays the lobby background and buttons for the shop and hotbar.
        """

        surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Set the display surface to fullscreen

        background = pygame.image.load('../assets/lobby.png') # Load the lobby background
        background = pygame.transform.scale(background, (1920, 1080)) # Scale the background to the display size

        # * This part will change when the shop and hotbar will be implemented
        shop_button_image = pygame.image.load('../assets/shop_button.png') # Load the shop button image
        shop_button_image = shop_button_image.convert_alpha() # Convert the shop button image to alpha
        shop_button_area = pygame.Rect(0, 0, *shop_button_image.get_size()) # Create a rectangle for the shop button area


        hotbar_button_image = pygame.image.load('../assets/hotbar.png') # Load the hotbar button image
        hotbar_button_image = hotbar_button_image.convert_alpha() # Convert the hotbar button image to alpha

        custom_cursor_map = (
            '................',
            '.XXXXXXXXXXXXXX.',
            '.XXXXXXXXXXXXXX.',
            '.XXXXXXXXXXXXXX.',
            '.XXXXXXXXXXXXXX.',
            '.XXXX...........',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '.XXXX.          ',
            '......          ',
        ) # Custom cursor map for the game
        custom_cursor = pygame.cursors.compile(
            custom_cursor_map, black='X', white='.', xor='o'
        ) # Compile the custom cursor map

        pygame.mouse.set_cursor((16, 16), (0, 0), *custom_cursor) # Set the custom cursor

        self.done = False # The done state of the client (loop control)

        pygame.display.set_caption('Microtrooopers - lobby') # Set the display caption
        pygame.mouse.set_visible(True) # Ensure that the mouse is visible

        rcv_thread = threading.Thread(target=self.handle_inputs_from_server) # Create a thread for handling inputs from the server
        self.threads.append(rcv_thread) # Append the thread to the list of threads
        rcv_thread.start() # Start the thread 

        resume_button_topleft = (surface.get_width() / 2 - 200, surface.get_height() / 2 - 50) # Resume button topleft
        resume_button = Button(*resume_button_topleft, 400, 50, 'Resume', self.do_unpause, font_color=(255, 255, 255), bg_color=(0, 0, 0, 255), outline_color=(255, 255, 255)) # Create a resume button
        exit_button_topleft = (surface.get_width() / 2 - 200, surface.get_height() / 2 + 50) # Exit button topleft
        exit_button = Button(*exit_button_topleft, 400, 50, 'Exit', self.stop, font_color=(255, 255, 255), bg_color=(0, 0, 0, 255), outline_color=(255, 255, 255)) # Create an exit button

        while not self.done: # While the client is not done, do the lobby logic
            events = pygame.event.get() # Get the events (exit manager)
            for event in events: # keyboard events handling loop
                if event.type == pygame.QUIT:
                    self.done = True
                    self.send('QUIT')
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.pause:
                            self.pause = True
                        else:
                            self.pause = False

            if self.state == 'lobby': # If the state is lobby, display the lobby user interface
                surface.blit(background, (0, 0)) # Blit the background to the surface
                surface.blit(shop_button_image, (0, 0)) # Blit the shop button image to the surface
                surface.blit(
                    hotbar_button_image,
                    ((surface.get_width() / 2)- (hotbar_button_image.get_width() / 2),
                    (surface.get_height()- 50 - hotbar_button_image.get_height()))
                ) # Blit the hotbar button image to the surface
            
            # Pause menu
            if self.pause:
                surface_filter = pygame.Surface((surface.get_width(), surface.get_height())) # Create a surface filter
                surface_filter.set_alpha(128)
                surface_filter.fill((0, 0, 0))
                surface.blit(surface_filter, (0, 0))
                
                # Resume button
                resume_button.draw(surface)
                

                # Exit button
                exit_button.draw(surface)


                resume_button.handle_event(events)
                exit_button.handle_event(events)

                # Handle button clicks
                


            
            pygame.display.flip() # Update the display

    def run(self) -> None:
        """
        Run the client.

        The run method is the main method of the client.
        It handles the login user interface, lobby user interface, and shop user interface.
        """

        self.login_ui()
        print('[DBG] from client.py.Client.run : login_ui done')
        self.lobby()

    def do_unpause(self) -> None:
        """
        Pause the client.
        """
        self.pause = False
    def do_pause(self) -> None:
        """
        Unpause the client.
        """
        self.pause = True
    def stop(self):
        self.done = True
        self.send('QUIT')
        pygame.quit()
        sys.exit()


client = Client(HOST, PORT)
client.run()
