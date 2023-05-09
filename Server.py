from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os

SERVER_DATA_PATH = "server_data"
HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

clients = {}
conn = {}
addresses = {}

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Enter your name.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    name = client.recv(BUFSIZ).decode("utf8")
    introduction  = 'Hello %s! If you want to quit, write {quit}.\n' % name
    client.send(bytes(introduction , "utf8"))
    msg = "%s joined boxchat!" % name
    broadcast(msg)
    clients[client] = name
    conn[name]=client

    while True:
        data = client.recv(BUFSIZ).decode("utf8")
        msg=data
        if(data.find(" ")!=-1):
            data= data.split(" ",1)
            # msg=data[0]
        # if data[1] == "{list}":
        #     broadcast_personal(name,name,"List of users who are online")
        #     for client in clients:
        #         broadcast_personal(name,name,(str(clients[client])+" "))
        #code for file_transfer
        elif data[0] == "{ft}":

            # Receive file details.
            file_name = client.recv(1024).decode("utf8")
            file_size = client.recv(1024).decode("utf8")

            # Opening and reading file.
            with open("./server_data/" + file_name, "wb") as file:
                c = 0
                # Running the loop while file is recieved.
                while c < int(file_size):
                    data = client.recv(1024)
                    if not (data):                       
                        break
                    file.write(data)
                    c += len(data)
                    print(c)
            
            file.close()
            print("File Transfer Complete.")
            broadcast("Data has been transferred successfully.")
        
        elif data[0] == "{quit}":
            # client.send(bytes("{quit}", "utf8"))          
            broadcast("%s quited boxchat." % name)
            client.close()
            # break
        
        else:
            if(data[0].find("@")!=-1):
                cmd= data[0].split("@",1)
                name_re=cmd[1]
                broadcast_personal(name,name_re,data[1])
            else: 
                broadcast(msg, name + ": ")


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg.encode("utf8"))

def broadcast_personal(name_send,name_re,msg, prefix=""):  # prefix is for name identification.
    conn[name_send].send(bytes(prefix, "utf8") + (name_send+"(Personal): "+msg).encode("utf8"))
    conn[name_re].send(bytes(prefix, "utf8") + (name_send+"(Personal): "+msg).encode("utf8"))


def sendfile(data):  # event is passed by binders.
    data=data.split(" ",1)
    name=data[0]
    file_name=data[1]
    file_size = os.path.getsize(file_name)
    conn[name].send(file_name.encode("utf8"))
    conn[name].send(str(file_size).encode("utf8"))
# Opening file and sending data.
    with open("./server_data/" + file_name, "rb") as file:
        c = 0
        # Running loop while c != file_size.
        while c <= file_size:
            data = file.read(1024)
            if not (data):
                break
            conn[name].sendall(data)
            c += len(data)
    file.close()
    print("File Transfer Complete.")



if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting connections from clients...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()