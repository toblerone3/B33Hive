import socket

# server's IP address
SERVER_HOST = '127.0.0.1'  # input("Enter Your Current IPV4 Address: ") #### CHANGE THIS BEFORE SUBMISSIONS

SERVER_PORT = 5003  # port we want to use
separator_token = "<SEP>"  # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

#


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    # print(f"[+] {client_address} connected.") ##we have no fucking idea why this prints an additional number (eg: 51xxx)
    # print(client_socket)
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    # t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon, so it ends whenever the main thread ends
    # t.daemon = True
    # start the thread
    # t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
