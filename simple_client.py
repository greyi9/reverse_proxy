#!/usr/bin/env python



import socket,ssl,base64
HOST_IP = "127.0.0.1"
HOST_P = 12345
s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s1.connect((HOST_IP,HOST_P))
while 1:
    data = s1.recv(1000000)
    data = base64.decodestring(data)
    dx = data.replace('\n',' ').replace('\r',' ').split(' ') 
    try:
        host, port = dx[dx.index("Host:")+1].strip().split(':')
    except:
        try: 
            host = dx[dx.index("Host:")+1].strip()
            port = 80
        except:
            continue
    port = int(port)
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if port == 443:
        c = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        c.verify_mode = ssl.CERT_NONE
        s2=c.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    try:
        s2.connect((host, port))
    except Exception as e:
        data = "<pre>" + e + "</pre>"
    s2.send(data)
    data = s2.recv(1000000)
    data = base64.encodestring(data)
    s1.send(data)
    s2.close()
s1.close()


