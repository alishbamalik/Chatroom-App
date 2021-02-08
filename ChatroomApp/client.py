# Chatroom App
# To allow a chatting platform for users
# January 13 2021
# Alishba Malik

# References

# Client Code

import socket, threading

name = input("Choose your name: ")

if name == '':
    exit()
    
HOST = '127.0.0.1'
PORT = 7977

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

close_conn = False

# closes the connection
def close_connection():
    global close_conn
    close_conn = True
    print("Disconnected.")
    s.close()

# recieve messages from server
def recieve():''
    global close_conn

    while True:
        try:
            msg = s.recv(1024).decode('ascii')

            if msg == 'NAME':
                s.sendall(name.encode('ascii'))
            else:
                print(msg)

        except:
            if close_conn:
                break
            else: 
                print("Error Occured.")
                s.close()
                break


# writes messages to server
def write():
    global close_conn

    while not close_conn:
        client_input = input()
        
        if client_input == '':
            close_connection()
            break
        else:
            msg = '{}: {}'.format(name, client_input)
            s.sendall(msg.encode('ascii'))


threading.Thread(target=write).start()
threading.Thread(target=recieve).start()