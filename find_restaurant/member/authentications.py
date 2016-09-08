import json
from flask import g
from find_restaurant.member.views import dbsession
from find_restaurant.member.models import User
from oauth2client import client
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from itsdangerous import URLSafeSerializer
from config import SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

auth = HTTPTokenAuth()
s = URLSafeSerializer(SECRET_KEY)


def verify_token(token):
    user_id = User.verify_auth_token(token)
    if user_id:
        user = dbsession.query(User).filter_by(id=user_id).one()
        if not user:
            return False
        g.user = user
    return True


def google_login(auth_code):
    try:
        oauth_flow = client.OAuth2WebServerFlow(
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scope='profile email',
            redirect_uri='http://localhost:5000/dashboard')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except client.FlowExchangeError:
        return json.dumps({'error': 'Failed to upgrade the authorization code.'})
    access_token = credentials.access_token
    return access_token

