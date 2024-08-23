# api_client_generator/authentication/openid_connect_handler.py

import requests
from typing import Dict, Any
from jose import jwt
from jose.exceptions import JWTError
import time

class OpenIDConnectHandler:
    def __init__(self, issuer_url: str, client_id: str, client_secret: str):
        self.issuer_url = issuer_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
        self._load_configuration()

    def _load_configuration(self) -> None:
        well_known_url = f"{self.issuer_url}/.well-known/openid-configuration"
        response = requests.get(well_known_url)
        response.raise_for_status()
        self.config = response.json()

    def get_token(self) -> str:
        if not self.token or self._is_token_expired():
            self._refresh_token()
        return self.token['access_token']

    def _refresh_token(self) -> None:
        token_endpoint = self.config['token_endpoint']
        response = requests.post(
            token_endpoint,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
        )
        response.raise_for_status()
        self.token = response.json()

    def _is_token_expired(self) -> bool:
        if 'expires_at' not in self.token:
            return True
        return time.time() > self.token['expires_at']

    def get_auth_header(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.get_token()}'}

    def validate_id_token(self, id_token: str) -> Dict[str, Any]:
        jwks_uri = self.config['jwks_uri']
        jwks_response = requests.get(jwks_uri)
        jwks_response.raise_for_status()
        jwks = jwks_response.json()

        try:
            header = jwt.get_unverified_header(id_token)
            key = next((key for key in jwks['keys'] if key['kid'] == header['kid']), None)
            if not key:
                raise ValueError("Signing key not found")

            claims = jwt.decode(
                id_token,
                key,
                algorithms=['RS256'],
                audience=self.client_id,
                issuer=self.issuer_url
            )
            return claims
        except JWTError as e:
            raise ValueError(f"Invalid ID token: {str(e)}")

# Usage:
# oidc_handler = OpenIDConnectHandler('https://accounts.example.com', 'your-client-id', 'your-client-secret')
# auth_header = oidc_handler.get_auth_header()
# # Use auth_header in your API requests
#
# # If you receive an ID token and want to validate it:
# id_token = "received_id_token"
# try:
#     claims = oidc_handler.validate_id_token(id_token)
#     print(f"Validated claims: {claims}")
# except ValueError as e:
#     print(f"Token validation failed: {str(e)}")