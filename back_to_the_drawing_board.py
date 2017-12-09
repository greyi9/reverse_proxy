#!/usr/bin/env python

import ssl, socket, select
lport = 8080
lhost = '127.0.0.1'
def run():
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((lhost, lport))
    s1.listen(1)
    try:
        try:
            c1, addr = s1.accept()
            data = c1.recv(8192)
            print "Data Recv: \n %s" % data
            dx = data.replace('\n',' ').replace('\r',' ').split(' ')
            rhost = dx[dx.index("Host:")+1].strip().split(':')
            rport = 80
            if len(rhost)>1:
                rport = int(rhost[1])
            rhost = rhost[0]
            c1.send(b"HTTP/1.0 200 established\r\n\r\n")
            print "200 Sent\n"

            print "checking for ssl...\n"
            c1.setblocking(0)
            timeout_in_seconds = 1
            ready = select.select([c1], [], [], timeout_in_seconds)
            if ready[0]:
                data = c1.recv(4096)
                print "Data Recv: \n %s" % data
            else:
                print "not ready"

            try:
                c1 = ssl.wrap_socket(c1, certfile='cacert.der', server_side=True)
            except Exception as e:
                print "ssl wrap error:... \n%s\ntrying without ssl...\n" % str(e)



            print "Client-Proxy connection established...\n"
          

 
            s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            h = 'HTTP/1.1 200 OK\n'
            h += 'Content-Type: text/html; charset=utf-8'
            h += 'Connection: close\n\n'
            r = h + '<h1>No Change to R value in try block... </h1>'
            try:
                s2.connect((rhost, rport))
            except Exception as e:
                print "Couldn't connect without ssl...\n Error: %s" % e
                try:
                    print "trying to connect to the client with SSLv23\n"
                    c = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                    c.verify_mode = ssl.CERT_NONE
                    s2=c.wrap_socket(socket.socket(socket.AF_INET), server_hostname=rhost)
                except Exception as e:
                    print "Couldn't connect with SSLv23... \nError: %s\n" % e
            finally:
                c1.send(r)
                s2.close()




        finally:
            print 00
    finally:
        print 0
run()
