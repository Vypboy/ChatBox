import socket
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import filedialog
import os


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    # data=msg.split(" ")
    data= msg.split(" ")
    if msg == "{quit}":
        # client_socket.close()
        top.quit()
    elif data[0] == "{ft}":
        print("sendfile")
        sendfile(data[1])

def on_closing(event=None):
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter and File transfer")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Enter your name.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Gửi", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


    

def sendfile(file_name):
    file_size = os.path.getsize(file_name)
    client_socket.send(file_name.encode("utf8"))
    client_socket.send(str(file_size).encode("utf8"))
# Opening file and sending data.
    with open(file_name, "rb") as file:
        c = 0
        # Running loop while c != file_size.
        while c <= file_size:
            data = file.read(1024)
            print(c)
            if not (data):
                break
            client_socket.sendall(data)
            c += len(data)
    file.close()
    print("File Transfer Complete.")


    ################################################################


def receivefile():
    while True:
        try:
            file_name = client_socket.recv(1024).decode("utf8")
            file_size = client_socket.recv(1024).decode("utf8")

            # Opening and reading file.
            with open("./client_data/" + file_name, "wb") as file:
                c = 0
                # Running the loop while file is recieved.
                while c <= int(file_size):
                    data = client_socket.recv(1024)
                    if not (data):
                        break
                    file.write(data)
                    c += len(data)
            file.close()
            msg_list.insert(tkinter.END, "File receive Complete.")
        except OSError:  # Possibly client has left.
            break


# Phan Cuong lam ket thuc

# Ket noi toi server
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

if __name__ == "__main__":
    receive_thread = Thread(target=receive)
    receive_thread.start()

    # receive_file_thread = Thread(target=receivefile)
    # receive_file_thread.start()

    tkinter.mainloop()  # Starts GUI execution.
