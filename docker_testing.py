#this is a file in order to demonstrate basic control over docker desktop, all on the same machine.
#in this file, I should demo:
#downloading docker container images
#starting containers - not done
#stoping containers - not done
#viewing running containers - not done
#deleteing containers - not done


import sys, docker
client = docker.from_env()

def menu():
    print("1) Download test image \n2) start container\n3) stop container\n4) view running containers\n5) remove test container\n6) exit")
    choice = int(input("enter a number: "))
    #if (choice):
        #print("\ninvalid choice\n")
        #menu()

    if(choice == 1):
        download()
    elif(choice == 2):
        start()
    elif(choice == 3):
        stop()
    elif (choice == 4):
        view()
    elif (choice == 5):
        remove()
    elif(choice == 6):
        sys.exit()
    else:
        print("\ninvalid choice\n")
        menu()

def download():
    client.images.pull('debian:latest')
    print("latest debian container has been pulled")
    input("\nPress Enter to continue...")
    menu()
def start():
    global test_container
    test_container = client.containers.run('debian', 'tail -f /dev/null', detach=True)  # args separated by commas, i.e. domainname=alpine, auto_remove=true. args available here: https://docker-py.readthedocs.io/en/stable/index.html
    test_container.logs()  # shows logs from running container. If the detach argument is True, it will start the container and immediately return a Container object, similar to "docker run -d".
    input("\nPress Enter to continue...")
    menu()
def stop():
    test_container.stop()
    input("\nPress Enter to continue...")
    menu()
def view():
    print(client.containers.list(all=True))
    input("\nPress Enter to continue...")
    menu()
def remove():
    test_container.remove()
    print("\ncontainer removed\n")
    menu()

menu()