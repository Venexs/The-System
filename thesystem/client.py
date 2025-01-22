import socket
import threading

SERVER = "192.168.1.177"
PORT = 5555
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 64  # Keep header size consistent between client and server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = str(len(message)).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length)) # Pad to ensure consistent header length
    client.send(msg_length)
    client.send(message)

def receive():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)  # Print received messages to the console
                if msg == "SERVER FULL":
                    print("Server is full. Exiting.")
                    client.close()
                    break # Exit the receive loop

        except ConnectionResetError: # Handle server closing connection
            print("Server closed the connection.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break # exit if other errors occur


receive_thread = threading.Thread(target=receive)
receive_thread.start()

while True:
    message = input()
    if message == "!DISCONNECT":
        send(message)
        break  # Exit the client loop gracefully
    elif message.startswith("ATTACK"):
        send(message)
    else:
        send(message)
