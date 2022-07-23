from ipaddress import ip_address
from os import remove
import socket
from threading import Thread

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address="127.0.0.1"
port=8000
server.bind((ip_address,port))
server.listen()
clients=[]
print("The server is running...")

def clientsThread(conn,addr):
    conn.send("welcome to this chat room".encode('utf-8'))
    while True:
        try:
            message=conn.recv(2048).decode('utf-8')
            if (message):
                print("<"+addr[0]+">"+message)
                message_to_send="<"+addr[0]+">"+message
                broadcast(message_to_send,conn)
            else:
                remove(conn)
        except:
            continue
def broadcast(message,conn):
    for client in clients:
        if (clients!=conn):
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(client)    
def remove(conn):
    if (conn in clients):
        clients.remove(conn)
while True:
    conn,addr=server.accept()
    clients.append(conn)
    print(addr[0]+" connected")

    new_thread=Thread(target=clientsThread,args=(conn,addr))
    new_thread.start()

