import hashlib

from datetime import datetime
from pytz import timezone
from urllib.parse import urlencode

from digilocker.constants import AUTH_ENDPOINT, ACCESS_TOKEN_URL, ACCOUNT_VERIFY
from digilocker.connection import Connection


class Digilocker(object):
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.connection = Connection()

    def get_authorization_url(self, mobile_number, state):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "state": urlencode(state),
            "verified_mobile": mobile_number
        }
        return "{}?{}".format(AUTH_ENDPOINT, urlencode(params))

    def get_access_token(self, code):
        request_body = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        response = self.connection.make_request(ACCESS_TOKEN_URL, "POST", data=request_body)
        response_json = response.json()
        return response_json

    def get_refresh_token(self, refresh_token):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        request_body = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = self.connection.make_request(ACCESS_TOKEN_URL, "POST", data=request_body, headers=headers)
        response_json = response.json()
        return response_json

    def account_exists(self, mobile_number):
        timestamp = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata')).strftime('%s')
        app_hash = hashlib.sha256(
            "{}{}{}{}".format(self.client_secret, self.client_id, mobile_number, timestamp)
        ).hexdigest()
        request_body = {
            "mobile": mobile_number,
            "hmac": app_hash,
            "ts": timestamp,
            "clientid": self.client_id
        }
        response = self.connection.make_request(ACCOUNT_VERIFY, "POST", request_body)
        return response.json()
