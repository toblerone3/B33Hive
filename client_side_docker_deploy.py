import random
import string
import subprocess
import sys
from pathlib import Path
import docker

client = docker.from_env()


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def menu():
    print(
        "\n1) create container \n2) destroy container \n3) start container \n4) stop container\n5) fetch logs"
        "\n6) fetch resource usage\n8) exit")
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
        resource()
    elif (choice == 7):
        sys.exit()
    elif (choice == 69):
        exec(open("bee.py").read())
    else:
        print("\ninvalid choice\n")
        menu()


def create(Container):
    kipponame = "kippo-" + randomword(8)

    print(
        "\n1) create kippo \n2) create mySQL  \n3) create kippo-graphs \n4) create glutton \n)5 create snare \n"
        "6) create tanner \n7) create Honey_ports \n8) exit ")

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

        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        # client.containers.build(path="./glutton/dockerfile")
        gluttonname = "glutton-" + randomword(8)
        client.containers.create(image="glutton", name=gluttonname)

    elif (choice == 5):
        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        # client.containers.build(path="./snare/dockerfile")
        snarename = "snare-" + randomword(8)
        client.containers.create(image="snare", name=snarename)
    elif (choice == 6):
        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        # client.containers.build(path="./tanner/dockerfile")
        tannername = "tanner-" + randomword(8)
        client.containers.create(image="tanner", name=tannername)
    elif (choice == 7):
        answer = ""
        print(
            "the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
        # client.containers.build(path="./honey_ports/dockerfile")
        honeyportsname = "honeyports-" + randomword(8)
        client.containers.create(image="honey_ports", name=honeyportsname)
        print("this container requires a separate bash script in order to function.")
        try:
            answer = str(input("\nrun this now? [Y/N] : "))
        except:
            print("\ninvalid input...")

        if (answer == "Y" or "y"):
            print(subprocess.run(["docker_testing/honey_ports/honey_ports.sh"]))

        elif (answer == "N" or "n"):
            print("No longer running script, returning to menu")
            create()

        else:
            print("invalid input...")

    elif (choice == 8):
        menu()


def destroy(container):
    print()
    client.containers.list()
    print()
    destroyname = ''

    try:
        destroyname = input("input the name of the container to stop")
    except:
        print("invalid selection")

    container.image(name=destroyname)
    client.containers.stop(name=destroyname)

    print()
    input("\nfinished, press enter...\n")
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

    client.containers.stop(name=stopname)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()


def logs(container):
    print()
    client.containers.list()
    print()
    logname = ''

    try:
        logname = input("input the name of the container to retrieve logs from")
    except:
        print("invalid selection")

    client.containers.logs(logname, stdout=True, stderr=True, stream=True, timestamps=False, tail='all', since=None,
                           follow=None,
                           until=None)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()


def resource(container):
    print()
    client.containers.list()
    print()
    resourcename = ''

    try:
        resourcename = input("input the name of the container to retrieve resource usage from")
    except:
        print("invalid selection")

    client.containers.top(name=resourcename)
    print()
    print("container status: " + container.name.status)
    input("\nfinished, press enter...\n")
    menu()


imageflag = Path("./flag")
if imageflag.is_file():
    print("\nimages already pulled, proceeding\n")
    print("the default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")
    menu()

else:
    print("pulling images\n")
    #open("flag", "w")
    client.images.pull('dariusbakunas/kippo')  # medium interaction SSH honeypot
    print("kippo pulled...")
    client.images.pull('mysql')  # dependency for kippo - data storage
    print("mySQL pulled...")
    client.images.pull('dariusbakunas/kippo-graph')  # dependency for kippo - analysing kippo data
    print("kippo-graph pulled...")
    # client.images.pull('dtagdevsec/glutton')  # Generic Low Interaction Honeypot - potentially worth building ourselves
    # print("glutton pulled...")
    # client.images.pull('dtagdevsec/snare')  # web application honeypot
    # print("snare pulled...")
    # client.images.pull('dtagdevsec/tanner')  # remote data analysis and classification service for snare

    client.images.build(fileobj="./docker_testing/glutton/Dockerfile", custom_context=True, pull=True)
    #print("\nglutton built...")
    #client.images.build(path="./docker_testing/honey_ports/Dockerfile", pull=True)
    #print("\nHoney_ports built...")
    #client.images.build(path="./docker_testing/snare/Dockerfile", pull=True)
    #print("\nsnare built...")
    #client.images.build(path="./docker_testing/tanner/Dockerfile", pull=True)
    #print("\ntanner built")
    print("\nthe default password for created containers which aren't honeypots is K[5UZ4ELSf;e)gX= - change this ASAP")

    # dockertrap image made separately - https://github.com/mrhavens/DockerTrap/tree/master

    menu()
