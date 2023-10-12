import socket
import tkinter
from tkinter import *
from PIL import ImageTk, Image

def show_data():
    global serverIP
    global rawPort
    serverIP = servIP.get()
    rawPort = port.get()
    print('Connecting to %s on port %s' % (servIP.get(), port.get()))
    print(serverIP)
    print(rawPort)
    win.quit()


win = Tk()
win.title("B33Hive: Connect to a Server")
#win.geometry("640x480")
win.resizable(True, True)
win.configure(bg='#010204')
#Loads an Image
Logo = Image.open("B33Hive.png")
photo = ImageTk.PhotoImage(Logo)
win.wm_iconphoto(False, photo) #this sets our icon
#Puts image into a label
label = tkinter.Label(image=photo, highlightthickness=0, background='#010204')
label.image = photo

label.grid(row=6, column=8, sticky=W, pady=4)

##These are descriptors for the entry boxes
Label(win, bg='black', fg='white', text='Server IP').grid(row=10, column= 7)
Label(win, bg='black', fg='white', text='Port').grid(row=11, column=7)

#These are our entry boxes
servIP = Entry(win, width=16, bg="gray25", fg='Orange2')
port = Entry(win, width=6, bg="gray25", fg='Orange2')

servIP.grid(row=10, column=8)
port.grid(row=11, column=8)

Button(win, bg='#ca891d', text='Connect', command=show_data).grid(row=13, column=9, pady=0)
Button(win, bg='#ca891d', text='Exit', command=win.quit).grid(row=13, column=7, pady=0)

mainloop() ### End of First Tkinter Window

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = serverIP  # ("Enter IP Address or for Local Chats: 127.0.0.1: ")
SERVER_PORT = rawPort  # server's port
separator_token = "<SEP>"  # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
SERVER_HOST = str(SERVER_HOST)
SERVER_PORT = int(SERVER_PORT)
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))  #### From this point on, we're talking to the server
print("[+] Connected.")

# close the socket
s.close()
