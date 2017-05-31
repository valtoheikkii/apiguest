from flask import Flask, request, jsonify
import os

from common.config_manager import get_logging_handler, is_local_or_dev_environment
from common.helper import get_consul_server

import guest_base
from common.log_writer import *
import common.services_helper
import json

app = Flask(__name__)

consul_server = get_consul_server()
logger = get_logger("guest-service")

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": True, "msg": "Unknown error occured on server."}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": True, "msg": "Resource not found."}), 404

@app.route("/signup", methods = ["POST"])
def signup():
	try:

		data = request.get_json(force=False, silent=True)
		if not data:
			return jsonify({"error": True, "msg": "Request was not understood"}), 500	
		
		user_struct, status_code = guest_base.signup(data)

		return jsonify(user_struct), status_code

	except Exception as e:
		error(logger, e)


@app.route("/login", methods = ["POST"])
def login():
	try:

		data = request.get_json(force=False, silent=True)

		ret_msg, status_code = guest_base.login(data)

		return jsonify(ret_msg), status_code

	except Exception as e:
		error(logger, e)

@app.route("/resetpassword", methods = ["POST"])
def reset_password():
	try:

		data = request.get_json(force=False, silent=True)
		if not data:
			return jsonify({"error": True, "msg": "Request was not understood"}), 500
		
		item, status_code = guest_base.reset_password(data)

		return jsonify(item), status_code

	except Exception as e:
		error(logger, e)

@app.route("/clientIds", methods = ["GET"])
def get_client_ids():
	try:

		clients = common.services_helper.get_all_clients()
		client_ids=[]

		for client in clients:
			client_ids.append(client["EntityID"])			

		return json.dumps(client_ids), 200

	except Exception as e:
		error(logger, e)

if __name__ == "__main__":
	app.logger.addHandler(get_logging_handler(consul_server))
	if is_local_or_dev_environment(consul_server):
		app.run(debug=True,host='0.0.0.0')
	else:
		app.run(debug=False,host='0.0.0.0')