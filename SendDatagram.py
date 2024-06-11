import socket
import time

def send_udp_message(message, server_ip, server_port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, server_port)
    try:
        udp_socket.sendto(message.encode(), server_address)
        print(f"Message sent to {server_ip}:{server_port}: {message}")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    server_ip = "10.0.0.31"  
    server_port = 4444
    # ip, user, passwd, time: mensagem
    for i in range(30):
        for count in range(1750):
            time_now = time.time()
            message = "10.0.0.200:rayner:1234:"+str(time_now)+":Docker Falante"+", teste="+str(i)+", repetition="+str(count)
            send_udp_message(message, server_ip, server_port)
            time.sleep(0.05)
