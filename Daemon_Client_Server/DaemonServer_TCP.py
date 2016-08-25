# Server program TCP
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
session= requests.Session()

#Tarkistetaan rest
def Check_rest(url,mac,header):
    myResponse = session.get(url=url+mac, headers=header)
    #print('*** ',myResponse.status_code)
    return myResponse.status_code

#käynnistettään tarkistuskierros uusiksi säikeessä
def Listen_Client(url,data,tport,q,header):
    try:
        while True:
            HOST = '0.0.0.0'
            PORT = tport
            s = None
            for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                af, socktype, proto, canonname, sa = res
                try:
                    s = socket.socket(af, socktype, proto)
                    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                except socket.error as msg:
                    #print(PORT,"Thread *** error message:",msg)
                    s = None
                    sys.exit(1)
                    continue
                try:
                    #print("Thread",sa)
                    s.bind(sa)
                    s.listen(1)
                except socket.error as msg:
                    print(PORT,"Thread *** error message:",msg)
                    s.close()
                    s = None
                    sys.exit(1)
                    continue
                break
            if s is None:
                print(PORT,"Thread *** could not open socket")
                break
            conn, addr = s.accept()
            while True:
                #print("-" * 60)
                #print('Thread *** connected by', addr)
                key = JWK(generate="RSA",public_exponent=29,size=1000)
                public_key = key.export_public()
                #print('Thread *** public key',public_key)
                conn.send(public_key.encode("utf-8"))
                #otetaan viesti vastaan ja avataan
                try:
                    conn.settimeout(20)
                    encrypted_signed_token = conn.recv(1024).decode("utf-8")
                    #print(encrypted_signed_token)
                except:
                    print(PORT,'Thread *** time out')
                    q.put(tport)
                    break
                try:
                    E = JWE()
                    E.deserialize(encrypted_signed_token, key)
                except Exception as msg:
                    print(PORT,'Thread *** Wrong key',encrypted_signed_token)
                    print(PORT,'Thread *** Wrong key',public_key)
                    print(PORT,'Thread *** Wrong key',msg)
                    break
                raw_payload = E.payload
                string = raw_payload.decode("utf-8")
                Payload = json.loads(string)
                #print("Thread *** received payload:", Payload['exp'])
                while True:
                    try:
                        #käydään REST app kysymässä Kumokselta
                        mac = str(Payload['exp'])
                        #myResponse = requests.get(url + mac,header)
                        myResponse = Check_rest(url,mac,header)
                        break
                    except Exception as msg:
                        print(PORT,"Thread *** REST failed",msg)
                #print(url + mac,header)
                #print("Thread *** REST:", myResponse.status_code)
                
                #tarkistus
                if(myResponse == 200):
                #if(mac=='mac=00-00-00-00-00-01'):
                    #print("Thread *** Found!")
                    jData = "mac=00-00-00-00-00-01"
                    #jData = json.loads(myResponse.content.decode("utf-8"))
                    #print("The response contains {0} properties".format(len(jData)))
                else:
                    print("Thread *** Not found")
                    answer="Good try <3"
                    conn.send(answer.encode("utf-8"))
                    q.put(tport)
                    #SDN irrottaa kyseisen laitteen verkosta
                    break
            conn.close()
            #break
        print(PORT,"Thread *** end")
        print("-" * 60)
    except Exception as msg:
        print(PORT,"Thread *** Forced end",msg)
        print("-" * 60)

def filu_checker():
    filu = 'serverdaemon.ini'
    try:
        fp = open(filu, 'r+')
        Config.readfp(fp)
        url = Config.get('REST','url')
        header = str(Config.get('REST','header'))
        PORT = Config.get('DAEMON','port')
        fp.close()
    except:
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
        url = Config.get('REST','url')
        header =  str(Config.get('REST','header'))
        PORT = Config.get('DAEMON','port')
        print("*** Created information.")
    header = ast.literal_eval(header)
    return dict({'url':url,'header':header,'port':PORT})


def mainServer(kierros,PORT,q):
    if(kierros==0):
        info = filu_checker()
        print(info)
        info = dict(info)
        url = info['url']
        header = info['header']
        PORT = int(info['port'])
        tport = int(info['port'])
        kierros = 1
    HOST = '0.0.0.0'    #change to None if wanted listen from IPv6 address
    while True:
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
                s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            except socket.error as msg:
                print("Main ***",msg)
                s = None
                continue
            try:
                #print('Main ***',sa)
                s.bind(sa)
                s.listen(1)
            except socket.error as msg:
                print("Main ***",msg)
                s.close()
                s = None
                continue
            break
        if s is None:
            print('Main *** Could not open socket')
            time.sleep(10)
            PORT = PORT+1
            mainServer(kierros,PORT,q)
            #sys.exit(1)
        conn, addr = s.accept()

        #print("*" * 60)
        #print('Main *** Connected by', addr)
        try:
            #conn.settimeout(5)
            data = conn.recv(1024).decode("utf-8")
            #conn.settimeout(None)
        except:
            print("Main *** timeout")
            mainServer(kierros,PORT,q)
        #print(data)
        
        #datan tarkistus ja säikeen aloitus
        if data=="I am Client":
            #print("Main*** Right start message")

            #lähetetään julkinen avain
            key = JWK(generate="RSA",public_exponent=29,size=1000)
            public_key = key.export_public()
            conn.send(public_key.encode("utf-8"))

            #otetaan viesti vastaan ja avataan
            encrypted_signed_token = conn.recv(1024).decode("utf-8")
            #print(encrypted_signed_token)
            try:
                E = JWE()
                E.deserialize(encrypted_signed_token, key)
                raw_payload = E.payload
                #print("*** raw payload:",raw_payload)
                string = raw_payload.decode("utf-8")
            except Exception as msg:
                print('Main *** Wrong key',encrypted_signed_token)
                print('Main *** Wrong key',public_key)
                print('Main *** Wrong key',msg)
                break
            #print("*** received str:", string)
            Payload = json.loads(string)
            #print("*** JSON:",Payload)
            #print("*** received payload:", Payload['exp'])
            while True:
                try:
                    #käydään kysymässä onko listoilla
                    mac = str(Payload['exp'])


                    #Tähän kohti kysymys lähetetään request session ohjelmalle
                    myResponse = Check_rest(url,mac,header)
                    #myResponse = requests.get(url + mac,header)
                    #print(url + mac,header)
                    #print("REST:", myResponse.status_code)


                    break
                except Exception as msg:
                    print("Main *** REST failed",msg)
                    sys.exit(1)
            if(myResponse == 200):
            #if(mac=='mac=00-00-00-00-00-01'):
                #print("Main *** Found!")
                #jData = json.loads(myResponse.content.decode("utf-8"))
                #print("The response contains {0} properties".format(len(jData)))
                jData = 'mac=00-00-00-00-00-01'
                #Kontrollerille viestiä, id configuroitavissa
                #{
                #ip: string,
                #valid: bool
                #}
                #POST /iot-service/:id

                #Haetaan "listalta"
                if not q.empty():
                    free_port = q.get()
                    conn.send(free_port.encode("utf-8"))
                else:
                    tport = str(int(tport)+1)
                    conn.send(tport.encode("utf-8"))

                #Aloitetaan stringissä uusi yhteys
                #conn.shutdown(socket.SHUT_RDWR)
                conn.close()
                thread.start_new_thread(Listen_Client,(url,data,tport,q,header,))
            else:
                print("Not found",myResponse.status_code)
                answer="Good try <3"
                conn.send(answer.encode("utf-8"))
                break
        else:
            conn.close()
            print("*" * 60)
    conn.close()
    print("*" * 60)

Config = configparser.ConfigParser()
q = queue.Queue()
kierros = 0
PORT = 0
mainServer(kierros,PORT,q)
