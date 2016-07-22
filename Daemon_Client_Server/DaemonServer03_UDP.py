# Server program UDP
import ast
import socket
import sys
import codecs
import time
import json
import requests
import queue
from backports import configparser
import _thread as thread
from jwcrypto.common import json_decode
from jwcrypto.common import json_encode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT

#käynnistettään tarkistuskierros uusiksi säikeessä
def Listen_Client(url,data,tport,q,header):
    try:
        while True:
            #print("---Thread---")
            HOST = '0.0.0.0'
            PORT = int(tport)
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                conn.bind((HOST, PORT))
                print("Thread *** Bind is ready", PORT)
            except:
                print("Thread *** Connection bind failed")
                Listen_Client(url,data,PORT,q,header)
            info = conn.recvfrom(1024)
            #print(info)
            data = info[0].decode("utf-8")
            #print (data)
            addr = info[1]
            #print (addr)
            #print("-" * 60)
            #print('Thread *** connected by', addr)
            key = JWK(generate="RSA",public_exponent=29,size=1000)
            public_key = key.export_public()
            #print('Thread *** public key',public_key)
            conn.sendto(public_key.encode("utf-8"),addr)
            #otetaan viesti vastaan ja avataan
            try:
                conn.settimeout(60)
                encrypted_signed_token_info = conn.recvfrom(1024)
                encrypted_signed_token = encrypted_signed_token_info[0].decode("utf-8")
                #print(encrypted_signed_token)
            except:
                print('Thread *** time out')
                break
            E = JWE()
            E.deserialize(encrypted_signed_token, key)
            raw_payload = E.payload
            string = raw_payload.decode("utf-8")
            Payload = json.loads(string)
            #print("Thread *** received payload:", Payload['exp'])
            #käydään REST app kysymässä Kumokselta
            mac = str(Payload['exp'])
            myResponse = requests.get(url + mac,header)
            #print(url + mac,header)
            #print("Thread *** REST:", myResponse.status_code)
            #tarkistus
            if(myResponse.ok):
                print("Thread *** Found!")
                jData = json.loads(myResponse.content.decode("utf-8"))
                #print("The response contains {0} properties".format(len(jData)))
                conn.close()
            else:
                print("Thread *** Not found")
                answer="Good try <3"
                conn.send(answer.encode("utf-8"))
                #SDN irrottaa kyseisen laitteen verkosta
                break
            conn.close()
        print("Thread *** end")
        q.put(tport)
    except:
        q.put(tport)
        print("Thread *** Forced end")

def ServerMain():
    try:
        Config = configparser.ConfigParser() 
        q=queue.Queue()
        filu = 'serveraddress.ini'
        HOST = '0.0.0.0'    #change to None if wanted listen from IPv6 address
        try:
            fp = open(filu, 'r+')
            Config.readfp(fp)
            url = Config.get('REST','url')
            header = Config.get('REST','header')
            tport = int(Config.get('DAEMON','port'))
            PORT = int(Config.get('DAEMON','port'))
            fp.close()
        except:
            filu = input('anna kansion nimi:')
            url = input('anna url:')
            header = input('anna header:')
            port = input('anna port:')
            cfgfile = open(filu,'w')
            try:
                Config.add_section('REST')
                Config.add_section('DAEMON')
                print("*** Created sections")
            except:
                print('*** sections already exists')
            Config.set('REST','url',url)
            Config.set('REST','header', header)
            Config.set('DAEMON','port',port)
            Config.write(cfgfile)
            cfgfile.close()
            tport = int(Config.get('DAEMON','port'))
            url = Config.get('REST','url')
            header =  Config.get('REST','header')
            PORT = int(Config.get('DAEMON','port'))
            print("*** Created information.")
        header = ast.literal_eval(header)

        while True:
            print("*** Main ***")
            #print("*" * 60)
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                conn.bind((HOST, PORT))
            except:
                print("Main *** Ei onnistunut")
                ServerMain()
            info = conn.recvfrom(1024)
            print(info)
            data = info[0].decode("utf-8")
            print (data)
            addr = info[1]
            print (addr)
            
            #datan tarkistus ja säikeen aloitus
            if data=="I am Client":
                #print("Main *** Right start message")

                #lähetetään julkinen avain
                key = JWK(generate="RSA",public_exponent=29,size=1000)
                public_key = key.export_public()
                conn.sendto(public_key.encode("utf-8"),addr)

                #otetaan viesti vastaan ja avataan
                encrypted_signed_token = conn.recv(1024).decode("utf-8")
                #print(encrypted_signed_token)

                E = JWE()
                E.deserialize(encrypted_signed_token, key)
                raw_payload = E.payload
                #print("*** raw payload:",raw_payload)
                string = raw_payload.decode("utf-8")
                #print("*** received str:", string)
                Payload = json.loads(string)
                #print("*** JSON:",Payload)
                #print("*** received payload:", Payload['exp'])

                #käydään REST app kysymässä Kumokselta
                mac = str(Payload['exp'])
                myResponse = requests.get(url + mac,header)
                #print(url + mac,header)
                #print("REST:", myResponse.status_code)
                if(myResponse.ok):
                    print("main *** Found!")
                    jData = json.loads(myResponse.content.decode("utf-8"))
                    #print("The response contains {0} properties".format(len(jData)))
                    
                    # Konrollerille yhteys
                    
                    
                    #Haetaan "listalta"
                    if not q.empty():
                        tport = q.get()
                        conn.sendto(tport.encode("utf-8"),addr)
                    else:
                        tport = str(int(tport)+1)
                        conn.sendto(tport.encode("utf-8"),addr)

                    #Aloitetaan stringissä uusi yhteys
                    thread.start_new_thread(Listen_Client,(url,data,tport,q,header,))
                else:
                    print("main *** Not found")
                    answer="Good try <3"
                    conn.sendto(answer.encode("utf-8"),addr)
            else:
                conn.close()
                print("*" * 60)
        conn.close()
        print("*" * 60)
    except:
        print("Main *** frong message. Start again")
        ServerMain()
        
ServerMain()
