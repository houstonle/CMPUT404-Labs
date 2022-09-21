#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    proxy_host = 'www.google.com'
    proxy_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
                print("Connecting to google")
                remote_ip = get_remote_ip(proxy_host)

                #connect proxy_socket
                proxy_socket.connect((remote_ip, proxy_port))

                p = Process(target=handle_echo, args=(addr,proxy_socket, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()

def handle_echo(addr, pconn, conn):
    #send data
    send_full_data = pconn.recv(BUFFER_SIZE)
    pconn.sendall(send_full_data)
    #shutdown
    pconn.shutdown(socket.SHUT_WR)
    data = pconn.recv(BUFFER_SIZE)
    conn.send(data)

if __name__ == "__main__":
    main()