#!/usr/bin/env python



import socket,ssl
HOST_IP = "127.0.0.1"
HOST_P = 12345
PROXY_IP = "192.168.0.1"
PROXY_P = 8000
s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s1.connect((HOST_IP,HOST_P))
while 1:
    data = s1.recv(1000000)
    dx = data.replace('\n',' ').replace('\r',' ').split(' ') 
    try:
        host, port = dx[dx.index("Host:")+1].strip().split(':')
    except:
        try: 
            host = dx[dx.index("Host:")+1].strip()
            port = 80
        except:
            continue
    try:
        ip = socket.gethostbyname(host)
    port = int(port)
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if port == 443:
        s2 = ssl.wrap_socket(s2)
    s2.connect((host, port))
    s2.send(data)
    s1.send(s2.recv(1000000))
    s2.close()
s1.close()


