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
import _thread as thread
    

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

def send_UDP(afilu,bfilu,t,IP,PORT,PAYLOAD,error_test,threadnumber):
    try:
        print(threadnumber)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        kierros = 0
        while True:
            print("-"*60)
            
            #Lähetetään check        
            CHECK = "I am Client"
            PORT = int(PORT)
            s.sendto(CHECK.encode("utf-8"),(IP,PORT))
            #print('*** send check')

            if error_test==10:
                kierros = kierros+1
                if kierros==20:
                    PAYLOAD = 'max=00-00-00-00-00-00'
                
            #bfp = open(bfilu, 'r')
            #Config.readfp(bfp) 
            #PAYLOAD = Config.get('KaMU','username')
            #bfp.close()
            #print ("ip:", IP)
            #print ("port:", PORT)
            #print (PAYLOAD)
                    
            try:
                s.settimeout(t)
                info = s.recvfrom(1024)
                #print(info)
                key = info[0]
                s.settimeout(None)
            except:
                print(threadnumber,'*** timeout')
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
            #print("*** engrypted signed token:",encrypted_signed_token)
            s.sendto(encrypted_signed_token.encode("utf-8"),(IP,PORT))
            #print(threadnumber,'*** send inoformation')

            afp = open(afilu, 'r')
            Config.readfp(afp)
            old_PORT = int(Config.get('address','port'))
            afp.close()

            if PORT == old_PORT:
                NEW_PORT = s.recv(1024).decode("utf-8")
                if PORT == b'':
                    send_UDP(afilu,bfilu,t,IP,PORT,PAYLOAD,error_test,threadnumber)
                else:
                    s.close()
                    send_UDP(afilu,bfilu,t,IP,NEW_PORT,PAYLOAD,error_test,threadnumber)
            time.sleep(t)
    except:
        afp = open(afilu, 'r')
        Config.readfp(afp)
        old_PORT = int(Config.get('address','port'))
        afp.close()
        print(threadnumber,"New start")
        #time.sleep(t)
        send_UDP(afilu,bfilu,t,IP,old_PORT,PAYLOAD,error_test,threadnumber)

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
        ErrorHandling(bfilu,"KaMU","username","time")
threadnumber = 0
kierros = 0
error_test = 0
while True:
    kierros = kierros+1
    error_test = error_test+1
    threadnumber = threadnumber+1
    if kierros==10:
        thread.start_new_thread(send_UDP,(afilu,bfilu,t,IP,PORT,'mac=00-00-00-00-00-00',error_test,threadnumber,))
    elif error_test==20:
        thread.start_new_thread(send_UDP,(afilu,bfilu,t,IP,PORT,PAYLOAD,10,threadnumber,))
    else:
        thread.start_new_thread(send_UDP,(afilu,bfilu,t,IP,PORT,PAYLOAD,error_test,threadnumber,))
    time.sleep(1)
