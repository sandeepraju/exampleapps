# Python standard imports
import os

# Third party imports
import redis
from flask import Flask, render_template, jsonify, send_from_directory

# Local imports
from twofactor import PlivoTwoFactorAuth


app = Flask(__name__)
app.config.from_object("settings")  # Load configurations from settings.py

# Redis configuration
redis_url = os.getenv('REDISTOGO_URL', app.config["APPLICATION_REDIS_URI"])
r = redis.from_url(redis_url)

# Plivo two factor authentication configuration
p2fa = PlivoTwoFactorAuth({
			"auth_id": app.config["PLIVO_AUTH_ID"],
			"auth_token": app.config["PLIVO_AUTH_TOKEN"]
		}, appNumber=app.config["PLIVO_NUMBER"])


# Applicattion landing page
@app.route("/")
def index():
	""" index() renders the landing page of
		the application.
	"""
	return render_template("index.html")


# Number verification initiation
@app.route("/verify/<number>")
def verify(number):
	""" verify(number) accepts a number
		and initiates verification for it.
	"""
	code = p2fa.getVerificationCode(number, "Your verification code is __code__")  # String should be less than 160 chars
	r.setex("number:%s:code" % number, code, 60*15)  # Verification code is valid for 15 mins
	return jsonify({"status": "success", "message": "verification initiated"})


# Code validation endpoint
@app.route("/checkcode/<number>/<code>")
def checkCode(number, code):
	""" checkCode(number, code) accepts a number 
		and the code entered by the user and tells 
		if the code entered for that number is correct or not
	"""
	originalCode =  r.get("number:%s:code" % number)
	if originalCode:  # checks if code expired
		if originalCode == code:
			r.delete("number:%s:code" % number)  # verification successful, delete the code
			return jsonify({"status": "success", "message": "codes match! number verified"})
		else:
			return jsonify({"status": "failure", "message": "codes do not match! number not verified"})
	else:
		return jsonify({"status": "failure", "message": "number not found!"})


# Application error handlers
@app.errorhandler(404)
def not_found(error=None):
    return render_template("404.html"), 404


# Etc routes (favicon, robots.txt, humans.txt, etc.)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')


@app.route('/humans.txt')
def humans():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'humans.txt', mimetype='text/plain')


if __name__ == "__main__":
	app.run()