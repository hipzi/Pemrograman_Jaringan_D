import socket
import time

TARGET_IP = '192.168.122.0'
TARGET_PORT = 5005


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT, 1)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)


angka = 0
while True:
    angka = angka+1
    msg = " BROADCAST ini angka {} " . format(angka)
    print(msg)
    sock.sendto(msg.encode(), (TARGET_IP, TARGET_PORT))
    time.sleep(1)
