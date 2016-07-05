from jwcrypto.common import json_decode, json_encode
from jwcrypto import jwk
from jwcrypto import jws
from jwcrypto import jwe
from jwcrypto import jwt
import json

key = jwk.JWK(generate="RSA",public_exponent=29,size=1000)

print(key.export())

P = dict(json.loads(key.export_public()))
print(P)

P_key = jwk.JWK(**P)

PAYLOAD = json.dumps({'username': "Hello", 'password': "world"})
claims = dict(exp=PAYLOAD)
header = dict(alg="RSA-OAEP-256", enc="A128GCM")
T = jwt.JWT(header, claims)

T.make_encrypted_token(P_key)

T.serialize(compact=True)
encrypted_signed_token = T.serialize(compact=True)
print("*** engrypted signed token:",encrypted_signed_token)

E = jwe.JWE()
E.deserialize(encrypted_signed_token, key=key)

raw_payload = E.payload
print("*** raw payload:",raw_payload)

string = raw_payload.decode("utf-8")
print("*** received str:", string)
Payload = json.loads(string)
print("*** JSON:",Payload)
print("*** received payload:", Payload['exp'])


            
