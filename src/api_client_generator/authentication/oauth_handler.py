# api_client_generator/authentication/oauth_handler.py

import requests
from typing import Dict, Any

class OAuthHandler:
    def __init__(self, token_url: str, client_id: str, client_secret: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Dict[str, Any] = {}

    def get_token(self) -> str:
        if not self.token or self._is_token_expired():
            self._refresh_token()
        return self.token['access_token']

    def _refresh_token(self) -> None:
        response = requests.post(
            self.token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
        )
        response.raise_for_status()
        self.token = response.json()

    def _is_token_expired(self) -> bool:
        # Implement token expiration check
        # This will depend on how the API provides expiration information
        pass

    def get_auth_header(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.get_token()}'}