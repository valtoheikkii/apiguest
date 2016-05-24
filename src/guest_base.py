from flask import request
import os
import requests
from common.config_manager import discover_service
from common.helper import base64_encode, get_consul_server
import json
from validate_email import validate_email
from common.log_writer import *

consul_server = get_consul_server()
logger = get_logger("guest-base")

def signup(data):
	if "email" not in data:
		return {"error": True, "msg": "Email not provided"}, 404
	if not validate_email(data['email']):
		return {"error": True, "msg": "Supplied value is not an email"}, 404

	if "OrganizationName" not in data:
		return {"error": True, "msg": "OrganizationName not provided"}, 404
	debug(logger,"calling user create...")
	#Sign up users are created as System Administrators	
	ret_msg, status_code = get_service_response("create", {"Email": data["email"], "OrganizationName": data["OrganizationName"], "PermissionLevel":0})
	if status_code != 201:
		return ret_msg, status_code

	# user_id = ret_msg["EntityID"]
	# user_struct = ret_msg
	# pwd = ret_msg["HashedPassword"]
	# token = base64_encode(ret_msg["Email"] + ":" + pwd)
	# user_struct["AuthToken"] = token
	# final_header["User-Id"] = user_id	

	return {"Status": "success"}, 201

def login(data):
	if not data:
		return {"error": True, "msg": "Request was not understood"}, 500
	if not "username" in data:
		return {"error": True, "msg": "Username/Password is wrong"}, 401
	if not "password" in data:
		return {"error": True, "msg": "Username/Password is wrong"}, 401
		
	ret_msg, status_code = get_service_response("login", data)

	if "HashedPassword" not in ret_msg:
		return {}, status_code

	pwd = ret_msg["HashedPassword"]
	token = base64_encode(data["username"].lower() + ":" + pwd)
	ret_msg.pop("HashedPassword")
	ret_msg["AuthToken"] = token

	return ret_msg, 200

def reset_password(data):
	if "Email" not in data:
		return {"error": True, "msg": "Cannot perform action. No Email"}, 401

	ret_msg, status_code = get_service_response("resetpassword", data)

	item = {}
	item["Status"] = ret_msg["Status"]

	return item, status_code

def get_service_response(service_name, data):
	request_headers = {}
	for k, v in request.headers.items():
		request_headers[k] = v
	send_data = json.dumps(data)
	final_header = {}
	final_header["User-Agent"] = request_headers["User-Agent"]

	if "Content-Type" in request_headers:
		final_header["Content-Type"] = request_headers["Content-Type"]
	else:
		final_header["Content-Type"] = "application/json"

	ret = discover_service(consul_server, "user-account")
	service_addr= ret[0]["Address"]
	service_port = ret[0]["ServicePort"]
	user_service = "http://" + service_addr + ":" + str(service_port) + "/"+service_name
	r = requests.post(user_service, data=send_data, headers=final_header)
	
	return r.json(), r.status_code