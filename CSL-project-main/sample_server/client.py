import socket
host = socket.gethostname()
port = 5000
client_socket = socket.socket()
client_socket.connect((host, port))
message = input(' -> ')
# enter -terminate- to close the connection
while message.lower().strip() != 'terminate':
    # send the entered message to the server
    client_socket.send(message.encode())
    # get the server's response
    data = client_socket.recv(1024).decode()
    print('Recieved from server: ' + str(data))
    # again ...
    message = input(' -> ')
client_socket.close()