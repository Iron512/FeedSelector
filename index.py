from flask import Flask, request, session, redirect, url_for

import json
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
	if 'user_id' in session:
		if session['user_id'] == -1:
			return "Bad request. Short lived access token not retrieved"
		else:
			#logged correctly
			url_get_user = "https://graph.instagram.com/"+str(session['user_id'])
			url_get_user = url_get_user+"?fields=username&access_token="+session['access_token']

			response_user = requests.get(url_get_user)
			response_user_json = json.loads(response_user.text)

			return "Welcome back," + response_user_json["username"]
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
	response_token_json = json.loads(response_token.text) #probably could have been done better

	if "error_type" not in response_token_json:
		#everything ok
		session['access_token'] = response_token_json["access_token"]
		session['user_id'] = response_token_json["user_id"]
	else: 
		#something went wrong
		session['user_id'] = -1

	return redirect(url_for("serve"))

if __name__ == '__main__':
	task.run()

