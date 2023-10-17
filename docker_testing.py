import sys

import docker

client = docker.from_env() # detects the docker installation and assigns this to a variable


def menu():
    print(
        "1) Download test image \n2) start container\n3) stop container\n4) view running containers\n5) remove test container\n6) exit")
    choice = int(input("enter a number: "))
    # if (choice):
    # print("\ninvalid choice\n")
    # menu()

    if (choice == 1):
        download()
    elif (choice == 2):
        start()
    elif (choice == 3):
        stop()
    elif (choice == 4):
        view()
    elif (choice == 5):
        remove()
    elif (choice == 6):
        sys.exit()
    else:
        print("\ninvalid choice\n")
        menu()


def download():
    client.images.pull(
        'debian:latest')  # Pull an image of the given name and return it. Similar to the docker pull command. If tag is None or empty, it is set to latest. If all_tags is set, the tag parameter is ignored and all image tags will be pulled.
    print("latest debian container has been pulled, check for duplicates")
    input("\nPress Enter to continue...")
    menu()


def start():
    test_container = client.containers.run('debian', 'tail -f /dev/null',
                                           detach=True)  # args separated by commas, i.e. domainname=alpine, auto_remove=true. args available here: https://docker-py.readthedocs.io/en/stable/index.html
    test_container.logs()  # shows logs from running container. If the detach argument is True, it will start the container and immediately return a Container object, similar to "docker run -d".
    input("\nPress Enter to continue...")
    menu()


def stop():
    client.containers.stop(name='debian')
    input("\nPress Enter to continue...")
    menu()


def view():
    print(client.containers.list(
        all=True))  # List containers. Similar to the docker ps command. all (bool) – Show all containers. Only running containers are shown by default
    input("\nPress Enter to continue...")
    menu()


def remove():
    client.containers.stop(name='debian', force=True)  # Remove this container. Similar to the docker rm command. forces the deletion
    input("\nPress Enter to continue...")
    menu()


menu()
