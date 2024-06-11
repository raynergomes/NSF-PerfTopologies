#!/usr/bin/python
from socket import *
import time
import threading
import sys
import json
import os


bufsize = 1024 
targetHost = "10.0.0.34"
listenPort = 4444
localhost = "10.0.0.33"
traf_analysis_file = "traf-analysis.json"

arrivals = []
mensages_to_send = []


def doAnalysis(ta_file, lixo):
    global arrivals
    global mensages_to_send

    while True:
        if arrivals:
            message = str(arrivals.pop())
            print("Arrived message:", message)
            ip, user, passwd, time_orig, payload = message.split(":")
            with open(ta_file, 'r') as bill_csv:
                dados = json.load(bill_csv)
                for letters in payload:
                    try:
                        dados[letters] += 1 
                    except KeyError:
                        dados[letters] = 1
            with open(ta_file, 'w') as bill_csv:
                json.dump(dados, bill_csv, indent=2)
            
            mensages_to_send.append(message.encode())
        else:
            time.sleep(1)              

def forward(port, targetHost):
    sock = socket(AF_INET, SOCK_DGRAM)
    global mensages_to_send
    
    while True:
        #print("Aguardando mensagens. Chegadas %s" % (len(mensages_to_send)))
        if (mensages_to_send):
            print("Forwarding...")
            message = mensages_to_send.pop()
            ip,user,passwd,times,msg = str(message).split(":")
            times = times + "," + str(time.time())
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
        times = times + "," + str(time.time())
        data = ip+":"+user+":"+passwd+":"+times+":"+msg
        # print("Inserindo o valor data e addr %s %s" % (data, addr))
        arrivals.append(data)


def create_ta_file(file_name, qty_pass):
    dado = {'id':0, 'valor':0}
    with open(file_name, 'w') as f_csv:
        json.dump(dado, f_csv)

if __name__ == '__main__':

    if not os.path.exists(traf_analysis_file):
        create_ta_file(traf_analysis_file,"")

    threadListen = threading.Thread(target=listen,  args=(localhost, listenPort))
    threadForward = threading.Thread(target=forward, args=(listenPort, targetHost))
    threadBilling = threading.Thread(target=doAnalysis, args=(traf_analysis_file,""))

    threadListen.start()
    threadForward.start()
    threadBilling.start()
    
    threadListen.join()
    threadForward.join()
    threadBilling.join()

