# [GCT700] AR Project / Team 3
# Unity3d - UDP Receiver : this code will be rewritten in C#

import socket

TARGET_IP = '' # receive data from all hosts
PORT = 9999

# create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket
server_socket.bind((TARGET_IP, PORT)) # server ip, port
print("Start the server ...")

try:
    # waiting ...
    while True:
        # receive a message from the client
        data, addr = server_socket.recvfrom(1024) # get the message and address from client
        data = data.decode() # decode the message
        print(f"Received from {addr} / {data}")

        # send a message to the client
        data = f"Return: {data.upper()}" # uppercasing* (server function)
        server_socket.sendto(data.encode(), addr) # send message to client
except:
    print("Server Exception")
finally:
    server_socket.close()