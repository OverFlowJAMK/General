from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
api = Api(app)

devices = [
    {
	'device': '00:00:00:00:00:01'
    }
]

device_marshal = {
    'device': fields.String
}

class DeviceList(Resource):
    
    def __init__(self):
	self.reqparse = reqparse.RequestParser()
	super(DeviceList, self).__init__()
    
    def get(self):
	return {'devices': [marshal(device, device_marshal) for device in devices]}

class Device(Resource):

    def __init__(self):
	self.reqparse = reqparse.RequestParser()
	self.reqparse.add_argument('device', type=str, required=True, help='No device provided', location='json')

    def get(self):
	args = self.reqparse.parse_args()
	device = args['device']
	# Check if parameter is empty
	if len(device) == 0:
	    abort(404)
	# Check if device is allowed
	for element in devices:
	    if element['device'] == device:
	   	 return {'device allowed':'true'}
	return {'device allowed':'false'}

    def post(self):
	args = self.reqparse.parse_args()
	device = args['device']
	# Check if parameter is empty
	if len(device) == 0:
	    abort(404)
	# Check if device is allowed
	for element in devices:
	    if element['device'] == device:
		return {'result': [{'success':'false', 'details':'device already allowed'}]}
	devices.append({'device': device})	
	return {'success':'true'}

    def delete(self):
	args = self.reqparse.parse_args()
	device = args['device']
	# Check if parameter is empty
	if len(device) == 0:
	    abort(404)
	# Check if device is allowed
	for element in devices:
	    if element['device'] == device:
		# Remove device from allowed list
		devices.remove({'device': device})
		return {'success':'true'}
	return {'result': [{'success':'false', 'details':'no such device in allowed list'}]}

api.add_resource(DeviceList, '/network/api/v0.1/devices', endpoint='devices')
api.add_resource(Device, '/network/api/v0.1/device', endpoint='device')

if __name__ == '__main__':
    app.run(debug=True)


