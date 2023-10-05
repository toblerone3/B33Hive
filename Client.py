import os
import socket
import random
import hashlib
import subprocess
from threading import Thread
from datetime import datetime
from cryptography.fernet import Fernet
from time import sleep

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = input("Enter IP Address or for Local Chats: 127.0.0.1: ")
SERVER_PORT = 5003 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT)) #### From this point on, we're talking to the server
print("[+] Connected.")
key = s.recv(1024)  #### Current Fernet key from server

# close the socket
s.close()
