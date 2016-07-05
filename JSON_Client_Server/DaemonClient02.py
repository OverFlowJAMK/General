#Client program
import json
import codecs
import sys
import socket
import time
from backports import configparser
Config = configparser.ConfigParser()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def RSA_public(key):
    P = dict(json.loads(key.export_public()))
    return JWK(**P)

def ErrorHandling(filu,t):
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
        

def send_UDP(filu,t):
    while True:
        fp = open(filu, 'r+')
        Config.readfp(fp)
        try:
            Config.get('Check', 'sections')
        except:
            print("*** File is missing sections and information.")
            ErrorHandling(filu,t)
            break

        IP = Config.get('UDP','udp_ip')
        PORT = int(Config.get('UDP','udp_port'))
        PAYLOAD = json.dumps({"username": Config.get('KaMU','username'), "password": Config.get('KaMU','password')})
        fp.close()
        
        print ("ip:", IP)
        print ("port:", PORT)
        print (PAYLOAD)

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
            print('*** could not open socket')
            time.sleep(t)
            send_UDP(filu,t)
        s.sendall(PAYLOAD.encode())
        print('*** send inofrmation')
        try:
            s.settimeout(10)
            key = s.recv(1024)
            s.settimeout(None)
            s.close()
            break
        except socket.error as msg:
            print('*** timeout')
            time.sleep(t)
            continue
        
        public_key = RSA_public(key)
        
    
    print('Received', repr(data))
    sys.exit(1)

t = 30
filu = 'daemon.ini'

send_UDP(filu,t)
