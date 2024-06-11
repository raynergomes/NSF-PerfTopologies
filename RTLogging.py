#!/usr/bin/python
from socket import *
import time
import random
import threading
import os
import random
import string
import csv
import sys

bufsize = 1024 
targetHost = "10.0.0.32"
listenPort = 4444
localhost = "10.0.0.31"
pass_file = "/RTP/senhas.csv"

average_nap = 5
std_nap = 2
arrivals = []
mensages_to_send = []


def checkMensagens(pass_file, lixo):
    global arrivals
    global mensages_to_send

    while True:
        if arrivals:
           message = str(arrivals.pop())
           print("Arrived messages:", message)
           ip, user, passwd, time_orig, payload = message.split(":")
           if check_passwrd(pass_file, user, passwd):
               mensages_to_send.append(message)
           else:
               print("Password wrong.")
        else:
           time.sleep(1)              

def forward(port, targetHost):
    sock = socket(AF_INET, SOCK_DGRAM)
    global mensages_to_send
    
    while True:
        #print("Waiting for messages. Arrived %s" % (len(mensages_to_send)))
        if (mensages_to_send):
            print("Forwarding...")
            message = mensages_to_send.pop()
            ip,user,passwd,times,msg = message.split(":")
            times = times+","+str(time.time())
            message = ip+":"+user+":"+passwd+":"+times+":"+msg
            print("Forwarding: %s from port %s to %s" % (message, port, targetHost))
            sock.sendto(message.encode(), (targetHost, 4444))
        else:
            #print("Sleeping...")
            time.sleep(1)

def listen(host, port):
    global arrivals
    listenSocket = socket(AF_INET, SOCK_DGRAM)
    listenSocket.bind((host, port))

    while True:
        #print("Escutando na porta %s:%s" % (host, port))
        data, addr = listenSocket.recvfrom(bufsize)
        ip,user,passwd,times,msg = str(data).split(":")
        times = times+","+str(time.time())
        data = ip+":"+user+":"+passwd+":"+times+":"+msg
        # print("Inserindo o valor data e addr %s %s" % (data, addr))
        arrivals.append(data)
        

def generate_random_user(size=8):
    caracteres = string.ascii_letters 
    user = ''.join(random.choice(caracteres) for _ in range(size))
    return user

def generate_random_pass(size=8):
    caracteres = string.digits
    passwd = ''.join(random.choice(caracteres) for _ in range(size))
    return passwd

def create_initial_passwords(file_name, qty_pass):
    with open(file_name,'w',newline='') as f:
        for i in range(qty_pass):
            if i == qty_pass -1:
                user = "rayner"
                passwd = "1234"
            else:
                user = generate_random_user(8)
                passwd = generate_random_pass(8)
            line = [user,passwd]
            f_csv = csv.writer(f)
            f_csv.writerow(line)

def check_passwrd(pass_file, user, passwd):
    with open(pass_file, 'r', newline='') as f:
        f_csv = csv.reader(f)
        found = False
        login = False
        line = next(f_csv, None)
        while  line and not found:
            userline = line[0]
            passwdline = line[1]

            if userline == user and passwdline == passwd:
                found = True
                login = True
            elif userline == user and passwdline != passwd:
                found = True
            else:
                line = next(f_csv, None)
        
    return login


if __name__ == '__main__':

    if not os.path.exists(pass_file):
        create_initial_passwords(pass_file, 10)
     
    threadListen = threading.Thread(target=listen,  args=(localhost, listenPort))
    threadForward = threading.Thread(target=forward, args=(listenPort, targetHost))
    threadCheckMensages = threading.Thread(target=checkMensagens, args=(pass_file,""))

    threadListen.start()
    threadForward.start()
    threadCheckMensages.start()
    
    threadListen.join()
    threadForward.join()
    threadCheckMensages.join()
