<h1>ServerClientDaemon</h1>

<h2>Device requirement</h2>

<h3>Server:</h3>

||version|
|---|---|
| Linux Ubuntu | 16.04 |
| Python | 3.5.2 |
| jsonschema| 2.7.0 |
| cryptography | 1.4 |
| configparser | 3.5.0 |
| requests | 2.7.0 |
| queuelib | 1.4.2 |
| websocket-client | 0.37.0 |
| JWCrypto ||
| ast ||
| codecs ||
| _thread ||

<h3>Client:</h3>

||version|
|---|---|
| Python | 3.5.2 |
| jsonschema| 2.7.0 |
| cryptography | 1.4 |
| configparser | 3.5.0 |
| websocket-client | 0.37.0 |
| JWCrypto ||
| codecs ||

<h2>Installation</h2>
* Download Server or Client zip file from the official site depending witch one your machine will be
* Unzip
* Run the requirements.txt script
* Run the server.py/client.py script with python 3.5

<h2>Setting Server computer</h2>
You can easily change your Server's settings by changing information in server.ini file.

* url is for baasbox address
* header is baasbox's header
* port is the main port of server, which is start number of ports

<h2>Setting Client machine</h2>

<h3>Client.ini</h3>

* Check Server computer's ip address and write it down to "address"
* Port is the main port of server, which is start number of ports
* under KaMu write right mac address

<h3>ServerAddress.ini</h3>

* Check Server computer's ip address and write it down to "address"
* Port is the main port of server, which is start number of ports
