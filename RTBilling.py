#!/usr/bin/python
from socket import *
import time
import threading
import sys
import json
import os


bufsize = 1024 
targetHost = "10.0.0.33"
listenPort = 4444
localhost = "10.0.0.32"
billing_file = "billing.json"

arrivals = []
mensages_to_send = []


def doBilling(bill_file, lixo):
    global arrivals
    global mensages_to_send

    while True:
        if arrivals:
            message = str(arrivals.pop())
            print("Arrived messanges:", message)
            ip, user, passwd, time_org, payload = message.split(":")
            found = False
            index = -1
            with open(bill_file, 'r') as bill_csv:
                dados = json.load(bill_csv)
                while not found and index < len(dados):
                    index +=1
                    if index < len(dados):
                        item = dados[index]
                        if item.get('id') == user:
                            item['valor'] += sys.getsizeof(payload)
                            found = True
            if not found:
                dado  = {'id':user, "valor": sys.getsizeof(payload)}
                dados.append(dado)

            with open(bill_file, 'w') as bill_csv:
                json.dump(dados, bill_csv, indent=2)
            
            mensages_to_send.append(message)

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
        times=times+","+str(time.time())
        data = ip+":"+user+":"+passwd+":"+times+":"+msg
        # print("Inserindo o valor data e addr %s %s" % (data, addr))
        arrivals.append(data)


def create_billing_log(file_name, qty_pass):
    dado = [{'id':0, 'valor':0}]
    with open(file_name, 'w') as f_csv:
        json.dump(dado, f_csv)

if __name__ == '__main__':

    if not os.path.exists(billing_file):
        create_billing_log(billing_file,"")

    threadListen = threading.Thread(target=listen,  args=(localhost, listenPort))
    threadForward = threading.Thread(target=forward, args=(listenPort, targetHost))
    threadBilling = threading.Thread(target=doBilling, args=(billing_file,""))

    threadListen.start()
    threadForward.start()
    threadBilling.start()
    
    threadListen.join()
    threadForward.join()
    threadBilling.join()

