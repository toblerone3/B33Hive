import socket
import tkinter
import subprocess
import os
import platform
from tkinter import *
from PIL import ImageTk, Image


whichOS = platform.system()
print("Launching",whichOS, "B33Hive Client") ##Just a debug, we need this logic later

Attempts = 0

PIN = ''


def button7(): ## THIS IS HOW WE SEND TO THE SERVER, THIS CAN BE REPEATED AD-NAUSEAM
    signal_Send = "Button 7"
    sigSent = signal_Send.encode()
    s.send(sigSent)


def pullImages(): ## Further Example
    signal_Send = "pullImages"
    sigSent = signal_Send.encode()
    s.send(sigSent)


def runningContainers(): ## Further Example
    signal_Send = "Show Running Containers"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    while True:
        currentcontainers = s.recv(2048)
        printcontainers = currentcontainers.decode()
        print("Current Containers:")
        print(printcontainers)#[1:][:-1]
        if currentcontainers != '':
            break


def reverseshell():  # Launches our Reverse Shell
    signal_Send = "Reverse Shell"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    # os.system("start cmd /k /reverseshell/reverseClient.py")
    subprocess.run(["python", "reverseshell/reverseServer.py"])


def disconnect():
    print("Disconnecting...")
    signal_Send = "Disconnect"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    s.close()
    quit()


def show_data():
    global serverIP
    global rawPort
    global CLIENT_PIN
    serverIP = servIP.get()
    rawPort = port.get()
    CLIENT_PIN = entryPIN.get()
    print('Connecting to %s on port %s' % (servIP.get(), port.get()))
    print(serverIP)
    print(rawPort)
    win.destroy()

def menu1Grab():
    global serverIP
    global rawPort
    serverIP = servIP.get()
    rawPort = port.get()
    print('Connecting to %s on port %s' % (servIP.get(), port.get()))
    print(serverIP)
    print(rawPort)
    win.destroy()
    pinMenu()

def menu2Grab():
    global CLIENT_PIN
    CLIENT_PIN = entryPIN.get()
    print(CLIENT_PIN)
    winpin.destroy()

def debugMain():  # This is how we skip to the main menu for debug, does not connect to the server
    win.destroy()
    mainMenu()


def mainMenu():  # This is our main menu, functionalized, so we can debug and call later
    win2 = Tk()
    win2.title("B33Hive: Main Menu")
    # win.geometry("640x480")
    win2.resizable(True, True)
    win2.configure(bg='#010204')
    # Loads an Image
    Logo = Image.open("B33Hive.png")
    photo = ImageTk.PhotoImage(Logo)
    # Puts image into a label
    imageLogo = tkinter.Label(image=photo, highlightthickness=0, background='#010204')
    imageLogo.image = photo
    win2.wm_iconphoto(False, photo)  # sets icon

    imageLogo.grid(row=5, column=2, sticky=W, pady=4)

    # Lists all our buttons DO NOT USE ROW 5 as this will break the logo formatting
    # Left Row
    Button(win2, bg='#ca891d', activebackground='gray25', text='Pull / Update Images', command=pullImages).grid(row=1, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='See Current Containers', command=runningContainers).grid(row=2, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button3', ).grid(row=3, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button4', ).grid(row=4, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button5', ).grid(row=6, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button6', ).grid(row=7, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button7', command=button7 ).grid(row=8, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button8', ).grid(row=9, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Exit', command=quit).grid(row=10, column=1, pady=0)
    # Right Row
    Button(win2, bg='#ca891d', activebackground='gray25', text='button9', ).grid(row=1, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button10', ).grid(row=2, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button11', ).grid(row=3, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button12', ).grid(row=4, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button13', ).grid(row=6, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button14', ).grid(row=7, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button15', ).grid(row=8, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Start Remote Shell', command=reverseshell).grid(row=9, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Disconnect', command=disconnect).grid(row=10, column=3, pady=0) ##Both Buttons currently call disconnect due to the fact we can't recall our login screen

    entryBox = Entry(win2, width=32, bg="gray25", fg='#ca891d')
    entryBox.grid(row=9, column=2)
    # This entry box is to send commands to the server,
    # clientInput = entryBox.get() #This is how we'll grab from the entry box later

    mainloop()

def pinMenu():
    global entryPIN
    global winpin
    winpin = Tk()
    winpin.title("B33Hive: Connect to a Server")
    # win.geometry("640x480")
    winpin.resizable(True, True)
    winpin.configure(bg='#010204')
    # Loads an Image
    Logo = Image.open("B33Hive.png")
    photo = ImageTk.PhotoImage(Logo)
    winpin.wm_iconphoto(False, photo)  # this sets our icon
    # Puts image into a label
    conLogo = Label(image=photo, highlightthickness=0, background='#010204')
    conLogo.image = photo
    conLogo.grid(row=5, column=8, sticky=W, pady=4)
    Label(winpin, bg='black', fg='white', text='NOTE: If there is no pin, leave blank...').grid(row=7, column=8)
    entryPIN = Entry(winpin, width=6, bg="gray25", fg='#ca891d')
    entryPIN.grid(row=12, column=8)
    Label(winpin, bg='black', fg='white', text='PIN (Optional):').grid(row=12, column=7)
    Button(winpin, bg='#ca891d', activebackground='gray25', text='Enter', command=menu2Grab).grid(row=13, column=9, pady=0)
    Button(winpin, bg='#ca891d', activebackground='gray25', text='Exit', command=winpin.quit).grid(row=13, column=7, pady=0)
    winpin.mainloop()


win = Tk()
win.title("B33Hive: Connect to a Server")
# win.geometry("640x480")
win.resizable(True, True)
win.configure(bg='#010204')
# Loads an Image
Logo = Image.open("B33Hive.png")
photo = ImageTk.PhotoImage(Logo)
win.wm_iconphoto(False, photo)  # this sets our icon
# Puts image into a label
conLogo = tkinter.Label(image=photo, highlightthickness=0, background='#010204')
conLogo.image = photo

conLogo.grid(row=5, column=8, sticky=W, pady=4)


Label(win, bg='black', fg='white', text='A Dynamic Honeypot C2 Server and Client').grid(row=7, column=8)
Label(win, bg='black', fg='white', text='').grid(row=8, column=8) ##Blank Labels are Spacers because Tkinter.grid is bad
# These are descriptors for the entry boxes
Label(win, bg='black', fg='white', text='Server IP').grid(row=10, column=7)
Label(win, bg='black', fg='white', text='Port').grid(row=11, column=7)
####Label(win, bg='black', fg='white', text='PIN (Optional)').grid(row=12, column=7) ####REDUNDANT####


# These are our entry boxes
servIP = Entry(win, width=16, bg="gray25", fg='#ca891d')
port = Entry(win, width=6, bg="gray25", fg='#ca891d')
#entryPIN = Entry(win, width=6, bg="gray25", fg='#ca891d') ####REDUNDANT####

servIP.grid(row=10, column=8)
port.grid(row=11, column=8)
#entryPIN.grid(row=12, column=8) ####REDUNDANT####

Button(win, bg='#ca891d', activebackground='gray25', text='Connect', command=menu1Grab).grid(row=13, column=9, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Exit', command=win.quit).grid(row=13, column=7, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Debug Main', command=debugMain).grid(row=1, column=9, pady=0)
# added 'Debug Main' to load main menu without having to connect to the server, remove before hand in

mainloop()  # End of First Tkinter Window
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
s.connect((SERVER_HOST, SERVER_PORT))  # From this point on, we're talking to the server


recvPIN = s.recv(4096)
SERVER_PIN = recvPIN.decode('utf-8')


# print("Variable: SERVER_PIN:", SERVER_PIN,"Variable recvPIN:", recvPIN) # (debug option for PINS)

totalAttempts = 3
while True:
    if SERVER_PIN == '8888': ##8888 is the default pin, if the server doesn't have a pin, it will be automatically set to 8888, so we're checking if we can skip
        print("Server Has No Pin, Continuing...")
        break
    if SERVER_PIN != '8888':
        if SERVER_PIN != CLIENT_PIN and Attempts < 2:
            Attempts = Attempts + 1
            print(SERVER_PIN, CLIENT_PIN)
            print("Incorrect PIN", totalAttempts-Attempts, "remaining...")
            print(Attempts)
            pinMenu()
        elif SERVER_PIN == CLIENT_PIN:
            print("Correct PIN")
            print("Connected.")
            mainMenu()
        else:
            print("Pin Attempts Exceed, Disconnecting")
            disconnect()




