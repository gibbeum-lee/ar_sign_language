# [GCT700] AR Project / Team 3
# Python - UDP Message Sender
# This code will be merged with WebCam capturing and model prediction code

import socket

RECEIVER_IP = 'localhost'
RECEIVER_PORT = 9999

# create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket

try:
    # waiting ...
    while True:
        # send a message to the server
        msg = input("->") # promt the message
        msg = bytes(msg.encode()) # encode the message
        client_socket.sendto(msg, (RECEIVER_IP, RECEIVER_PORT))

        # receive a message from the server, if needed
#        data, addr = client_socket.recvfrom(1024) # get the message and address from server
#        data = str(data.decode()) # decode the message
#        print(f"Received from Server / {data}")
finally:
    client_socket.close()