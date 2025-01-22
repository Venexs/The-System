import socket
import threading

SERVER = "192.168.1.177"
PORT = 5555
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
MAX_PLAYERS = 2  # Maximum number of players for the PVP match

connections = []  # List to hold client connections
player_data = {}  # Dictionary to store player data (e.g., health, position)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connections.append(conn)
    player_data[addr] = "Files/Status.json"  # Initialize player health

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == "!DISCONNECT":
                    connected = False
                elif msg.startswith("ATTACK"):  # Handle attack messages
                    target_addr = eval(msg.split(":")[1])  # Get target address
                    damage = int(msg.split(":")[2])  # Get damage value
                    if target_addr in player_data:
                        player_data[target_addr]['health'] -= damage
                        send_to_all(f"UPDATE:{addr}:{player_data[addr]['health']}") # Update attacker health (could be counter-attack)
                        send_to_all(f"UPDATE:{target_addr}:{player_data[target_addr]['health']}") # Update target health
                        if player_data[target_addr]['health'] <= 0:
                            send_to_all(f"{target_addr} DEFEATED!")


                else:
                    print(f"[{addr}] {msg}")
                    # Handle other game logic here

        except ConnectionResetError:
            print(f"[DISCONNECT] {addr} forcibly closed the connection.")
            connected = False # Make sure to break the loop

    connections.remove(conn)
    del player_data[addr]
    conn.close()
    print(f"[DISCONNECT] {addr} disconnected.  Active connections: {len(connections)}")

def send_to_all(msg):
    message = msg.encode(FORMAT)
    msg_length = str(len(message)).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    for conn in connections:
        try: # Handle potential errors during sending
            conn.send(msg_length)
            conn.send(message)
        except Exception as e:
            print(f"Error sending message to a client: {e}")
            # Handle the disconnection here, similar to how it's done in handle_client
            connections.remove(conn) # Or handle disconnection in separate function


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        if len(connections) < MAX_PLAYERS:  # Limit the number of players
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # subtract main thread
        else: # Server full message
            full_msg = "SERVER FULL".encode(FORMAT)
            full_msg_length = str(len(full_msg)).encode(FORMAT)
            full_msg_length += b' ' * (HEADER - len(full_msg_length))
            conn.send(full_msg_length)
            conn.send(full_msg)
            conn.close()


print("[STARTING] server is starting...")
HEADER = 64
start()