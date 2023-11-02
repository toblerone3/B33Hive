import platform
import re
import socket
import subprocess
import time
import tkinter
from idlelib.tooltip import Hovertip
from pathlib import Path
from tkinter import *
from tkinter import messagebox  # Weirdly, despite importing tkinter *, we still need this

import rsa
from PIL import ImageTk, Image
from cryptography.fernet import Fernet

key = Fernet.generate_key()
Fern = Fernet(key)


whichOS = platform.system()
print("Launching",whichOS, "B33Hive Client") ##Just a debug, we need this logic later

Attempts = 0

PIN = ''

# --------------------------------------------------- RSA GENERATION ---------------------------------------------------

rsaflag = Path("RSA/rsaflag")
if rsaflag.is_file():
    print("\nRSA Keys Already Generated\n")
else:
    print("Generating new RSA Keys...")
    open("RSA/rsaflag", "w")
    # generate RSA key pair
    public_key, private_key = rsa.newkeys(2048)
    # save key pair to files
    with open('RSA/clientpublic.pem', 'wb') as f:
        f.write(public_key.save_pkcs1())
    with open('RSA/clientprivate.pem', 'wb') as f:
        f.write(private_key.save_pkcs1())
    print('RSA PGP key pair generated successfully')

# Loads Public Key into memory
f_pub = open("RSA/clientpublic.pem", 'rb')
publicdata = f_pub.read()
public_key = rsa.PublicKey.load_pkcs1(publicdata, 'PEM')
f_pub.close()
# Loads Private Key into Memory
f_private = open("RSA/clientprivate.pem", 'rb')
privatedata = f_private.read()
private_key = rsa.PrivateKey.load_pkcs1(privatedata, 'PEM')
f_private.close()

print("Keys Loaded")


def pinexchange(): ## Further Example
    global SERVER_PIN
    global key
    global Fern
    print("Beginning Key Exchange")
    signal_Send = "Begin Key Exchange"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    time.sleep(0.5)
    s.send(public_key.save_pkcs1("PEM"))  # then we send it using s.send
    encPIN = s.recv(3096)
    decPIN = rsa.decrypt(encPIN, private_key).decode()
    print(decPIN, '# DEBUG')
    SERVER_PIN = str(decPIN)
    key = s.recv(1024)
    key = rsa.decrypt(key, private_key).decode()
    Fern = Fernet(key)
    print(Fern)


# ---------------------------------------------- DISCONNECTIONS AND DEBUG ----------------------------------------------


def disconnect():
    print("Disconnecting...")
    signal_Send = "Disconnect"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    s.close()
    quit()


def debugMain():  # This is how we skip to the main menu for debug, does not connect to the server
    win.destroy()
    mainMenu()


# --------------------------------------------------- LOG RETRIEVAL ----------------------------------------------------

def logcontainers(): ## THIS IS HOW WE SEND TO THE SERVER, THIS CAN BE REPEATED AD-NAUSEAM
    runningContainers()
    signal_Send = "Get Container Logs"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    logMenu()


def logMenuGrab():
    global loggrab
    loggrab = entryLog.get()
    print(loggrab)
    winlog.destroy()
    signal_Send = loggrab
    sigSent = signal_Send.encode()
    s.send(sigSent)
    logsreturned = s.recv(11264)
    print(logsreturned)
    enclogs = logsreturned.decode()
    print(enclogs)
    declogs = Fern.decrypt(enclogs)
    strlogs = str(declogs)
    logwrap = '\n'.join(re.findall('.{1,128}', strlogs))
    f = open("%sContainerLogs.txt" % loggrab, "w")
    f.write(logwrap)
    print(declogs[4:]) # DEBUG ONLY


def logquit():
    signal_Send = "Cancel"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    winlog.destroy()

# ------------------------------------------------------- DOCKER -------------------------------------------------------


def pullImages(): ## Further Example
    hangwarning = messagebox.askyesnocancel("Confirmation", "This Menu will freeze while the server pulls"
                                            " the images, are you sure you want to pull the images now?")
    print(hangwarning)
    if hangwarning is True:
        signal_Send = "pullImages"  # We store what we want to send to the server here
        sigSent = signal_Send.encode()  # Then we encode it into bytes
        s.send(sigSent)  # then we send it using s.send
        while True: # we then start a listener
            pulledimages = s.recv(2048) # and wait for a message from the server
            printimages = pulledimages.decode()  # we then turn it back into a string
            print(printimages) # and print it
            if pulledimages != '':  # this just checks to see if we got anything, once the server responds the loop breaks
                break
        messagebox.showinfo("Pulled Images", "Images were successfully pulled / updated")

def startEntry():
    global startWin
    global containerStart
    startWin = Toplevel()
    startWin.title("Enter container name")
    startWin.resizable(True, True)
    startWin.configure(bg='#010204')
    containerStart = Entry(startWin, width=6, bg="gray25", fg='#ca891d')
    containerStart.grid(row=12, column=8)
    Label(startWin, bg='black', fg='white', text='Container name:').grid(row=12, column=7)
    Button(startWin, bg='#ca891d', activebackground='gray25', text='Enter', command=start).grid(row=13, column=9, pady=0)
    Button(startWin, bg='#ca891d', activebackground='gray25', text='Exit', command=startWin.quit).grid(row=13, column=7, pady=0)


def start(): ## Further Example
    global startGrab
    startGrab = containerStart.get()
    startWin.destroy()
    signal_Send = "start"
    startContainer_send = startGrab.encode()
    sigSent = signal_Send.encode()
    s.send(sigSent)
    time.sleep(1)
    s.send(startContainer_send)


def createcontainer():
    signal_Send = "create containers"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    while True:
        createoutput = s.recv(2048)  # and wait for a message from the server
        createoutput = createoutput.decode()  # we then turn it back into a string
        print(createoutput)  # and print it
        if createoutput != '':  # this just checks to see if we got anything, once the server responds the loop breaks
            break


def destroycontainer():
    signal_Send = "destroy containers"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    while True:
        destroystatement = s.recv(2048)  # and wait for a message from the server
        destroystatement = destroystatement.decode()  # we then turn it back into a string
        print(destroystatement)  # and print it

        destroyresponse = str(input())
        print(destroyresponse)
        sigSent = destroyresponse.encode()
        s.send(sigSent)

        destroyres = s.recv(2048)
        destroyresult = destroyres.decode()
        print(destroyresult)

        break


def runningContainers(): ## Further Example
    signal_Send = "Show Running Containers"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    while True:
        currentcontainers = s.recv(2048)
        enccontainers = currentcontainers.decode()
        printcontainers = Fern.decrypt(enccontainers)
        print("Current Containers:")
        print(printcontainers)#[1:][:-1]
        if currentcontainers != '':
            break



def reverseshell():  # Launches our Reverse Shell
    userwarning = messagebox.askyesnocancel("Confirmation", "This Menu will freeze while using the Remote Shell"
                                            "\nType Exit to return to the Main Menu"
                                            "\nLaunch the Remote Shell?")
    print(userwarning)
    if userwarning is True:
        signal_Send = "Reverse Shell"
        sigSent = signal_Send.encode()
        s.send(sigSent)
        # os.system("start cmd /k /reverseshell/reverseClient.py")
        subprocess.run(["python", "reverseshell/reverseServer.py"])
    elif userwarning is False:
        print("Reverting to Main Menu")
    elif userwarning is None:
        print("No Input Detected")

# ------------------------------------------------- ENTRY BOX GRABBERS -------------------------------------------------


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
    #pinexchange()


# ------------------------------------------------------- MENU'S -------------------------------------------------------


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
    Button(win2, bg='#ca891d', activebackground='gray25', text='Start Container', command=startEntry).grid(row=6, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button6', ).grid(row=7, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Get Container Logs', command=logcontainers).grid(row=8, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button8', ).grid(row=9, column=1, pady=0)
    exitButton = Button(win2, bg='#ca891d', activebackground='gray25', text='Exit', command=quit)  # This allows us to reference a button later
    # Right Row
    Button(win2, bg='#ca891d', activebackground='gray25', text='create containers', command=createcontainer).grid(row=1, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='destroy containers', command=destroycontainer).grid(row=2, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button11', ).grid(row=3, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button12', ).grid(row=4, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button13', ).grid(row=6, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button14', ).grid(row=7, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='button15', ).grid(row=8, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Start Remote Shell', command=reverseshell).grid(row=9, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Disconnect', command=disconnect).grid(row=10, column=3, pady=0) ##Both Buttons currently call disconnect due to the fact we can't recall our login screen

    # TO-DO: We should remove this and the exit button before hand in as they are only for debug purposes
    exitbuttontip = Hovertip(exitButton, "DO NOT USE IF YOU'RE CONNECTED TO THE SERVER")  # Here we're referencing the exit button we saved as a variable
    exitButton.grid(row=10, column=1, pady=0)  # Here we tell tkinter to put exitbutton into the grid

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
    winpin.bind('<Return>', lambda e, w=winpin: menu2Grab())
    winpin.mainloop()


def logMenu():
    global entryLog
    global winlog
    winlog = Tk()
    winlog.title("B33Hive: Input a Container")
    # win.geometry("640x480")
    winlog.resizable(True, True)
    winlog.configure(bg='#010204')
    # Loads an Image
    #Logo = Image.open("B33Hive.png")
    #photo = ImageTk.PhotoImage(Logo)
    # This sets our icon
    #winlog.wm_iconphoto(False, photo)
    # Labels
    Label(winlog, bg='black', fg='white', text='What Container Do You Want the Logs From?').grid(row=7, column=8)
    entryLog = Entry(winlog, width=6, bg="gray25", fg='#ca891d')
    entryLog.grid(row=12, column=8)
    Label(winlog, bg='black', fg='white', text='Container:').grid(row=12, column=7)
    # Buttons
    Button(winlog, bg='#ca891d', activebackground='gray25', text='Enter', command=logMenuGrab).grid(row=13, column=9, pady=0)
    Button(winlog, bg='#ca891d', activebackground='gray25', text='Exit', command=logquit).grid(row=13, column=7, pady=0)
    winlog.mainloop()




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
win.bind('<Return>', lambda e, w=win: menu1Grab())
Button(win, bg='#ca891d', activebackground='gray25', text='Connect', command=menu1Grab).grid(row=13, column=9, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Exit', command=win.quit).grid(row=13, column=7, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Debug Main', command=debugMain).grid(row=1, column=9, pady=0)
# added 'Debug Main' to load main menu without having to connect to the server, remove before hand in

mainloop()  # End of First Tkinter Window


# ------------------------------------------------------ NETWORK -------------------------------------------------------
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

pinexchange()

# -------------------------------------------------------- PIN ---------------------------------------------------------
totalAttempts = 3
while True:
    if SERVER_PIN == '8888': ##8888 is the default pin, if the server doesn't have a pin, it will be automatically set to 8888, so we're checking if we can skip
        print("Server Has No Pin, Continuing...")
        mainMenu()
    if SERVER_PIN != '8888':
        if SERVER_PIN != CLIENT_PIN and Attempts < 2:
            Attempts = Attempts + 1
            print(SERVER_PIN, CLIENT_PIN)
            print("Incorrect PIN", totalAttempts-Attempts, "remaining...")
            pinMenu()
        elif SERVER_PIN == CLIENT_PIN:
            print("Correct PIN")
            print("Connected.")
            mainMenu()
        else:
            print("Pin Attempts Exceed, Disconnecting")
            disconnect()


s.close()