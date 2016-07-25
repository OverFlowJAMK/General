#Client program
import json
import codecs
import sys
import socket
import time
import _thread as thread
from backports import configparser
Config = configparser.ConfigParser()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
from jwcrypto.common import json_decode, json_encode
from jwcrypto import jwk
from jwcrypto import jws
from jwcrypto import jwe
from jwcrypto import jwt

def RSA_public(key):
    P = dict(json.loads(key.decode("UTF-8")))
    return jwk.JWK(**P)

def ErrorHandling(filu,t,IP,PORT,CHECK):
    ip = input('anna ip:')
    port = input('anna port:')
    user = input('anna user:')
    passw = input('anna passw:')
    
    cfgfile = open(filu,'w')
    while True:
        try:
            Config.add_section('UDP')
            Config.add_section('KaMU')
            Config.add_section('Check')
            print("*** Created.")
        except socket.error as msg:
            print(msg)
            continue
        break
    Config.set('UDP','UDP_IP',ip)
    Config.set('UDP','UDP_PORT', port)
    Config.set('KaMU','username',user)
    Config.set('KaMU','password',passw)
    Config.set('Check','sections', '${UDP,udp_ip} ${UDP,udp_port} ${KaMU,username} ${KaMU,password}')
    
    Config.write(cfgfile)
    cfgfile.close()
    
    print("*** Created information.")
    send_UDP(filu,t)
        

def send_UDP(kierros,filu,t,IP,PORT,CHECK):
    while kierros<=10:
        kierros = kierros+1
        print(kierros,"*** try connection")
        s = None
        for res in socket.getaddrinfo(IP, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                s = None
                continue
            try:
                s.connect(sa)
            except socket.error as msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print(kierros,'*** could not open socket')
            send_UDP(kierros,filu,t,IP,PORT,CHECK)
                
        s.sendall(CHECK.encode("utf-8"))
        print(kierros,'*** new connection port:')
        PAYLOAD = Config.get('KaMU','password')#näyttää tarkistavan tämän vain jos koko aliohjelma alkaa alusta             
        try:
            s.settimeout(10)
            key = s.recv(1024)
            s.settimeout(None)
            if key == b'Good try <3':
                PORT = int(Config.get('UDP','udp_port'))
                send_UDP(filu,t,IP,PORT,CHECK)
        except socket.error as msg:
            print(kierros,'*** could not revice key')
            s.close()
            send_UDP(kierros,filu,t,IP,PORT,CHECK) 
        public_key = RSA_public(key)
        claims = dict(exp=PAYLOAD)
        header = dict(alg="RSA-OAEP-256", enc="A128GCM")
        T = jwt.JWT(header, claims)
        T.make_encrypted_token(public_key)
        encrypted_signed_token = T.serialize(compact=True)
        s.sendall(encrypted_signed_token.encode("utf-8"))
        #print(kierros,'*** send inoformation')

        NEW_PORT = s.recv(1024).decode("utf-8")
        print(NEW_PORT)
        if NEW_PORT == b'':
            s.close()
            send_UDP(kierros,filu,t,IP,PORT,CHECK)
        s.close()
        thread.start_new_thread(Continue_Conversation,(kierros,filu,t,IP,NEW_PORT,))
        time.sleep(10)

def Continue_Conversation(kierros,filu,t,IP,PORT):
        try:
            while True:
                s = None
                for res in socket.getaddrinfo(IP, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
                    af, socktype, proto, canonname, sa = res
                    try:
                        s = socket.socket(af, socktype, proto)
                    except socket.error as msg:
                        s = None
                        continue
                    try:
                        s.connect(sa)
                    except socket.error as msg:
                        s.close()
                        s = None
                        continue
                    break
                if s is None:
                    print(kierros,'*** could not open socket')
                    time.sleep(t)
                    Continue_Conversation(kierros,filu,t,IP,PORT)
            
                print(kierros,'*** port:',PORT)
                PAYLOAD = Config.get('KaMU','password')#näyttää tarkistavan tämän vain jos koko aliohjelma alkaa alusta
                try:
                    s.settimeout(10)
                    key = s.recv(1024)
                    s.settimeout(None)
                    if key == b'Good try <3':
                        break
                except socket.error as msg:
                    time.sleep(t)
                    continue
                public_key = RSA_public(key)

                claims = dict(exp=PAYLOAD)
                header = dict(alg="RSA-OAEP-256", enc="A128GCM")
                T = jwt.JWT(header, claims)
                T.make_encrypted_token(public_key)
                encrypted_signed_token = T.serialize(compact=True)
                s.sendall(encrypted_signed_token.encode("utf-8"))
                #print(kierros,'*** send inoformation')

                s.close()
                print(kierros,"*** connect close.")
        except:
            print(kierros,"Error")

        
kierros=0
t = 5
filu = 'daemon.ini'
fp = open(filu, 'r+')
Config.readfp(fp)
try:
    Config.get('Check', 'sections')
except:
    print("*** File is missing sections and information.")
    ErrorHandling(filu,t)
print("Tarkistetaan kansio")
IP = Config.get('UDP','udp_ip')
PORT = int(Config.get('UDP','udp_port'))
CHECK = Config.get('KaMU','username')
#PAYLOAD = Config.get('KaMU','password')
fp.close()
send_UDP(kierros,filu,t,IP,PORT,CHECK)
#while True:
#    kierros= kierros+1
#    thread.start_new_thread(send_UDP,(kierros,filu,t,IP,PORT,CHECK,))
#    time.sleep(20)

