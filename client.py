import socket
import random
import secrets
import string
import time
import threading
global state
from des import encrypt, decrypt, generateKeys, stringBinary, binaryString
from rsa import encoder, decoder, setkeys

def randomString(length=8):
    characters = string.ascii_letters + string.digits
    randomString = ''.join(secrets.choice(characters) for _ in range(length))
    return randomString

def recvMessage(client_socket):
    global state, target_id, session_des_key, session_round_key
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            data = eval(data)
            if 'public_keys' in data:
                public_keys.update(data['public_keys'])
            elif 'public_key' in data:
                public_keys[data['client_id']] = data['public_key']
                print(f"\nReceived: {data['data']}")
            elif 'step' in data:
                if data['step'] == 1:
                    print("\nPress 'R' to reply.")
                    decrypted = eval(decoder(data['data'], private_key, n))
                    bring_back_to = data['sender_id']
                    recv_n1_from_step1 = decrypted['n1']
                    recv_n1 = recv_n1_from_step1
                    data_step2 = {
                        'n1': recv_n1_from_step1,
                        'n2': n2
                    }
                    selected_public_keys = public_keys[bring_back_to]
                    encrypted_step2 = encoder(
                        str(data_step2), selected_public_keys, n)
                    client_socket.send(str({
                        "step": 2,
                        "target_id": bring_back_to,
                        "data": encrypted_step2,
                        'length': -1
                    })
                        .encode('utf-8'))
                elif data['step'] == 2:
                    decrypted = eval(decoder(data['data'], private_key, n))
                    bring_back_to = int(data['sender_id'])
                    recv_n1_from_step2 = decrypted['n1']
                    recv_n2_from_step2 = decrypted['n2']
                    if n1 != recv_n1_from_step2:
                        raise ValueError("N1 didn't match!")
                    if n1 == recv_n1_from_step2:
                        print(f"N1 matches: {n1} == {recv_n1_from_step2}")
                    data_step3 = {
                        'n2': recv_n2_from_step2
                    }
                    selected_public_keys = public_keys[bring_back_to]
                    encrypted_step3 = encoder(
                        str(data_step3), selected_public_keys, n)
                    client_socket.send(str({
                        "step": 3,
                        "target_id": bring_back_to,
                        "data": encrypted_step3,
                        'length': -1
                    })
                        .encode('utf-8'))
                elif data['step'] == 3:
                    decrypted = eval(decoder(data['data'], private_key, n))
                    bring_back_to = int(data['sender_id'])
                    recv_n2_from_step3 = decrypted['n2']
                    if n2 != recv_n2_from_step3:
                        raise ValueError("N2 didn't match!")
                    if n2 == recv_n2_from_step3:
                        print(f"N2 matches: {n2} == {recv_n2_from_step3}")
                    state = 'chat'
                    data_step4 = {
                        'n1': recv_n1,
                        'k_s': generated_des_key
                    }
                    session_des_key = generated_des_key
                    bin_key = stringBinary(session_des_key)[0]
                    session_round_key = generateKeys(bin_key)
                    selected_public_keys = public_keys[bring_back_to]
                    encrypted_step4 = encoder(
                        str(data_step4), selected_public_keys, n)
                    client_socket.send(str({
                        "step": 4,
                        "target_id": bring_back_to,
                        "data": encrypted_step4,
                        'length': -1
                    })
                        .encode('utf-8'))
                elif data['step'] == 4:
                    target_id = int(data['sender_id'])
                    decrypted = eval(decoder(data['data'], private_key, n))
                    recv_n1_from_step4 = decrypted['n1']
                    if n1 != recv_n1_from_step4:
                        raise ValueError("N1 didn't match!")
                    if n1 == recv_n1_from_step4:
                        print(f"N1 matches: {n1} == {recv_n1_from_step4}")
                    session_des_key = decrypted['k_s']
                    bin_key = stringBinary(session_des_key)[0]
                    session_round_key = generateKeys(bin_key)
                    print("Successfully connected")
                elif data['step'] == 5:
                    target_id = int(data['sender_id'])
                    state = 'chat'
                    length = data['length']
                    encrypted_bin_message = data['data']
                    source = data['sender_id']
                    decrypted_bin_message = ''
                    for i in range(0, len(encrypted_bin_message), 64):
                        chunk = encrypted_bin_message[i:i+64]
                        decrypted_chunk = decrypt(chunk, session_round_key)
                        decrypted_bin_message += decrypted_chunk
                    decrypted_message = binaryString(decrypted_bin_message)
                    print(f"\nReceived from {source}: {decrypted_message[:length]}")
            else:
                print(f"\nReceived from server: {data['data']}")
    except Exception as e:
        print(f"\nError receiving messages: {e}")

if __name__ == "__main__":
    public_keys = {}
    state = "listen"
    target_id = None
    generated_des_key = randomString()
    session_des_key = None
    session_round_key = None

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8888))

    public_key, private_key, n = setkeys()
    n1 = random.randint(1000, 9999)
    n2 = random.randint(1000, 9999)
    recv_n1 = None

    print(f"{private_key} is your private key.")
    client.send(str({
        "public_key": public_key})
        .encode('utf-8'))

    welcome_msg = eval(client.recv(1024).decode('utf-8'))
    print(welcome_msg['data'])
    my_id = welcome_msg['client_id']

    receive_thread = threading.Thread(target=recvMessage, args=(client,))
    receive_thread.start()

    try:
        while True:
            time.sleep(0.1)
            if state == 'listen':
                if target_id is None:
                    while True:
                        target_id_str = input("'L' to show the list of connected clients\n'Ctrl + C' to exit\n'R' to refresh\nInput target client ID:")
                        if target_id_str.isdigit():
                            target_id = int(target_id_str)
                            if target_id in public_keys:
                                break
                            else:
                                print("Don't input your ID.")
                        elif target_id_str.strip().upper() in ['L', 'Q', 'R']:
                            break
                        else:
                            print("Invalid input.")
                    if target_id_str.lower() == 'q':
                        break
                    if target_id_str.lower() == 'l':
                        target_id = None
                        client.send(str({
                            "data": 'L'})
                            .encode('utf-8'))
                        continue
                    elif target_id_str.lower() == 'r':
                        print("Updating client.")
                        continue
                    else:
                        target_id = int(target_id_str)
                        state = 'chat'
                print("Retrieving session ...")
                selected_public_keys = public_keys[int(target_id)]
                data_step1 = {
                    'n1': n1,
                    'id_a': my_id
                }
                encrypted_step1 = encoder(
                    str(data_step1), selected_public_keys, n)
                client.send(str({
                    "step": 1,
                    "target_id": target_id,
                    "data": encrypted_step1,
                    'length': -1
                })
                    .encode('utf-8'))
                continue
            elif state == 'chat':
                message = input(f"Message to {target_id} ('bye' to stop chatting): ")
                if message.lower() == 'bye':
                    state = 'listen'
                    target_id = None
                else:
                    bin_message = stringBinary(message)
                    encrypted_bin_message = ''
                    for chunk in bin_message:
                        encrypted_bin_message += encrypt(chunk, session_round_key)
                    client.send(str({
                        'step': 5,
                        'target_id': target_id,
                        'length': len(message),
                        'data': encrypted_bin_message
                    })
                        .encode('utf-8'))

    except KeyboardInterrupt:
        pass

    finally:
        client.close()