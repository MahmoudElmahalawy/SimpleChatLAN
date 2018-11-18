from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle

def accept_clients():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Connecting to server...", "utf8"))
        addresses[client] = client_address
        Thread(target=check_authentication, args=(client,)).start()

def check_authentication(client):
    username, password = pickle.loads(client.recv(BUFSIZ))
    print(username, password)
    if username in users and users[username] == password:
        client.send(bytes("\nLogged in successfully", "utf8"))
        handle_client(client, username)
    else:
        # client.send(bytes("\nUsername or Password is incorrect, Please try again\n", "utf8"))
        client.send(bytes("{quit}", "utf8"))

def handle_client(client, username):  # Takes client socket as argument.
    """Handles a single client connection."""

    # name = client.recv(BUFSIZ).decode("utf8")
    welcome = '\n\nWelcome %s!\nEnter a message or type {quit} to exit.' %username
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" %username
    broadcast(bytes(msg, "utf8"))
    clients[client] = username

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            print(msg)
            broadcast(msg, username+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            print("%s logged out" %username)
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." %username, "utf8"))
            break



def broadcast(msg, sender=""):  # sender is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(sender, "utf8")+msg)


users = {'amr':'23', 'ahmed' : '24', 'moh' : '25'}
clients = {}
addresses = {}

HOST = ''
PORT = 33445
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5) #Listens for a maximum of 5 clients
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_clients)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
