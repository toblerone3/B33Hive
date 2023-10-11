import socket
from tkinter import *


def show_data():
    global serverIP
    global rawPort
    serverIP = servIP.get()
    rawPort = port.get()
    print( 'Connecting to %s on port %s' % (servIP.get(), port.get()) )
    print(serverIP)
    print(rawPort)
    win.quit()


win = Tk()
win.title("B33Hive: Connect to a Server")
win.geometry("640x480")
Label( win, text='Server IP' ).grid( row=0 )
Label( win, text='Port' ).grid( row=1 )

servIP = Entry( win )
port = Entry( win )

servIP.grid( row=0, column=1 )
port.grid( row=1, column=1 )

Button( win, text='Exit', command=win.quit ).grid( row=3, column=0, sticky=W, pady=4 )
Button( win, text='Connect', command=show_data ).grid( row=3, column=1, sticky=W, pady=4 )

mainloop()


# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = serverIP #("Enter IP Address or for Local Chats: 127.0.0.1: ")
SERVER_PORT = rawPort # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
SERVER_HOST = str(SERVER_HOST)
SERVER_PORT = int(SERVER_PORT)
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT)) #### From this point on, we're talking to the server
print("[+] Connected.")


# close the socket
s.close()
