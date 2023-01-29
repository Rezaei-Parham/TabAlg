import socket
host = socket.gethostname()
port = 5000
server_socket = socket.socket()
server_socket.bind((host, port))
# only one clinet can connect
server_socket.listen(1)
connection, address = server_socket.accept()
# print client's information
print("Connection from: " + str(address))
while True:
    # recieve the clients request
    data = connection.recv(1024).decode()
    if not data:
        break
    print("From connected user: " + str(data))
    # send a response to the client
    data = input(' -> ')
    connection.send(data.encode())
connection.close()