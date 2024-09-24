import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)
print('Server listening on port 12345')
client, address = server.accept()
print(f'Connection from {address}')
client.send(b'Hello, client!')
client.close()