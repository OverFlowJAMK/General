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

    def post(self):
	args = self.reqparse.parse_args()
	device = args['device']
	if len(device) == 0:
	    abort(404)
	devices.append({'device': device})	
	return {'success':'true'}

    def delete(self):
	args = self.reqparse.parse_args()
	device = args['device']
	if len(device) == 0:
	    abort(404)
	devices.remove({'device': device})
	return {'success':'true'}

api.add_resource(DeviceList, '/network/api/v0.1/devices', endpoint='devices')
api.add_resource(Device, '/network/api/v0.1/device', endpoint='device')

if __name__ == '__main__':
    app.run(debug=True)


