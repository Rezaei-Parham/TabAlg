import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 12345))
server.listen(5)

while True:
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address}")
    data = client_socket.recv(1024).decode()
    print(f"Received: {data}")
    client_socket.sendall(b"ACK")
    client_socket.close()
