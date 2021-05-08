import time
import datetime
import socket
import logging
from multiprocessing import Process

TARGET_IP = '192.168.1.0'
TARGET_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT, 1)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)

def get_image_list():
    paths = dict()
    paths['bear']='bear.png'
    paths['bunga']='bunga.jpg'
    paths['camera']='camera.jpg'
    paths['kelinci']='kelinci.png'
    paths['pinguin']='pinguin.png'
    return paths

def broadcast_image(path=None):
    waktu_awal = datetime.datetime.now()
    if (path is None):
        return False

    f=open(path,"rb")
    sendfile = f.read(1024)
    while (sendfile):
        if(sock.sendto(sendfile, (TARGET_IP, TARGET_PORT))):
            # print(f"sending...")
            sendfile = f.read(1024)
    f.close()
    #untuk simulasi, diberi tambahan delay 2 detik
    time.sleep(2) 

    waktu_process = datetime.datetime.now() - waktu_awal
    waktu_akhir =datetime.datetime.now()
    logging.warning(f"writing {path} dalam waktu {waktu_process} {waktu_awal} s/d {waktu_akhir}")
    return waktu_process

flag = 0
while flag < 1:

    try:
        texec = dict()
        paths = get_image_list()

        catat_awal = datetime.datetime.now()
        for k in paths:
            print(f"mengirim gambar {paths[k]}")
            waktu = time.time()
            
            # bagian ini merupakan bagian yang mengistruksikan eksekusi fungsi broadcast gambar secara multiprocess
            texec[k] = Process(target=broadcast_image, args=(paths[k],))
            texec[k].start()
        
        #setelah menyelesaikan tugasnya, dikembalikan ke main process dengan join
        for k in paths:
            texec[k].join()

        catat_akhir = datetime.datetime.now()
        selesai = catat_akhir - catat_awal
        print(f"Waktu TOTAL yang dibutuhkan {selesai} detik {catat_awal} s/d {catat_akhir}")

    finally:
        print(f"done")
        flag = 1
    