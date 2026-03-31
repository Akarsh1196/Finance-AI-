import os
from authlib.integrations.requests_client import OAuth2Session

# 🔐 Load from environment
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USER_INFO = "https://www.googleapis.com/oauth2/v1/userinfo"


def get_google_auth_url():
    client = OAuth2Session(
        CLIENT_ID,
        CLIENT_SECRET,
        scope="openid email profile"
    )

    uri, state = client.create_authorization_url(
        AUTHORIZATION_ENDPOINT,
        redirect_uri="http://localhost:8501"
    )

    return uri


def fetch_user_info(code):
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET)

    token = client.fetch_token(
        TOKEN_ENDPOINT,
        code=code,
        redirect_uri="http://localhost:8501"
    )

    resp = client.get(USER_INFO)
    return resp.json()