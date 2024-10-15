# Broadcaster Script #
# Thisi s a very simple script used for testing purposes when building this app.

import socket


MAXIMUM_CHARACTERS = 1025
FORMAT = "utf-8"
EXIT_COMMAND = "^DISCONNECT"

ip = str(input("enter the ip you wanna broadcast at. \n"))
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((ip,5050))
print("connected, anything you input now will be broadcasted to the server.")
while True:
    global_message = str(input())
    packet = global_message.encode(FORMAT)
    packet_length = len(packet)
    s_Length = str(packet_length).encode(FORMAT)
    s_Length += b' '*(MAXIMUM_CHARACTERS-len(s_Length))

    sock.send(s_Length)
    sock.send(packet)
