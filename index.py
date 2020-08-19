from flask import Flask, request, session, redirect, url_for
import requests
import os

task = Flask(__name__)

#os variables
application_id = str(os.environ.get('APPLICATION_ID'))
application_home = str(os.environ.get('APPLICATION_HOME'))
instagram_app_secret = str(os.environ.get('INSTAGRAM_APP_SECRET'))
session_secret_key = str(os.environ.get('SESSION_SECRET_KEY'))

task.secret_key = session_secret_key

@task.route('/')
def serve():
	

	if 'username' in session:
		return "z"
	else:
		#if no username is logged go to application login
		auth_url = "https://api.instagram.com/oauth/authorize?client_id="
		auth_url = auth_url + str(application_id) + "&redirect_uri="
		auth_url = auth_url + str(application_home) + "auth/&scope=user_profile,user_media&response_type=code"

		return redirect(auth_url)
	
@task.route('/auth/', methods=['GET'])
def auth():
	if request.args.get('code') == None:
		return "This area is forbidden without a code"

	redirect_for_token = str(application_home) + "auth/"
	params = {
		"client_id":application_id,
		"client_secret":instagram_app_secret,
		"grant_type":"authorization_code",
		"redirect_uri":redirect_for_token,
		"code":request.args.get('code')
	}

	#ask for the short timed user auth
	response_token = requests.post("https://api.instagram.com/oauth/access_token", data=params)
	return response_token.text

	if 'username' not in session:
		#procede with login
		return "y"

@task.route('/authtoken/', methods=["POST"])
def authtoken():
	return request.form

if __name__ == '__main__':
	task.run()

