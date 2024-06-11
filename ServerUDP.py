import socket
import time
import sys
import statistics as stat
import json


amount = 0
arrivals = []
sizes = []

def udp_server(server_ip, server_port, new_file):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (server_ip, server_port)
        udp_socket.bind(server_address)
        print(f"UDP server listening on {server_ip}:{server_port}")
        count = 0
        messages = []
        while True:
            count+=1
            data, address = udp_socket.recvfrom(1024)
            print(f"{count} - Received message from {address}")
             # ip, user, passwd, time, mensagem
            ip, user, passwd, times, message = data.decode().split(":")
            print(times)
            total = times.split(",")
            t1 = float(total[1]) - float(total[0])
            c1 = float(total[2]) - float(total[1])
            t2 = float(total[3]) - float(total[2])
            c2 = float(total[4]) - float(total[3])
            t3 = float(total[5]) - float(total[4])
            c3 = float(total[6]) - float(total[5])
            t4 = float(total[7]) - float(total[6]) 
            c4 = float(total[8]) - float(total[7])
            now = time.time()
            t5 = now - float(total[8])
            info = [t1,c1,t2,c2,t3,c3,t4,c4,t5,now - float(total[0]) ]
            messages.append(info)
            
    except:
        print("Saving file as JSON")
        with open(new_file, 'w') as msg_file:
            json.dump(messages, msg_file, indent=2)
            

if __name__ == "__main__":
    new_file = str(time.time()).split(".")[0] + ".json"
    server_ip = "10.0.0.200"  
    server_port = 4444  
    udp_server(server_ip, server_port, new_file)
