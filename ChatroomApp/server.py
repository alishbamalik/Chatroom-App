# Chatroom App
# To allow a chatting platform for users
# January 13 2021
# Alishba Malik

# References

# Server Code


# message database application - sql

import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="alish")

# setting up database and table 
c = db.cursor()
c.execute("CREATE DATABASE IF NOT EXISTS chatroom")
c.execute("USE chatroom")
c.execute("CREATE TABLE IF NOT EXISTS msgs (Messages TEXT)")
c.close()


def add_msg_to_table(msg):
    c = db.cursor()
    c.execute("INSERT INTO msgs VALUES (%s)", (msg,))
    c.close()


def display_prev_msgs(client):
    c = db.cursor()

    count = c.execute("SELECT COUNT(*) FROM msgs")

    if count > 0:
        c.execute("SELECT Messages FROM msgs")
        while True:
            m = c.fetchone()

            if m is None:
                break
            client.sendall((m[0] + '\n').encode('ascii'))
        
    else:
        client.sendall('No Previous Messages.'.encode('ascii'))

    c.close()


# server and client application - python

import socket, threading

HOST = '127.0.0.1' # 0.0.0.0
PORT = 7977

clients = []
names = []


# closes the connection for that client and lets the other clients know
def close_connection(client,conn_closed=False):
    index = clients.index(client)
    name = names[index]

    clients.remove(client)
    print("Disconnected by {}".format(name))

    names.remove(name)
    display("{} has left the chat!".format(name).encode('ascii'))

    if not conn_closed:
        client.close()


# Sends message given from server or another client to all clients 
# connected to the server
def display(msg):
    for client in clients:
        client.sendall(msg)


# recieve messages and handles disconnections
def procedure(client):
    global db

    while True:
        try:
            msg = client.recv(1024).decode('ascii')

            if msg == '':
                close_connection(client,True)
                break
            else:
                pass
                # adding message to table in database
                try: 
                    add_msg_to_table(msg)
                    db.commit()
                except:
                    db.rollback()

                display(msg.encode('ascii'))

        except:
            close_connection(client)
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        # adding as a client
        client, addr = s.accept()
        clients.append(client)
        print('Connected by {}'.format(addr))

        # adding as a member
        client.sendall('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        display(("{} has joined the chat!".format(name)).encode('ascii'))

        # starts the process of all previous messages being displayed
        display_prev_msgs(client)

        # starting thread specific to the new connected client
        threading.Thread(target=procedure, args=(client,)).start()

