import requests

url = 'http://localhost:9000/plugin/instapp.enabled?'
header = { 'X-BAASBOX-APPCODE': 1234567890 }
mac = 'mac=00-00-00-00-00-01'

s = requests.Session()
myResponse = requests.get(url + mac,header)
print('*** ',myResponse.status_code)

myResponse = s.get(url=url+mac, headers=header)
print('*** ',myResponse.status_code)
