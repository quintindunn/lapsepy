"""
Author: Quintin Dunn
Date: 10/22/23
"""
import requests
from lapsepy.journal.common.exceptions import AuthTokenError

REFRESH_URL = "https://auth.production.journal-api.lapse.app/refresh"


def refresh(refresh_token: str):
    """
    Sends API call to auth.production.journal-api.lapse.app/refresh to refresh your auth token.
    :param refresh_token: Token gotten from Lapse to refresh your access token.
    :return:
    """
    request = requests.post(REFRESH_URL, json={"refreshToken": refresh_token})
    if request.status_code != 200:
        raise AuthTokenError("Invalid refresh token")

    access_token = request.json().get("accessToken")

    return access_token
