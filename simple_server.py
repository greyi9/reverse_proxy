#!/usr/bin/env python

import threading
from multiprocess import Process
import socket, select, os, sys

HOST = ''
PROXY_TIMEOUT = 10 #seconds
RSHELL_TIMEOUT = 30 #seconds
processes = []

global conn_proxy_in
conn_proxy_in = [0]
global conn_proxy_out
conn_proxy_out = [0]
global conn_rshell
conn_rshell = [0]
global server_rshell
server_rshell = [0]


def proxy(flags):
    socket_bind(server_proxy_out,l_port_proxy_out)
    while running:
        try:
            conn_proxy_out[0] = server_proxy_out[0].accept()[0]
            conn_proxy_out[0].settimeout(PROXY_TIMEOUT)
            data = conn_proxy_out[0].recv(14336)
        except Exception as e:
            print "[*] Hmm: %s\n" % str(e)
        if data:
            h = 'HTTP/1.1 200 OK\n'
            h += 'Content-Type: text/html; charset=utf-8'
            h += 'Connection: close\n\n'
            r = h + '<h1>No Response</h1>' 
            try:
                conn_proxy_in[0].send(data)
                r = conn_proxy_in[0].recv(14336) 
	    except Exception as e:   
                r += '\n<pre>' + str(e) + '</pre>'            
            conn_proxy_out[0].send(r)
        conn_proxy_out[0].close()
    server_proxy_out[0].close()
    conn_proxy_in[0].close()
    server_proxy_in[0].close()
        

def proxy_create():
    global server_proxy_in
    global server_proxy_out
    global l_port_proxy_in
    global l_port_proxy_out
    server_proxy_in = ['foo']
    server_proxy_out = ['bar'] 
    try:
        server_proxy_in[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_proxy_out[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l_port_proxy_out = raw_input('Enter the port to proxy your browser traffic through: ')
        l_port_proxy_in = raw_input('Enter the port to receive proxied responses from remote host: ')
        l_port_proxy_out = int(l_port_proxy_out)
        l_port_proxy_in = int(l_port_proxy_in)
        ports = [l_port_proxy_out, l_port_proxy_in, l_port_rshell]
        if '' in ports:
            proxy_create()
        elif len(ports) > len(set(ports)):
            print "[*] Your reverse shell port and your two proxy ports must all be unique...\n"
            proxy_create()
    except Exception as e:
        print "[*] Hmm: %s" % str(e)              
    socket_bind(server_proxy_in,l_port_proxy_in)
#    conn_rshell[0].send('PROXY '+ str(l_port_proxy_in)) 
    socket_accept(server_proxy_in, conn_proxy_in)
    conn_proxy_in[0].settimeout(PROXY_TIMEOUT)
    flag = 'None'
    p = Process(target=proxy,args=(flag,))
    p.start()
    processes.append(p)    

def menu_create():
    print 'making menu....\n'

def socket_bind(server,port):
    try:
        server[0].bind((HOST, port))
    except Exception as e:
        print "[*] Hmm: %s \n" % str(e)
    try:
        server[0].listen(1)
    except Exception as e:
        print "[*] Hmm: %s \n" % str(e)

def socket_accept(server, conn):
    global r_proxy_addr
    try:
        conn[0], r_proxy_addr = server[0].accept()
        print "[*] Proxy connection established with %s " % r_proxy_addr[0]
    except Exception as e:
        print "[*] Hmm: %s\n" % str(e)

def menu(input):    
    global running
    running = True
    while running:
        cmd = raw_input("[*]" + str(hosts[0]) + " > ")
        if cmd == "quit":
            shutdown()
        elif cmd == "proxy":
            proxy_create()
        else:
            print "[*] Not Implemented: %s" % cmd

def shutdown():
    conn.close()
    server.close()
    running = False


def main():
    menu_create()
    menu('')    
    for proc in processes:
        proc.join
    sys.exit()

main()

