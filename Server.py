import socket
from threading import Thread
import docker
import os
import subprocess
import random
import string
import sys
from pathlib import Path


client = docker.from_env() # detects the docker installation and assigns this to a variable

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# server's IP address
SERVER_HOST = '127.0.0.1'    # IPAddr # IMPORTANT - BEFORE SUBMISSION, REPLACE '127.0.0.1' WITH IPAddr (as is commented, this is for development ONLY)
SERVER_PORT = 5003  # port we want to use
SERVER_PIN = '8888'
Attempts = 0
print("Current Server IP address: " + IPAddr)
PIN_ASK = input("Do you want to protect your Server with a PIN? [Y/N]: ")

while PIN_ASK.lower() not in ('y', 'n'):
    if Attempts >= 3:
        print("No Attempts Left, Quitting.")
        quit()
    PIN_ASK = input("Please Enter Only a Y or an N Character: ")
    Attempts += 1
    print(Attempts, "/ 3 Attempts Left")


if PIN_ASK.lower() == 'n':
    print("PIN Not Set, Continuing...")
    SERVER_PIN = '8888'
if PIN_ASK.lower() == 'y':
    SERVER_PIN = input("Enter a Four Digit Pin for your server: ")

Attempts = 0


def reverseshell():
    #with open("reverseshell/reverseClient.py") as f:
        #exec(f.read())
    #os.system("start cmd /k reverseClient.py")
    subprocess.run(["python", "reverseshell/reverseClient.py"])
    print("Shell Running")


def checkimage():
    imageflag = Path("./flag")
    if imageflag.is_file():
        print("\nimages already pulled, proceeding\n")
        print("the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        #menu()

    else:
        print("pulling images\n")
        open("flag", "w")
        client.images.pull('dariusbakunas/kippo')  # medium interaction SSH honeypot
        print("kippo pulled...")
        client.images.pull('mysql')  # dependency for kippo - data storage
        print("mySQL pulled...")
        client.images.pull('dariusbakunas/kippo-graph')  # dependency for kippo - analysing kippo data
        print("kippo-graph pulled...")

        print("\nthe default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")

        #menu()

while True:
    if Attempts >= 3:
        print("No Attempts Left, Quitting.")
        quit()
    if len(SERVER_PIN) == 4 and SERVER_PIN.isdigit() is True:
        print("Your PIN:", SERVER_PIN, "is now set!")
        break
    if len(SERVER_PIN) != 4 or SERVER_PIN.isdigit() is False:
        Attempts += 1
        print(Attempts, "/ 3 Attempts Left")
        SERVER_PIN = input("Please enter a FOUR Digit Pin: ")


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

def listen_for_client(cs):
    """
    This function keep listening for a message from cs socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from cs socket
            msg = cs.recv(1024).decode()
            print(msg)
            if msg == "Button 1":
                print("Button 1 Okay")
                checkimage()
            if msg == "Button 7":
                print("Button 7 Okay")
            if msg == "Reverse Shell":
                print("Starting Shell")
                reverseshell()
                break
            if msg == "Disconnect":
                print("Client Disconnecting")
                break
            msg = ""
            #quit() ##PLACE HOLDER, WE WILL WANT TO MAP MESSAGES TO COMMANDS FROM HERE
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)



while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.") ##we have no fucking idea why this prints an additional number (eg: 51xxx)
    # print(client_socket)
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon, so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
    sentPIN = SERVER_PIN.encode()
    client_socket.send(sentPIN)  # NSend the pin to the client - IMPORTANT, ENCRYPT THIS LATER

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
