from flask import Flask, request, session, redirect, url_for
from privates import *

task = Flask(__name__)
task.secret_key = session_secret_key

@task.route('/')
def serve():
	if 'username' in session:
		#return "Ciao, flask! Il valore è " + session['value']
		return "z"
	else:
		#if no username is logged go to application login
		auth_url = "https://api.instagram.com/oauth/authorize?client_id="
		auth_url = auth_url + str(application_id) + "&redirect_uri="
		auth_url = auth_url + str(home) + "auth/&scope=user_profile,user_media&response_type=code"

		#return redirect(auth_url)
		return auth_url

@task.route('/set/<val>', methods=['GET'])
def set_val(val):
	session['value'] = val
	return redirect(url_for('serve'))

@task.route('/auth/<code>')
def auth(code):
	return code
	if 'username' not in session:
		#procede with login
		return "y"

if __name__ == '__main__':
	task.run()