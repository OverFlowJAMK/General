#Client program UDP
import json
import codecs
import sys
import socket
import time
from backports import configparser
Config = configparser.ConfigParser()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
from jwcrypto.common import json_decode, json_encode
from jwcrypto import jwk
from jwcrypto import jws
from jwcrypto import jwe
from jwcrypto import jwt
    

def ErrorHandling(filu,section,a_info,b_info):
    print(filu,section,a_info,b_info)
    cfgfile = open(filu,'w')
    try:
        Config.add_section(section)
        print("*** Created section")
    except:
        print("*** Section already exists")
        
    if filu == 'ServerAddress.ini':
        a = input('server ip:')
        b = input('server port:')
    else:
        a = input('mac address:')
        b = str(time.time())
    Config.set(section,a_info,a)
    Config.set(section,b_info,b)
    Config.write(cfgfile)
    cfgfile.close()
    print("*** New",filu,"created")

def send_UDP(afilu,bfilu,t,IP,PORT,PAYLOAD):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            print("-"*60)
            
            #Lähetetään check        
            CHECK = "I am Client"
            PORT = int(PORT)
            s.sendto(CHECK.encode("utf-8"),(IP,PORT))
            print('*** send check')
                
            bfp = open(bfilu, 'r')
            Config.readfp(bfp) 
            PAYLOAD = Config.get('KaMU','username')
            bfp.close()
            print ("ip:", IP)
            print ("port:", PORT)
            print (PAYLOAD)
                    
            try:
                s.settimeout(t)
                info = s.recvfrom(1024)
                print(info)
                key = info[0]
                s.settimeout(None)
            except:
                print('*** timeout')
                continue
            if key == b'Good try <3':
                afp = open(afilu, 'r')
                Config.readfp(afp)
                PORT = int(Config.get('address','port'))
                afp.close()

                send_UDP(afilu,bfilu,t,IP,PORT,PAYLOAD)
                
            #Salataan ja lähetetään tieto julkisella avaimella
            P = dict(json.loads(key.decode("UTF-8")))
            public_key = jwk.JWK(**P)
            claims = dict(exp=PAYLOAD)
            header = dict(alg="RSA-OAEP-256", enc="A128GCM")
            T = jwt.JWT(header, claims)
            T.make_encrypted_token(public_key)
            encrypted_signed_token = T.serialize(compact=True)
            print("*** engrypted signed token:",encrypted_signed_token)
            s.sendto(encrypted_signed_token.encode("utf-8"),(IP,PORT))
            print('*** send inoformation')

            afp = open(afilu, 'r')
            Config.readfp(afp)
            old_PORT = int(Config.get('address','port'))
            afp.close()

            if PORT == old_PORT:
                NEW_PORT = s.recv(1024).decode("utf-8")
                if PORT == b'':
                    send_UDP(afilu,bfilu,t,IP,PORT,PAYLOAD)
                else:
                    s.close()
                    send_UDP(afilu,bfilu,t,IP,NEW_PORT,PAYLOAD)
            time.sleep(t)
    except:
        afp = open(afilu, 'r')
        Config.readfp(afp)
        old_PORT = int(Config.get('address','port'))
        afp.close()
        print("New start")
        time.sleep(t)
        send_UDP(afilu,bfilu,t,IP,old_PORT,PAYLOAD)

t = 20
afilu = 'ServerAddress.ini'
bfilu = 'ClientDaemon.ini'

while True:
    print("*** Opening",afilu)
    try:
        afp = open(afilu, 'r')
        Config.readfp(afp)
        IP = Config.get("address","ip")
        PORT = int(Config.get("address","port"))
        afp.close()
        break
    except:
        print("*** File is missing sections and information.")
        ErrorHandling(afilu,"address","ip","port")
           
while True:
    print("*** Opening",bfilu)   
    try:
        bfp = open(bfilu, 'r')
        Config.readfp(bfp) 
        PAYLOAD = Config.get("KaMU","username")
        bfp.close()
        break
    except:
        print("*** File is missing sections and information.")
        bfp.close()
        ErrorHandling(bfilu,"KaMU","username","time")

send_UDP(afilu,bfilu,t,IP,PORT,PAYLOAD)
