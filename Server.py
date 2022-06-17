import socket
import threading

# connection data
host = "192.168.1.23"
port = 9999

# starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# lists for clients and usernames
clients = []
usernames = []


# sending message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# handling messages from clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            
        except:
            # removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the chat".encode("utf-8"))
            usernames.remove(username)
            break


# receiving messages from clients
def receive():
    while True:
        # accepting connection
        client, address = server.accept()
        print(f"Connected to {address}")

        # requesting and storing username
        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        usernames.append(username)
        clients.append(client)

        # print and broadcast nickname
        print(f"Username: {username}")
        broadcast(f"{username} joined the chat".encode("utf-8"))

        # start thread for handling messages
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
