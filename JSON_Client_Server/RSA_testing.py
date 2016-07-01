import time
import json
from jwcrypto.common import json_decode
from jwcrypto.common import json_encode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT

PAYLOAD = json.dumps({'username': "Hello", 'password': "world"})
print(PAYLOAD)
key = JWK(generate="RSA",public_exponent=29,size=1000) #public_exponent pitää olla alkuluku (e)
print(key.export())
#Koko avain {"q":"Second Prime Factor","p":"First Prime Factor","dq":"Second Factor CRT Exponent","dp":"First Factor CRT Exponent","qi":"First CRT Coefficient","d":"Private Exponent","kty":"key type","n":"public_Modulus","e":"public_exponent"}
p_key = key.get_op_key(operation=None, arg=None)
print(key.export_public())
# https://github.com/latchset/jwcrypto/blob/master/jwcrypto/jwk.py
# http://jwcrypto.readthedocs.io/en/stable/jwk.html
#Julkinen avain {"e":"public_exponent","kty":"key type","n":"public_Modulus"}

claims = dict(exp=PAYLOAD) #salattava tieto
header = dict(alg="RSA-OAEP-256", enc="A128GCM")
T = JWT(header, claims)
T.make_encrypted_token(key)
T.serialize(compact=True)
encrypted_signed_token = T.serialize(compact=True)
print(encrypted_signed_token)

testing_token = JWT(jwt=encrypted_signed_token).token

testing_token.decrypt(p_key)
raw_payload = testing_token.payload
print(raw_payload)

payload = raw_payload.decode("utf-8")
print(payload)

E = JWE()
E.deserialize(encrypted_signed_token, key=key)
raw_payload = E.payload
print(raw_payload)

string = raw_payload.decode("utf-8")
print("received str:", string)
Payload = json.loads(string)
print(Payload)
print("received payload:", Payload['exp'])
