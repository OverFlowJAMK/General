# Server program
import socket
import sys
import codecs
import time
import json
import requests
from jwcrypto.common import json_decode
from jwcrypto.common import json_encode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT

def RSA_key():
    key = JWK(generate="RSA",public_exponent=29,size=1000) #public_exponent pitää olla alkuluku (e)
    return key
try:
    while True:
        HOST = '0.0.0.0'    #change to None if wanted listen from IPv6 address
        PORT = 55535
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
        data = conn.recv(1024).decode("utf-8")
        print(data)
        #datan tarkistus
        if data=="I am Client":
            print("*** Right start message")
            while True:
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
                url = 'http://82.196.14.4:9000/plugin/instapp.enabled?'
                data =  { 'X-BAASBOX-APPCODE': 1234567890 }

                myResponse = requests.get(url + mac,data)
                print("REST:", myResponse.status_code)
                if(myResponse.ok):
                    print("Found!")
                    jData = json.loads(myResponse.content.decode("utf-8"))
                    print("The response contains {0} properties".format(len(jData)))
                    
                    #No jos se client on listalla niin se SDN-kontrolleri vaan lisää sen sensorin siihen samaan vlaniin
                    #missä se kaa ja baasbox on. Se controllerin toteutus on mulla ihan vähän vielä vaiheessa,
                    #mutta saan sen varmaan sellaseksi, että sitä vois alkaa testaileen niin vielä tällä viikolla
                    
                    
                else:
                    print("Not found")
                    answer="Good try <3"
                    conn.send(answer.encode("utf-8"))
                    conn.close()
                    break
            else:
                conn.close()
                
except KeyboardInterrupt:
    print("pressed Ctrl+C")
    conn.close()
    sys.exit()
