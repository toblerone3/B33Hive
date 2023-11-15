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
import pickle

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
    client.containers.list(all=True)
    if start_name not in str(client.containers.list(all=True)):
        print("Invalid Start Name Received")
        cl_response = 'Invalid Start Name'.encode()
        client_socket.send(cl_response)
    else:
        print("Attempting to launch container:", start_name)
        container = client.containers.get(start_name)
        container.start()
        print("Container", start_name, "Launched Successfully!")
        cl_response = ("Container", start_name, "Launched Successfully!")
        cl_response = str(cl_response).encode()
        client_socket.send(cl_response)

def groupstart():
    containersInfo=[]
    containerlist = client.containers.list(all)
    for container in containerlist:
        container_name = container.name
        containersInfo.append(str(container_name))
    print(containersInfo)
    if containersInfo == [] or ("kippo-"+startgroup) not in containersInfo:
        print("Invalid Start Name Received")
        cl_response = 'Invalid Group Number'.encode()
        client_socket.send(cl_response)
    else:
        startcontainer = client.containers.get("kippo-"+startgroup)
        startcontainer.start()
        startcontainer = client.containers.get("sql-kippo-"+startgroup)
        startcontainer.start()
        startcontainer = client.containers.get("graph-kippo-"+startgroup)
        startcontainer.start()
        print("Container group:", startgroup, "Launched Successfully!")
        cl_response = ("Container group", startgroup, "Launched Successfully!")
        cl_response = str(cl_response).encode()
        client_socket.send(cl_response)


def stop():
    client.containers.list(all=True)
    if stop_name not in str(client.containers.list(all=True)):
        print("Invalid Start Name Received")
        cl_response = 'Invalid Start Name'.encode()
        client_socket.send(cl_response)
    else:
        print("Attempting to stop container:", stop_name)
        container = client.containers.get(stop_name)
        container.stop()
        cl_response = ("Container", stop_name, "Stopped Successfully!")
        cl_response = str(cl_response).encode()
        client_socket.send(cl_response)


def reverseshell():  # This Function Launches our Reverse Shell
    subprocess.run(["python", "reverseshell/reverseClient.py"])
    print("Shell Running")


def randomword(length): # user for human readable names, for naming containers. better an id tag
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def create():

    #print("\nthe default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP\n")
    # containersInfo=[]
    # containerlist = client.containers.list(all)
    # for container in containerlist:
    #     container_name = container.name
    #     containersInfo.append(str(container_name))
    # print(containersInfo)
    # if containersInfo == []:
    #     nextnum = 1
    # else:
    #     prevname = containersInfo[2]
    #     num = int(prevname[7:])
    #     nextnum = num + 1

    kipponame = "Cowrie-" + (str(randomword(4)))
    print("check 1")
    client.containers.create(name=kipponame, ports={'2222/tcp': 2222}, image="cowrie/cowrie")
    print("Check 2")
    created = ("The created containers are: ", kipponame)
    created = str(created)
    print(created)
    returnStr = created
    returnSig = returnStr.encode()
    client_socket.send(returnSig)


def destroy():
    client.containers.list(all=True)
    if rem_name not in str(client.containers.list(all=True)):
        print("Invalid Container ID")
        cl_response = "Invalid Container ID".encode()
        client_socket.send(cl_response)
    else:
        print("Attempting to remove container:", rem_name)
        container = client.containers.get(rem_name)
        container.remove()
        print("Container", rem_name, "Destroyed Successfully!")
        cl_response = ("Container", rem_name, "Destroyed Successfully!")
        cl_response = str(cl_response).encode()
        client_socket.send(cl_response)


def checkimage(client):
    while True:
        print("pulling images\n")
        client.images.pull('cowrie/cowrie')  # medium interaction SSH honeypot
        to_send = "Pulled Cowrie Successfully".encode()
        client_socket.send(to_send)
        break


def get_cpu_percentage(stats):
    cpu_stats = stats['cpu_stats']
    precpu_stats = stats['precpu_stats']

    if 'system_cpu_usage' in cpu_stats and 'system_cpu_usage' in precpu_stats:
        cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
        system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']
        cpu_usage_percentage = 100.0 * cpu_delta / system_delta
        return cpu_usage_percentage
    else:
        return None


def get_memory_percentage(stats):
    memory_stats = stats['memory_stats']
    memory_usage = memory_stats['usage']
    memory_limit = memory_stats['limit']

    if memory_limit > 0:
        memory_usage_percentage = (memory_usage / memory_limit) * 100
        return memory_usage_percentage
    else:
        return None


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
    global stop_name
    global rem_name
    global cpu_send
    global mem_send
    global startgroup
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
            if msg == "groupstart":
                time.sleep(1)
                startgroup = client_socket.recv(1024).decode()
                groupstart()
            if msg == "stop":
                time.sleep(1)
                stop_name = client_socket.recv(1024).decode()
                stop()

            if msg == "pullImages":
                checkimage(client)

            if msg == "Get Container Logs":
                print("Getting Container Logs")
                logname = cs.recv(1024).decode()
                if logname == "Cancel":
                    listen_for_client(cs)
                    break
                if logname not in str(client.containers.list(all=True)):
                    print("Ruh Roh Raggy")
                    log_response = "Not Valid".encode()
                    client_socket.send(log_response)
                    time.sleep(5)
                    endstream = 'EOT'.encode()
                    client_socket.send(endstream)
                else:
                    print(logname)
                    print("Check 1")
                    containerlogs = client.containers.get(logname)
                    print("Check 2")
                    print(containerlogs.logs())
                    logstosend = str(containerlogs.logs())
                    print(logstosend)
                    returnLogs = Fern.encrypt(logstosend.encode())
                    print(returnLogs)
                    client_socket.send(returnLogs)
                    time.sleep(5)
                    endstream = 'EOT'.encode()
                    client_socket.send(endstream)
            if msg == "Reverse Shell":
                print("Starting Shell")
                reverseshell()
            if msg == "Show Running Containers":
                print("Getting Containers")
                runningContainers = client.containers.list(all=True)
                containersInfo = []
                for container in runningContainers:
                    container_id = container.id
                    container_name = container.name
                    containersInfo.append({"Name": str(container_name),"ID": str(container_id[:12])})
                returnSig = Fern.encrypt(pickle.dumps(containersInfo))
                client_socket.send(returnSig)
            if msg == "Disconnect":
                print("Client Disconnecting")
                break
            if msg == "create containers":
                create()
            if msg == "destroy containers":
                time.sleep(1)
                rem_name = client_socket.recv(1024).decode()
                destroy()
            if msg == "Get Resources":
                print("Getting Container Resource Usage")
                rscname = cs.recv(1024).decode()
                if rscname not in str(client.containers.list(all=True)):
                    print("Invalid ID")
                    cl_response = "Invalid ID".encode()
                    client_socket.send(cl_response)
                else:
                    print(rscname)
                    print("Check 1")
                    if rscname in str(client.containers.list()):
                        print("Check 3")
                        container = client.containers.get(rscname)
                        for stat in container.stats(decode=True):
                            cpu_percentage = get_cpu_percentage(stat)
                            memory_percentage = get_memory_percentage(stat)
                            cpu_send = ''
                            mem_send = ''
                            if cpu_percentage is not None:
                                cpu_send = ("CPU Usage Percentage: {:.2f}%".format(cpu_percentage))
                                print(cpu_send)
                            if memory_percentage is not None:
                                mem_send = ("{:.2f}%".format(memory_percentage))
                                print(mem_send)
                            resources = ('CPU Usage is: ', cpu_send, '\n Memory Usage is: ', mem_send)
                            resources = str(resources).encode()
                            client_socket.send(resources)
                            break
                    else:
                        print("Container Not Running")
                        cl_response = "Container is not Running".encode()
                        client_socket.send(cl_response)

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
