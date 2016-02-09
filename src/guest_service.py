from flask import Flask, request, jsonify
import os

from common.config_manager import get_logging_handler, get_logger, is_local_or_dev_environment
from common.helper import get_consul_server

import guest_base

app = Flask(__name__)

consul_server = get_consul_server()
logger = get_logger(consul_server)

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": True, "msg": "Unknown error occured on server."}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": True, "msg": "Resource not found."}), 404

@app.route("/signup", methods = ["POST"])
def signup():

	data = request.get_json(force=False, silent=True)
	if not data:
		return jsonify({"error": True, "msg": "Request was not understood"}), 500	
	
	user_struct, status_code = guest_base.signup(data)

	return jsonify(user_struct), status_code


@app.route("/login", methods = ["POST"])
def login():
	
	data = request.get_json(force=False, silent=True)

	ret_msg, status_code = guest_base.login(data)

	return jsonify(ret_msg), status_code

@app.route("/resetpassword", methods = ["POST"])
def reset_password():
	
	data = request.get_json(force=False, silent=True)
	if not data:
		return jsonify({"error": True, "msg": "Request was not understood"}), 500
	
	item, status_code = guest_base.reset_password(data)

	return jsonify(item), status_code

# if __name__ == "__main__":
# 	app.logger.addHandler(get_logging_handler(consul_server))
# 	if is_local_or_dev_environment(consul_server):
# 		app.run(debug=True,host='0.0.0.0')
# 	else:
# 		app.run(debug=False,host='0.0.0.0')