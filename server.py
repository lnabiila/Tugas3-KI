import socket
import time
import threading

def handle_client(client_socket, address, client_id, clients):
    print(f"Client ID {client_id} connected from {address}")
    client_socket.send(str({
        'data': f"{client_id} is your ID",
        'client_id': client_id
    }).encode('utf-8'))

    time.sleep(0.5)

    public_key = eval(client_socket.recv(
        1024).decode('utf-8'))['public_key']

    for _, client_item_socket in clients.items():
        if client_item_socket != client_socket:
            client_item_socket.send(str({
                'client_id': client_id,
                'public_key': public_key,
                'data': f"New client has joined with ID {client_id}. It's public key has been received." 
            }).encode('utf-8'))

    time.sleep(0.5)

    client_socket.send(str({
        'public_keys': public_keys
    }).encode('utf-8'))

    public_keys[client_id] = public_key

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            data = eval(data)

            print(f"From client {client_id} with {address}: {data}")

            try:
                if data['data'] == 'L':
                    send_client_list(client_id)
                else:
                    target_ids = [int(data['target_id'])]

                    forward_message(client_id, target_ids, data['data'], data['step'], data['length'])
            except ValueError as e:
                print(f"From client {client_id} (invalid format): {e}")

    except Exception as e:
        print(f"From client {client_id} (error handling): {e}")

    finally:
        del clients[client_id]

        print(f"Client ID {client_id} from {address} closed the connection")
        client_socket.close()

def forward_message(sender_id, target_ids, message, step, length):
    for target_id in target_ids:
        try:
            target_socket = clients.get(target_id)
            if target_socket and target_id != sender_id:
                target_socket.send(str({
                    'step': step,
                    'sender_id': sender_id,
                    'data': message,
                    'length': length
                }).encode('utf-8'))
        except Exception as e:
            print(f"Forwarding message to client {target_id} failed: {e}")

def send_client_list(client_id):
    client_socket = clients[client_id]
    connected_clients = ", ".join(map(str, clients.keys()))
    client_socket.send(str({
        'data': f"\nID client(s) that has been connected: {connected_clients}"
    }).encode('utf-8'))

if __name__ == "__main__":
    clients = {}
    public_keys = {}
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8888))
    server.listen(5)

    print("Server is up and running, listening on port 8888...")

    try:
        while True:
            client_socket, addr = server.accept()
            client_id = len(clients) + 1
            clients[client_id] = client_socket
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket, addr, client_id, clients))
            client_handler.start()

    except KeyboardInterrupt:
        print("The server is stopping.")

    finally:
        for client_socket in clients.values():
            client_socket.close()