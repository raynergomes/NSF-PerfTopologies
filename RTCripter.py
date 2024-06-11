#!/usr/bin/python
from socket import *
import time
import random
import threading
import os

bufsize = 1024 
targetHost = "10.0.0.200"
listenPort = 4444
localhost = "10.0.0.34"

arrivals = []
messages_to_send = []

cript_file = "1"
key = 1


def cripto_msg(msg):
    global key
    cypher = ""
    for indice, caractere in enumerate(msg):
        codigo = ord(caractere)<<1
        novo =  chr(ord(caractere)<<int(key))
        cypher = cypher + novo
        
    return cypher

def cripto():
    global messages_to_send
    global arrivals
    global key
 
    while True:
        if arrivals:
            message = arrivals.pop()
            ip, user, passwd,time_origin, payload = str(message).split(":")
            payload = cripto_msg(payload)
            message = ip+":"+user+":"+passwd+":"+time_origin+":"+payload
            messages_to_send.append(message.encode())
        else:
            time.sleep(1)


def forward(port, targetHost):
    sock = socket(AF_INET, SOCK_DGRAM)
    # Retransmiti
    global messages_to_send
    
    while True:
        # print("Aguardando mensagens. Chegadas %s" % (len(arrivals)))
        if (messages_to_send):
            message = messages_to_send.pop()
            ip,user,passwd,times,msg = str(message).split(":")
            times = times + "," + str(time.time())
            message = ip+":"+user+":"+passwd+":"+times+":"+msg
            print("Forwarding: %s from port %s to %s" % (message, port, targetHost))
            sock.sendto(message.encode(), (targetHost, 4444))
        else:
            time.sleep(1)

def listen(host, port):
    global arrivals
    
    listenSocket = socket(AF_INET, SOCK_DGRAM)
    listenSocket.bind((host, port))
    while True:
        print("Listen on: %s:%s" % (host, port))
        data, addr = listenSocket.recvfrom(bufsize)
        ip,user,passwd,times,msg = str(data).split(":")
        times = times + "," + str(time.time())
        data = ip+":"+user+":"+passwd+":"+times+":"+msg
        print("Value inserted %s" % data)
        arrivals.append(data)

if __name__ == '__main__':
    threadListen = threading.Thread(target=listen,  args=(localhost, listenPort))
    threadForward = threading.Thread(target=forward, args=(listenPort, targetHost))
    threadCripto = threading.Thread(target=cripto, args=())
    
    threadListen.start()
    threadForward.start()
    threadCripto.start()

    threadListen.join()
    threadForward.join()
    threadCripto.join()
