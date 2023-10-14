import random
import string
import sys

import docker.api

# to do
# pull and configure images
# pull and configure dependencies
# automate creating dockertrap image
# create new containers
# remove containers
# Starting containers
# Stopping Containers
# Get Container Logs
# Get Container Uptime (?)
# Get Container Resource Usage (If possible, this would just be cool)
# Container config maybe?


client = docker.from_env()

try:
    open("flag", "w")
    client.images.pull('dariusbakunas/kippo')  # medium interaction SSH honeypot
    client.images.pull('mysql')  # dependency for kippo - data storage
    client.images.pull('dariusbakunas/kippo-graph')  # dependency for kippo - analysing kippo data
    client.images.pull('dtagdevsec/glutton')  # Generic Low Interaction Honeypot
    client.images.pull('dtagdevsec/snare')  # web application honeypot
    client.images.pull('dtagdevsec/tanner')  # remote data analysis and classification service for snare
    print("the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")

    # dockertrap image made separately - https://github.com/mrhavens/DockerTrap/tree/master

except:
    print("\nimages already pulled, proceeding\n")
    print("the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def menu():
    print(
        "\n1) create container \n2) destroy container \n3) start container \n4) stop container\n5) fetch logs\n6) fetch uptime\n6) fetch resource usage\n7) edit config\n8) exit")
    try:
        choice = int(input("enter a number: "))
    except:
        input("\ninvalid selection, press enter to continue...\n")

    if (choice == 1):
        create()
    elif (choice == 2):
        destroy()
    elif (choice == 3):
        start()
    elif (choice == 4):
        stop()
    elif (choice == 5):
        logs()
    elif (choice == 6):
        uptime()
    elif (choice == 7):
        resource()
    elif (choice == 8):
        config()
    elif (choice == 9):
        sys.exit()
    elif (choice == 69):
        exec(open("bee.py").read())
    else:
        print("\ninvalid choice\n")
        menu()


def create(Container):
    kipponame = "kippo-" + randomword(8)

    print( #done            #done               #done
        "\n1) create kippo \n2) create mySQL  \n3) create kippo-graphs \n4) create glutton \n)5 create snare \n6) create tanner \n7) create dockertrap \n8) exit ")
    print("the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
    try:
        choice = int(input("enter a number: "))
    except:
        input("\ninvalid selection, press enter to continue...\n")

    if (choice == 1):
        print(
            "\nthis honeypot requires 2 dependencies, mySQL for logging and the kippo-graphs container for analysing.")

        try:
            createsql = input("create mySQL now?: (yes/no)")
        except:
            input("\ninvalid input, press enter to continue...")

        if (createsql == "yes"):
            print(
                "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
            sqlname = "sql-" + kipponame
            client.containers.create(name=sqlname, environment=["MYSQL_ROOT_PASSWORD=K[5UZ4ELSf;e)gX="])

        try:
            creategraph = input("create kippo-graphs now? mySQL will need to be started in order to do so: (yes/no)")
        except:
            input("\ninvalid input, press enter to continue...")

        if (creategraph == "yes"):
            print(
                "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
            client.containers.start(name=sqlname, detach=False, tty=False)
            client.containers.create(name="kippo-graphs" + kipponame, links={sqlname: 'mysql'},
                                     image="dariusbakunas/kippo-graph")
            Container.stop(name=sqlname)

        elif (creategraph == "no"):
            print("\nskipping kippo-graphs...\n")
        else:
            print("invalid input, please try again")

        print("\nkippo and chosen dependencies finished, returning to menu")
        input("\npress enter to continue...")
        create()

    elif (choice == 2):
        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        sqlname = "sql-" + randomword(8)
        client.containers.create(image="mysql:latest", name=sqlname,
                                 environment=["MYSQL_ROOT_PASSWORD=K[5UZ4ELSf;e)gX="])
    elif (choice == 3):
        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        try:
            print("\nkippo requires a mysql datasource in order to function\n")
            sqllink = input("input the name of the container to link: ")
        except:
            input("\ninvalid input, press enter to continue...")

        client.containers.create(name="kippo-graphs" + randomword(8), links={sqllink},
                                 image="dariusbakunas/kippo-graph")
    elif (choice == 4):
        #this one has to be build using a dockerfile. must find a way to create the file in the right place
        lineone=("FROM debian:latest")
        linetwo=('LABEL authors="Toby, Ethan, Cal, Kris"')
        linethree=("")
        linefour=('ENTRYPOINT ["top", "-b"]')
        linefive=('RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo')
        linesix=("USER docker")
        lineseven=("CMD /bin/bash")
        lineeight=("RUN sudo apt-get upgrade -y")
        linenine=("RUN sudo apt-get install gcc libpcap-dev iptables -y")
        lineten=("RUN sed -i 's/[# ]*Port .*/Port 5001/g' /etc/ssh/sshd_config")
        lineelleven=("RUN exit")

        glutton = open("./glutton/dockerfile", "w")
        glutton.writelines([lineone, linetwo, linethree, linefour, linefive, linesix, lineseven, lineeight, linenine,
                            lineten, lineelleven])
        glutton.close()

        client.containers.build(path="./glutton/dockerfile")
        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")

    elif (choice == 5):
        client.containers.create()
    elif (choice == 6):
        client.containers.create()
    elif (choice == 7):
        client.containers.create()
    elif (choice == 8):
        menu()
    # client.containers.create()


def destroy():
    menu()


def start(container):
    print()
    client.containers.list(all=True)
    print()
    startname = ''

    try:
        startname = input("input the name of the container to start")
    except:
        print("invalid selection")

    client.containers.run(name=startname)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()


def stop(container):
    print()
    client.containers.list()
    print()
    stopname = ''

    try:
        stopname = input("input the name of the container to stop")
    except:
        print("invalid selection")

    client.containers.run(name=stopname)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()


def logs():
    menu()


def uptime():
    menu()


def resource():
    menu()


def config():
    menu()
