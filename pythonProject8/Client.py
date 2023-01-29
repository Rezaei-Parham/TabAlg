import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

client.sendall(b"Hello, Server!")
response = client.recv(1024).decode()
print(f"Received: {response}")

client.close()
