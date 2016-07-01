# Server program
import socket
import json
import sys
import codecs

HOST = '0.0.0.0'    #change to None if wanted listen from IPv6 address
PORT = 50000
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        print(sa)
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if not data: break
    print("received bytes-like:", data)
    conn.send(data)
    string = data.decode("utf-8")
    print("received str:", string)
    Payload = json.loads(string)
    print("received username:", Payload['username'])
    print("received password:", Payload['password'])
print("closing")
conn.close()
