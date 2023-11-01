import socket
import time
from threading import Thread
import docker
import os
import subprocess
import random
import string
import sys
import rsa
from pathlib import Path
from cryptography.fernet import Fernet

key = Fernet.generate_key()
Fern = Fernet(key)



dockerDebug = input("Launch with Docker? [Y/N] (DEBUG, REMOVE BEFORE HAND IN):")
while dockerDebug.lower() not in ('y', 'n'):
    dockerDebug = input("Please Enter Only a Y or an N Character: ")
if dockerDebug.lower() == 'n':
    print("Alright, just don't forget, Dockers not gonna work")
if dockerDebug.lower() == 'y':
    client = docker.from_env()

genKeys = input("Generate new RSA Keys? (Recommended after Installation)[Y/N]:")
while genKeys.lower() not in ('y', 'n'):
    genKeys = input("Please Enter Only a Y or an N Character: ")
if genKeys.lower() == 'n':
    print("Continuing...")
if genKeys.lower() == 'y':
    print("Generating new RSA Keys...")
    # generate RSA key pair
    public_key, private_key = rsa.newkeys(2048)
    # save key pair to files
    with open('RSA/serverpublic.pem', 'wb') as f:
        f.write(public_key.save_pkcs1())
    with open('RSA/serverprivate.pem', 'wb') as f:
        f.write(private_key.save_pkcs1())

    print('RSA PGP key pair generated successfully')

# Loads Public Key into memory
f_pub = open("RSA/serverpublic.pem", 'rb')
public_key = f_pub.read()
f_pub.close()
# Loads Private Key into Memory
f_private = open("RSA/serverprivate.pem", 'rb')
private_key = f_private.read()
f_private.close()

print("Keys Loaded")

# Line 21 commented out, replace lines 11-18 with this one liner before hand in, this is for ease of use
# client = docker.from_env()  # detects the docker installation and assigns this to a variable

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# server's IP address
SERVER_HOST = '127.0.0.1'  # IPAddr # IMPORTANT - BEFORE SUBMISSION, REPLACE '127.0.0.1' WITH IPAddr (as is commented, this is for development ONLY)
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

def start():
    print("Check 1")
    client.containers.list(all=True)
    print("Check 2")
    print(start_name)
    print("Check 3")
    client.containers.run(start_name)
    print("Check 4")
    print("container status: " + client.name.status())
    input("\nfinished, press enter...\n")

def reverseshell():  # This Function Launches our Reverse Shell
    subprocess.run(["python", "reverseshell/reverseClient.py"])
    print("Shell Running")


def randomword(length): # user for human readable names, for naming containers. better an id tag
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def create():

    print("\nthe default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP\n")

    kipponame = "kippo-" + randomword(8)
    sqlname = "sql-" + kipponame
    graphname = "graph-" + kipponame


    #environment=["links={sqlname: 'mysql'}, KIPPO_DB_PASSWORD=K[5UZ4ELSf;e)gX=, KIPPO_SRV_NAME=Barry B's Workstation"]
    client.containers.create(name=kipponame, environment=["links={sqlname: 'mysql'}, KIPPO_DB_PASSWORD=K[5UZ4ELSf;e)gX=, KIPPO_SRV_NAME=Barry B's Workstation"], image="dariusbakunas/kippo")
    client.containers.create(name=sqlname, environment=["MYSQL_ROOT_PASSWORD=K[5UZ4ELSf;e)gX="], image='mysql')
    client.containers.create(name=graphname, links={sqlname: 'mysql'},image="dariusbakunas/kippo-graph")

    created = "\nthe created containers are: " + kipponame + '' + sqlname + '' + graphname

    print(created)
    returnStr = created
    returnSig = returnStr.encode()
    client_socket.send(returnSig)


def destroy():
    destroystatement = "please enter the suffix of the container group to delete: "
    destroystatementencode = destroystatement.encode()
    client_socket.send(destroystatementencode)
    #time.sleep(1)
    #destroyname = client_socket.recv(1024).decode()


    try:
        destroyname = client_socket.recv(1024).decode()
        print(destroyname)

        destroykippo = "kippo-" + destroyname
        destroysql = "sql-" + destroykippo
        destroygraph = "graph-" + destroykippo

        print("deleted kippo container with name: " + destroykippo)
        client.containers.remove(name=destroykippo, v=True, force=True)

        client.containers.remove(name=destroysql, v=True, force=True)
        print("deleted kippo container with name: " + destroykippo)
        client.containers.remove(name=destroygraph, v=True, force=True)
        print("deleted kippo container with name: " + destroygraph)

        destroyed = "deleted kippo container with names: " + destroykippo + "" + destroysql + "" + destroygraph

        sigSent = destroyed.encode()
        s.send(sigSent)


    except:
        input("\nsuffix not known or incorrectly typed, trying again\n")



def checkimage():
    imageflag = Path("./flag")
    if imageflag.is_file():
        print("\nimages already pulled, proceeding\n")
        print("the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")

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


def listen_for_client(cs):
    global start_name
    """
    This function keep listening for a message from cs socket
    Whenever a message is received, Follows the IF Statement Chain
    """
    while True:
        try:
            # keep listening for a message from cs socket
            msg = cs.recv(1024).decode()
            print(msg)
            if msg == "Begin Key Exchange":
                cpub = rsa.PublicKey.load_pkcs1(cs.recv(2048))
                print(cpub)
                encmsg = SERVER_PIN.encode('UTF-8')
                client_socket.send(rsa.encrypt(encmsg, cpub))
                time.sleep(0.5)
                client_socket.send(rsa.encrypt(key, cpub))

            if msg == "start":
                time.sleep(1)
                start_name = client_socket.recv(1024).decode()
                start()

            if msg == "pullImages":
                imageflag = Path("./flag")
                print("Pulling Current Images..")
                if imageflag.is_file():
                    returnStr = "Images Already Pulled"
                    returnSig = returnStr.encode()
                    client_socket.send(returnSig)
                else:
                    checkimage()
            if msg == "Get Container Logs":
                print("Getting Container Logs")
                logname = cs.recv(1024).decode()
                if logname == "Cancel":
                    listen_for_client(cs)
                    break
                else:
                    print(logname)
                    print("Check 1")
                    containerlogs = client.containers.get(logname)
                    print("Check 2")
                    print(containerlogs.logs())
                    logstosend = str(containerlogs.logs())
                    returnLogs = logstosend.encode()
                    client_socket.send(returnLogs)
            if msg == "Reverse Shell":
                print("Starting Shell")
                reverseshell()
            if msg == "Show Running Containers":
                print("Getting Containers")
                runningContainers = str(client.containers.list(all=True))
                returnSig = Fern.encrypt(runningContainers.encode())
                client_socket.send(returnSig)
            if msg == "Disconnect":
                print("Client Disconnecting")
                break
            if msg == "create containers":
                create()
            if msg == "destroy containers":
                destroy()

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


    #client_public = s.recv(2048)
    #enc_PIN = rsa.encrypt(SERVER_PIN, client_public)


# NSend the pin to the client - IMPORTANT, ENCRYPT THIS LATER

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
