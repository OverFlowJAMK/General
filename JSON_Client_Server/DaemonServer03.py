# Server program
import socket
import sys
import codecs
import time
import json
import requests
import queue
import _thread as thread
from jwcrypto.common import json_decode
from jwcrypto.common import json_encode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT

class Fifo_queue:
    q=queue.Queue()
    
    def __init__(self,task,ip_number):
        self.q = q
        if task=='save_ip':
            q.put(ip_number)
        if task=='get_ip':
            if q.empty() == False:
                return q.get()
            else:
                return None
        
    
def RSA_key():
    key = JWK(generate="RSA",public_exponent=29,size=1000) #public_exponent pitää olla alkuluku (e)
    return key

#käynnistettään tarkistuskierros uusiksi
def Listen_Client(address,tport,q):
    try:
        while True:
            HOST = '0.0.0.0'
            PORT = tport
            s = None
            while True:
                for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                    af, socktype, proto, canonname, sa = res
                    try:
                        s = socket.socket(af, socktype, proto)
                    except socket.error as msg:
                        s = None
                        continue
                    try:
                        print("Thread",sa)
                        s.bind(sa)
                        s.listen(1)
                    except socket.error as msg:
                        s.close()
                        s = None
                        continue
                    break
                if s is None:
                    print('could not open socket')
                    break
                conn, addr = s.accept()
                if address == addr[0]:
                    while True:
                        print("-" * 60)
                        print('Thread *** connected by', addr)
                        key = RSA_key()
                        public_key = key.export_public()
                        print('Thread *** public key',public_key)
                        conn.send(public_key.encode("utf-8"))
                        #otetaan viesti vastaan ja avataan
                        try:
                            conn.settimeout(20)
                            encrypted_signed_token = conn.recv(1024).decode("utf-8")
                            print(encrypted_signed_token)
                        except:
                            print('Thread *** time out')
                            break
                        E = JWE()
                        E.deserialize(encrypted_signed_token, key)
                        raw_payload = E.payload
                        print("Thread *** raw payload:",raw_payload)
                        string = raw_payload.decode("utf-8")
                        print("Thread *** received str:", string)
                        Payload = json.loads(string)
                        print("Thread *** JSON:",Payload)
                        print("Thread *** received payload:", Payload['exp'])
                        #käydään REST app kysymässä Kumokselta
                        mac = str(Payload['exp'])
                        url = 'http://82.196.14.4:9000/plugin/instapp.enabled?'
                        data =  { 'X-BAASBOX-APPCODE': 1234567890 }
                        myResponse = requests.get(url + mac,data)
                        print("Thread *** REST:", myResponse.status_code)
                        #tarkistus
                        if(myResponse.ok):
                            print("Found!")
                            jData = json.loads(myResponse.content.decode("utf-8"))
                            print("The response contains {0} properties".format(len(jData)))
                        else:
                            print("Not found")
                            answer="Good try <3"
                            conn.send(answer.encode("utf-8"))
                            #SDN irrottaa kyseisen laitteen verkosta
                            
                            
                            break
                    conn.close()
                    break
            break
        q.put(tport)

        
        print("Thread *** end")
        print("-" * 60)
    except:
        q.put(tport)
        print("Thread *** Forced end")
        print("-" * 60)

q=queue.Queue()
tport = 55535
url = 'http://82.196.14.4:9000/plugin/instapp.enabled?'
header =  { 'X-BAASBOX-APPCODE': 1234567890 }
while True:
    HOST = '0.0.0.0'    #change to None if wanted listen from IPv6 address
    PORT = 55535
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            print("Main",sa)
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

    print("-" * 60)
    print('Main connected by', addr)
    data = conn.recv(1024).decode("utf-8")
    print(data)
    #datan tarkistus ja säikeen aloitus
    if data=="I am Client":
        print("*** Right start message")

        #lähetetään julkinen avain
        key = RSA_key()
        public_key = key.export_public()
        conn.send(public_key.encode("utf-8"))

        #otetaan viesti vastaan ja avataan
        encrypted_signed_token = conn.recv(1024).decode("utf-8")
        print(encrypted_signed_token)

        E = JWE()
        E.deserialize(encrypted_signed_token, key)
        raw_payload = E.payload
        print("*** raw payload:",raw_payload)
        string = raw_payload.decode("utf-8")
        print("*** received str:", string)
        Payload = json.loads(string)
        print("*** JSON:",Payload)
        print("*** received payload:", Payload['exp'])

        #käydään REST app kysymässä Kumokselta

        mac = str(Payload['exp'])

        myResponse = requests.get(url + mac,header)
        print(url + mac,header)
        print("REST:", myResponse.status_code)
        if(myResponse.ok):
            print("Found!")
            jData = json.loads(myResponse.content.decode("utf-8"))
            print("The response contains {0} properties".format(len(jData)))
            
            #No jos se client on listalla niin se SDN-kontrolleri vaan lisää sen sensorin siihen samaan vlaniin
            #missä se kaa ja baasbox on. Se controllerin toteutus on mulla ihan vähän vielä vaiheessa,
            #mutta saan sen varmaan sellaseksi, että sitä vois alkaa testaileen niin vielä tällä viikolla
            address = addr[0]
            print(address)
            
            #tässä vaiheessa pitäisi tallentaa "listalle"
            #free_port = Fifo_queue('get_ip',0)
            #print(free_port)
            #if free_port==None:
            #    tport = str(int(tport)+1)
            #    conn.send(tport.encode("utf-8"))
            #else:
            #    conn.send(free_port.encode("utf-8"))
            if q.empty() == False:
                free_port = q.get()
                conn.send(free_port.encode("utf-8"))
            else:
                tport = str(int(tport)+1)
                conn.send(tport.encode("utf-8"))

            #Aloitetaan stringissä uusi yhteys
            thread.start_new_thread(Listen_Client,(address, tport, q,))
            time.sleep(5)
        else:
            print("Not found")
            answer="Good try <3"
            conn.send(answer.encode("utf-8"))
        conn.close()
        print("-" * 60)
    else:
        conn.close()
        print("-" * 60)

conn.close()
print("-" * 60)
