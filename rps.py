#!/usr/bin/env python



import socket,subprocess,ssl
HOST = "127.0.0.1"
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,12345))
while 1:
    r = s.recv(1024)
    x = r.split(' ')
    if 'QUIT' in x[0]:
        s.close()
    elif 'PROXY' in x[0]:
        proxy_port = int(x[1])
        pserv1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        pserv1.connect((HOST,proxy_port))
        while 1:
            data = pserv1.recv(14336)
            dx = data.replace('\n',' ').replace('\r',' ').split(' ') 
            try:
                host, host_ip = dx[dx.index("Host:")+1].strip().split(':')
            except:
                try: 
                    host = dx[dx.index("Host:")+1].strip()
                    host_ip = 80
                except:
                    host = None
            if host:
                host_ip = int(host_ip)
                pserv2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                pserv2.settimeout(60)
                pserv2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if host_ip == 443:
                    pserv2 = ssl.wrap_socket(pserv2, ssl_version=ssl.PROTOCOL_TLSv1, \
                                                         ciphers="ADH-AES256-SHA")
                
                pserv2.connect((host, host_ip))
                pserv2.send(data)
                pserv1.send(pserv2.recv(14336))
                pserv2.close()
        pserv1.close()                
    s.send(r)
s.close()


