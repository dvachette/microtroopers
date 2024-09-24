import socket

# do a client for a server hosted in my machine

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))
response = client.recv(4096)
print(response.decode())
client.close()
