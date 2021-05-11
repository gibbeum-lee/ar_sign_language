# [GCT700] AR Project / Team 3

import socket, threading

def binder(client_socket, addr):
    print(f"Connected by {addr}")
    try:
        # waiting on the connection with a client ...
        while True:
            # initialization
            data = client_socket.recv(4) # RECEIVE the initial data of 4 byte
            length = int.from_bytes(data, "big") # byte data (big endien) to integer --- big endien for C# BitConverter
            
            # receiving data from client
            data = client_socket.recv(length) # RECEIVE the data of 4 byte
            msg = data.decode() # decode the binary data to string
            print(f"Received from {addr} / {msg}")

            # echoing
            msg = f"echo : {msg}"
            data = msg.encode() # string to byte (binary data)
            length = len(data) # length of the binary data to send
            client_socket.sendall(length.to_bytes(4, byteorder = "big")) # SEND the data size of little endien
            client_socket.sendall(data) # SEND the data to client
    except:
        # exception occurs when disconnected
        print(f"except : {addr}")
    finally:
        # close the socket when disconnected
        client_socket.clode()

# create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # socket level, data format
server_socket.bind(('', 9999)) # server ip, port
server_socket.listen(); # start listening ...

try:
    # waiting ...
    while True:
        # when a client access, accept() occurs on the server-side
        client_socket, addr = server_socket.accept() # get client socket & addr from accept
        th = threading.Thread(target = binder, args = (client_socket, addr)) # create a thread binding with the client
except:
    print("Server Exception")
finally:
    server_socket.close()