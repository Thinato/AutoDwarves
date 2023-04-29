import socket
import threading
import os
import sys
import pygame as pg

HEADER = 1024
HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

player_list = []

def listen():
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        sys.stdout.write('\b')
        player_list.append(addr)
        print(f"[ACTIVE CONNECTIONS] {len(player_list) - 1}")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}")
    thread = threading.Thread(target=listen)
    thread.start()
    
    while True:
        cmd = input()
        print(cmd)


os.system('cls')
print('[STARTING] server is starting...')
start()