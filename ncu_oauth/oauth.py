
#-*- encoding: UTF-8 -*-

import requests
from flask import redirect, session

OAUTH_URL = 'https://portal.ncu.edu.tw'

class Oauth():
	def __init__(self, redirect_uri, client_id, client_secret):
		self.grant_type = 'authorization_code'
		self.code = None
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri

	def authorize(self):
		get_code_url = OAUTH_URL + '/oauth2/authorization?response_type=code&scope=identifier+chinese-name&client_id='+self.client_id+'&redirect_uri='+self.redirect_uri
		return redirect(get_code_url)

	def get_token(self,code):
		self.code = code
		get_token_url = OAUTH_URL + '/oauth2/token'
		headers = {
			'Accept': 'application/json',
			'grant_type': 'authorization_code',
			'code': self.code,
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'redirect_uri': self.redirect_uri,
		}
		access_token = requests.post(get_token_url, data=headers).json().get('access_token', None)
		if access_token:
			session['ncu_token'] = access_token
			session['logged_in'] = True
			return True

		return False

	def get_profile(self):
		token = session.get('ncu_token')
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(token)
		}
		get_profile_url = OAUTH_URL + '/apis/oauth/v1/info'

		data = requests.get(get_profile_url,headers=headers).json()
		print(data)
		return data
