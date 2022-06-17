import socket
import threading

# connection details
import time

host = "192.168.1.23"
port = 9999

# choosing nickname
username = input("Enter your username: ")

# connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# receiving messages and sending username to server
def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "USERNAME":
                client.send(username.encode("utf-8"))

            else:
                print(f"{message}")

        except:
            raise "An error occurred. Disconnected from server."


# sending messages to server
def send():
    while True:
        time.sleep(0.1)
        message = input(f">> ")
        message_sent = f"{username} > {message}"
        client.send(message_sent.encode("utf-8"))


# starting threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
