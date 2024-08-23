# api_client_generator/authentication/auth_handler.py

from typing import Dict, Any
from .api_key_auth import APIKeyAuth
from .oauth_handler import OAuthHandler
from .openid_connect_handler import OpenIDConnectHandler

class AuthHandler:
    def __init__(self, security_schemes: Dict[str, Any]):
        self.security_schemes = security_schemes
        self.auth_methods = {}

    def setup_auth(self, scheme_name: str, **kwargs) -> None:
        scheme = self.security_schemes.get(scheme_name)
        if not scheme:
            raise ValueError(f"Unknown security scheme: {scheme_name}")

        if scheme['type'] == 'apiKey':
            self.auth_methods[scheme_name] = APIKeyAuth(
                kwargs['api_key'],
                scheme['name'],
                scheme['in']
            )
        elif scheme['type'] == 'oauth2':
            self.auth_methods[scheme_name] = OAuthHandler(
                kwargs['token_url'],
                kwargs['client_id'],
                kwargs['client_secret']
            )
        elif scheme['type'] == 'openIdConnect':
            self.auth_methods[scheme_name] = OpenIDConnectHandler(
                kwargs['issuer_url'],
                kwargs['client_id'],
                kwargs['client_secret']
            )
        else:
            raise ValueError(f"Unsupported auth type: {scheme['type']}")

    def get_auth(self, scheme_name: str) -> Any:
        auth = self.auth_methods.get(scheme_name)
        if not auth:
            raise ValueError(f"Auth not set up for scheme: {scheme_name}")
        return auth

    def get_auth_header(self, scheme_name: str) -> Dict[str, str]:
        auth = self.get_auth(scheme_name)
        if hasattr(auth, 'get_auth_header'):
            return auth.get_auth_header()
        raise ValueError(f"Auth method {scheme_name} does not support get_auth_header")

# Usage:
# auth_handler = AuthHandler(security_schemes)
# auth_handler.setup_auth('api_key', api_key='your-api-key')
# auth_handler.setup_auth('oauth2', token_url='https://example.com/oauth/token', client_id='your-client-id', client_secret='your-client-secret')
# auth_handler.setup_auth('oidc', issuer_url='https://accounts.example.com', client_id='your-client-id', client_secret='your-client-secret')
# auth_header = auth_handler.get_auth_header('api_key')