import pygame
import pygame_menu
import socket
import sys

if not pygame.get_init():
    pygame.init()

HOST, PORT = 'localhost', 5555


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.state = 'login'

    def send(self, message):
        message = message.encode('utf-8')
        self.client_socket.send(message)

    def receive(self):
        response = self.client_socket.recv(1024)
        response = response.decode('utf-8')
        return response

    def login_ui(self):
        surface = pygame.display.set_mode((800, 600))
        email = str()
        password = str()
        self.menu = pygame_menu.Menu(
            'Microtrooopers - login',
            800,
            600,
            theme=pygame_menu.themes.THEME_BLUE,
        )
        self.menu.add.text_input(
            'Email: ', default=email, maxchar=20, textinput_id='email'
        )
        self.menu.add.text_input(
            'Password: ', default=password, maxchar=20, textinput_id='password'
        )
        self.menu.add.button('Login', self.login)
        self.menu.add.button('Register', self.register)
        while self.state == 'login':
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.send('QUIT')
                    pygame.quit()
                    sys.exit()
            self.menu.update(events)
            self.menu.draw(surface)
            pygame.display.flip()
        print('Login done')

    def register(self):
        pass

    def login(self):
        data = self.menu.get_input_data()
        if not data['email'] or not data['password']:
            return
        self.send(f"{data['email']} {data['password']}")
        response = self.receive()
        if response == 'LOGIN ERROR':
            print('Login error')
        else:
            print('Login OK')
            self.menu.close()
            self.state = 'lobby'

    def lobby(self):
        surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        background = pygame.image.load('../assets/lobby.png')
        background = pygame.transform.scale(background, (1920, 1080))

        shop_button_image = pygame.image.load('../assets/shop_button.png')
        shop_button_image = shop_button_image.convert_alpha()
        shop_button_area = pygame.Rect(0, 0, *shop_button_image.get_size())

        hotbar_button_image = pygame.image.load('../assets/hotbar.png')
        hotbar_button_image = hotbar_button_image.convert_alpha()

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
        )
        print(len(custom_cursor_map))
        custom_cursor = pygame.cursors.compile(
            custom_cursor_map, black='X', white='.', xor='o'
        )

        pygame.mouse.set_cursor((16, 16), (0, 0), *custom_cursor)

        self.done = False

        pygame.display.set_caption('Microtrooopers - lobby')
        pygame.mouse.set_visible(True)

        while not self.done:
            message = self.receive()
            print(f'[DBG] from client.py.179 : {message=}')
            if len(message.split()) >= 2:
                head, tail = message.split()[0], message.split()[1:]
                if head == 'SHOP':
                    if tail[0] == 'OPEN':
                        print('Shop opened')
                        self.state = 'shop'
                    elif tail[0] == 'CLOSE':
                        print('Shop closed')
                        self.state = 'lobby'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.send('QUIT')
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                        self.send('QUIT')
                        pygame.quit()
                        sys.exit()
            if self.state == 'lobby':
                surface.blit(background, (0, 0))
                surface.blit(shop_button_image, (0, 0))
                surface.blit(
                    hotbar_button_image,
                    (
                        (surface.get_width() / 2)
                        - (hotbar_button_image.get_width() / 2),
                        (
                            surface.get_height()
                            - 50
                            - hotbar_button_image.get_height()
                        ),
                    ),
                )
            
            elif self.state == 'shop':
                surface.blit(background, (0, 0))
                

            pygame.display.flip()

    def run(self):
        self.login_ui()
        print('switching to lobby')
        self.lobby()


client = Client(HOST, PORT)
client.run()
