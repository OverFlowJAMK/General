# Server program
import socket
import sys
import codecs
import time
import json
from jwcrypto.common import json_decode
from jwcrypto.common import json_encode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT

def RSA_key():
    key = JWK(generate="RSA",public_exponent=29,size=1000) #public_exponent pitää olla alkuluku (e)
    return key

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
data = conn.recv(1024)
string = data.decode("UTF-8")
print(string)
key = RSA_key()
public_key = key.export_public()
conn.send(public_key.encode("UTF-8"))
#otetaan viesti vastaan
data = conn.recv(1024)
string = data.decode("UTF-8")
print(string)

print("closing")
conn.close()
