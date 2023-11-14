import os
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
from tkinter import simpledialog
import rsa
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
from tkterminal import Terminal
import pickle

key = Fernet.generate_key()
Fern = Fernet(key)

if os.path.exists('contemp.txt'):
    os.remove('contemp.txt')

whichOS = platform.system()
print("Launching", whichOS, "B33Hive Client")  ##Just a debug, we need this logic later

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


def pinexchange():  ## Further Example
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
    if os.path.exists('contemp.txt'):
        os.remove('contemp.txt')
    print("Disconnecting...")
    signal_Send = "Disconnect"
    sigSent = signal_Send.encode()
    try:
        s.send(sigSent)
        s.close()
        quit()
    except Exception as e:
        quit()



def localhost():
    global serverIP
    global rawPort
    win.destroy()
    serverIP = '127.0.0.1'
    rawPort = '5003'


def debugMain():  # This is how we skip to the main menu for debug, does not connect to the server
    win.destroy()
    mainMenu()


# --------------------------------------------------- LOG RETRIEVAL ----------------------------------------------------

def logcontainers():  ## THIS IS HOW WE SEND TO THE SERVER, THIS CAN BE REPEATED AD-NAUSEAM
    runningContainers()
    signal_Send = "Get Container Logs"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    logMenu()


def logMenuGrab():
    global loggrab
    messagebox.showinfo("Warning", "The Client will hang for five seconds while retrieving logs ")
    loggrab = entryLog.get()
    print(loggrab)
    winlog.destroy()
    signal_Send = loggrab
    sigSent = signal_Send.encode()
    s.send(sigSent)
    with open('raw.txt', 'w') as f:
        while True:
            logsreturned = s.recv(512).decode()
            print(logsreturned)
            if 'EOT' in logsreturned:
                break
            f.write(logsreturned)
    with open('raw.txt', 'r') as logfile:
        rawlogs = logfile.read()
    if rawlogs == 'Not Valid':
        messagebox.showinfo("Invalid ID", "Invalid Container ID, Please ensure you're using the"
                                          " Containers Shorthand ID")
    else:
        declogs = Fern.decrypt(rawlogs)
        strlogs = str(declogs)
        logwrap = '\n'.join(re.findall('.{1,128}', strlogs))
        f = open("%sContainerLogs.txt" % loggrab, "w")
        fnameloc = str("%sContainerLogs.txt" % loggrab)
        f.write(logwrap)
        print(declogs[4:])  # DEBUG ONLY
        messagebox.showinfo("Success", "Wrote Container Logs to %sContainerLogs.txt" % loggrab)
    if os.path.exists('raw.txt'):
        os.remove('raw.txt')
    if whichOS == 'Windows':
        mainterminal.run_command('type %s' % fnameloc)
    if whichOS == 'Linux':
        mainterminal.run_command('cat %s' % fnameloc)


def logquit():
    signal_Send = "Cancel"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    winlog.destroy()


# ------------------------------------------------------- DOCKER -------------------------------------------------------


def pullImages():
    hangwarning = messagebox.askyesnocancel("Confirmation", "This Menu will freeze while the server pulls"
                                                            " the images, are you sure you want to pull the images now?")
    print(hangwarning)
    if hangwarning is True:
        signal_Send = "pullImages"  # We store what we want to send to the server here
        sigSent = signal_Send.encode()  # Then we encode it into bytes
        s.send(sigSent)  # then we send it using s.send
        while True:  # we then start a listener
            pulledimages = s.recv(2048)  # and wait for a message from the server
            printimages = pulledimages.decode()  # we then turn it back into a string
            print(printimages)  # and print it
            if pulledimages != '':  # this just checks to see if we got anything, once the server responds the loop breaks
                break
        messagebox.showinfo("Pulled Images", "Images were successfully pulled / updated")


def remEntry():
    global remWin
    global containerrem
    containerrem = simpledialog.askstring("Destroy Container", "Enter a Container ID to destroy it")
    print(containerrem)
    destroycontainer()


def start():
    containerStart = simpledialog.askstring("Start Container", "Enter a Container ID to start it")
    signal_Send = "start"
    startContainer_send = containerStart.encode()
    sigSent = signal_Send.encode()
    s.send(sigSent)
    time.sleep(1)
    s.send(startContainer_send)
    response = s.recv(1024).decode()
    if response == 'Invalid Start Name':
        messagebox.showinfo("Invalid ID", "Invalid Container ID, Please ensure you're using the"
                                          " Containers Shorthand ID")
    else:
        # This is hacky, but it works
        response = response.replace(",", "")
        response = response.replace("'", "")
        response = response.replace(")", "")
        response = response.replace("(", "")
        print(response)
        messagebox.showinfo("Success", response)


def groupstart():
    containerStart = simpledialog.askstring("Start Container Group", "Enter a Container group number to start it")
    signal_Send = "groupstart"
    startContainer_send = containerStart.encode()
    sigSent = signal_Send.encode()
    s.send(sigSent)
    time.sleep(1)
    s.send(startContainer_send)
    response = s.recv(1024).decode()
    if response == 'Invalid Start Name':
        messagebox.showinfo("Invalid ID", "Invalid Container group, Please ensure you're using the"
                                          " Container group number (1,2,3...)")
    else:
        # This is hacky, but it works
        response = response.replace(",", "")
        response = response.replace("'", "")
        response = response.replace(")", "")
        response = response.replace("(", "")
        print(response)
        messagebox.showinfo("Success", response)


def stop():  ## Further Example
    containerStop = simpledialog.askstring("Stop Container", "Enter a Container ID to stop it")
    signal_Send = "stop"
    stopContainer_send = containerStop.encode()
    sigSent = signal_Send.encode()
    s.send(sigSent)
    time.sleep(1)
    s.send(stopContainer_send)
    response = s.recv(1024).decode()
    if response == 'Invalid Start Name':
        messagebox.showinfo("Invalid ID", "Invalid Container ID, Please ensure you're using the"
                                          " Containers Shorthand ID")
    else:
        # This is hacky, but it works
        response = response.replace(",", "")
        response = response.replace("'", "")
        response = response.replace(")", "")
        response = response.replace("(", "")
        print(response)
        messagebox.showinfo("Success", response)


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
    print(containerrem)
    signal_Send = "destroy containers"
    remContainer_send = containerrem.encode()
    sigSent = signal_Send.encode()
    s.send(sigSent)
    time.sleep(1)
    s.send(remContainer_send)
    deleteoutput = s.recv(2048)  # and wait for a message from the server
    deleteoutput = deleteoutput.decode()  # we then turn it back into a string
    print(deleteoutput)  # and print it
    if deleteoutput == 'Invalid Container ID':
        messagebox.showinfo("Invalid ID", "Invalid Container ID, Please ensure you're using the"
                                          " Containers Shorthand ID")
    else:
        deleteoutput = deleteoutput.replace(",", "")
        deleteoutput = deleteoutput.replace("'", "")
        deleteoutput = deleteoutput.replace(")", "")
        deleteoutput = deleteoutput.replace("(", "")
        print(deleteoutput)
        messagebox.showinfo("Success", deleteoutput)


def runningContainers():  ## Further Example
    signal_Send = "Show Running Containers"
    sigSent = signal_Send.encode()
    s.send(sigSent)
    with open('contemp.txt', 'w') as f:
        while True:
            currentcontainers = s.recv(2048)
            deenc_containers = Fern.decrypt(currentcontainers)
            printcontainers = pickle.loads(deenc_containers)
            msgbox_print = ""
            for container in printcontainers:
                msgbox_print += str(container) + "\n"
            print(msgbox_print)
            f.write(msgbox_print)
            messagebox.showinfo("Current containers:", msgbox_print)
            if whichOS == 'Windows':
                mainterminal.run_command('type contemp.txt')
            if whichOS == 'Linux':
                mainterminal.run_command('cat contemp.txt')
            if currentcontainers != '':
                break


def getresources():
    containerask = simpledialog.askstring("Get Container Stats", "What Container do you want the Stats from? "
                                                                 "(shorthand ID)")
    print(containerask)
    if len(containerask) == 12:
        signal_Send = "Get Resources"
        sigSent = signal_Send.encode()
        s.send(sigSent)
        print(containerask)  # DEBUG
        time.sleep(0.25)
        sigSent = containerask.encode()
        s.send(sigSent)
        resourceusage = s.recv(2048)
        resourceusage = resourceusage.decode()
        if resourceusage == 'Invalid ID':
            messagebox.showinfo("Invalid ID", "Invalid Container ID, Please ensure you're using the"                                          " Containers Shorthand ID")
            mainterminal.run_command("echo Invalid ID")
            print("Invalid ID")
        else:
            resourceusage = str(resourceusage)
            resourceusage = resourceusage.replace(",", "")
            resourceusage = resourceusage.replace("'", "")
            resourceusage = resourceusage.replace("\\n","")
            print(resourceusage)
            messagebox.showinfo("Success", resourceusage)
            mainterminal.run_command("echo %s" % resourceusage)
    elif containerask is None:
        mainterminal.run_command("echo Cancelling")
        print("Cancelling")
    else:
        messagebox.showinfo("Invalid ID","Invalid Container ID, Please ensure you're using the"                                          " Containers Shorthand ID")
        mainterminal.run_command("echo Invalid ID")
        print("Invalid ID")


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
    # pinexchange()


def entryboxGrab():
    secretINPUT = entryBox.get()
    if secretINPUT == 'physics'.lower():
        print('check 1')
        messagebox.showinfo("What do bees chew?", "Bumble gum!"
                                                  "\n(check the terminal)")
        subprocess.run(["python", "bee.py"])


# ------------------------------------------------------- MENU'S -------------------------------------------------------
def on_closing():
    print("Shutting down B33Hive client...")
    disconnect()


def mainMenu():  # This is our main menu, functionalized, so we can debug and call later
    global entryBox
    global mainterminal
    win2 = Tk()
    win2.title("B33Hive: Main Menu")
    # win.geometry("640x480")
    win2.resizable(False, False)
    win2.configure(bg='#010204')
    # Loads an Image
    Logo = Image.open("B33Hive.png")
    photo = ImageTk.PhotoImage(Logo)
    # Puts image into a label
    imageLogo = tkinter.Label(image=photo, highlightthickness=0, background='#010204')
    imageLogo.image = photo
    win2.wm_iconphoto(False, photo)  # sets icon

    imageLogo.grid(row=3, column=2, pady=0)

    # Lists all our buttons DO NOT USE ROW 5 as this will break the logo formatting
    # Left Row

    Button(win2, bg='#ca891d', activebackground='gray25', text='See Current Containers', command=runningContainers).grid(row=1, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Start Container', command=start).grid(row=2, column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Create Containers', command=createcontainer).grid(row=3, column=1, pady=0)

    Button(win2, bg='#ca891d', activebackground='gray25', text='Get Container Logs', command=logcontainers).grid(row=4,column=1, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Start Container Group', command=groupstart).grid(row=5, column=1, pady=0)

    # Middle Row
    Button(win2, bg='#ca891d', activebackground='gray25', text='Pull / Update Images', command=pullImages).grid(row=5, column=2, pady=0)


    # Right Row
    Button(win2, bg='#ca891d', activebackground='gray25', text='Get Container Stats', command=getresources).grid(row=1, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Stop Container', command=stop).grid(row=2, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Destroy Containers', command=remEntry).grid(row=3, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Start Remote Shell', command=reverseshell).grid(row=4, column=3, pady=0)
    Button(win2, bg='#ca891d', activebackground='gray25', text='Disconnect', command=disconnect).grid(row=5, column=3,pady=0)  ##Both Buttons currently call disconnect due to the fact we can't recall our login screen

    # This is just an example for how to make a tooltip, the below code is now redundant and
    # should only be used for as a reference
    # This allows us to reference a button later
    # exitButton = Button(win2, bg='#ca891d', activebackground='gray25', text='Exit', command=quit)
    # Here we're referencing the exit button we saved as a variable
    # exitbuttontip = Hovertip(exitButton, "DO NOT USE IF YOU'RE CONNECTED TO THE SERVER")
    # Here we tell tkinter to put exitbutton into the grid
    # exitButton.grid(row=10, column=1, pady=0)

    #entryBox = Entry(win2, width=32, bg="gray25", fg='#ca891d')
    #entryBox.grid(row=9, column=2)
    win2.bind('<Return>', lambda e, w=win2: entryboxGrab())

    win2.protocol("WM_DELETE_WINDOW", on_closing)

    # Terminal
    mainterminal = Terminal(win2, background='#010204', foreground='#ca891d', highlightcolor='#ca891d',
                            highlightbackground='#ca891d', insertbackground='#ca891d', selectbackground='#ca891d',
                            pady=0, padx=0, width=80, height=12)
    mainterminal.basename = "B33Hive:"
    mainterminal.shell = True
    mainterminal.linebar = True
    mainterminal.grid(row=12, column=2, pady=0)

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
    Button(winpin, bg='#ca891d', activebackground='gray25', text='Enter', command=menu2Grab).grid(row=13, column=9,
                                                                                                  pady=0)
    Button(winpin, bg='#ca891d', activebackground='gray25', text='Exit', command=quit).grid(row=13, column=7, pady=0)
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
    # Logo = Image.open("B33Hive.png")
    # photo = ImageTk.PhotoImage(Logo)
    # This sets our icon
    # winlog.wm_iconphoto(False, photo)
    # Labels
    Label(winlog, bg='black', fg='white', text='What Container Do You Want the Logs From?').grid(row=7, column=8)
    entryLog = Entry(winlog, width=6, bg="gray25", fg='#ca891d')
    entryLog.grid(row=12, column=8)
    Label(winlog, bg='black', fg='white', text='Container:').grid(row=12, column=7)
    # Buttons
    Button(winlog, bg='#ca891d', activebackground='gray25', text='Enter', command=logMenuGrab).grid(row=13, column=9,
                                                                                                    pady=0)
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
Label(win, bg='black', fg='white', text='').grid(row=8,
                                                 column=8)  ##Blank Labels are Spacers because Tkinter.grid is bad
# These are descriptors for the entry boxes
Label(win, bg='black', fg='white', text='Server IP').grid(row=10, column=7)
Label(win, bg='black', fg='white', text='Port').grid(row=11, column=7)
####Label(win, bg='black', fg='white', text='PIN (Optional)').grid(row=12, column=7) ####REDUNDANT####


# These are our entry boxes
servIP = Entry(win, width=16, bg="gray25", fg='#ca891d')
port = Entry(win, width=6, bg="gray25", fg='#ca891d')
# entryPIN = Entry(win, width=6, bg="gray25", fg='#ca891d') ####REDUNDANT####

servIP.grid(row=10, column=8)
port.grid(row=11, column=8)
# entryPIN.grid(row=12, column=8) ####REDUNDANT####
win.bind('<Return>', lambda e, w=win: menu1Grab())
Button(win, bg='#ca891d', activebackground='gray25', text='Connect', command=menu1Grab).grid(row=13, column=9, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Exit', command=win.quit).grid(row=13, column=7, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Debug Main', command=debugMain).grid(row=1, column=9, pady=0)
Button(win, bg='#ca891d', activebackground='gray25', text='Local Host', command=localhost).grid(row=1, column=7, pady=0)
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
    # 8888 is the default pin, if the server doesn't have a pin, it will be automatically set to 8888, so we're checking if we can skip
    if SERVER_PIN == '8888':
        print("Server Has No Pin, Continuing...")
        mainMenu()
    if SERVER_PIN != '8888':
        if SERVER_PIN != CLIENT_PIN and Attempts < 2:
            Attempts = Attempts + 1
            print(SERVER_PIN, CLIENT_PIN)
            print("Incorrect PIN", totalAttempts - Attempts, "remaining...")
            pinMenu()
        elif SERVER_PIN == CLIENT_PIN:
            print("Correct PIN")
            print("Connected.")
            mainMenu()
        else:
            print("Pin Attempts Exceed, Disconnecting")
            disconnect()

s.close()
