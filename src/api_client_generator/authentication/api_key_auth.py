# api_client_generator/authentication/api_key_auth.py

from typing import Dict
from requests.auth import AuthBase

class APIKeyAuth(AuthBase):
    def __init__(self, api_key: str, param_name: str, location: str = 'header'):
        self.api_key = api_key
        self.param_name = param_name
        self.location = location

    def __call__(self, r):
        if self.location == 'header':
            r.headers[self.param_name] = self.api_key
        elif self.location == 'query':
            r.prepare_url(r.url, {self.param_name: self.api_key})
        return r

    def get_auth_header(self) -> Dict[str, str]:
        if self.location == 'header':
            return {self.param_name: self.api_key}
        return {}

# Usage:
# auth = APIKeyAuth('your-api-key', 'X-API-Key', 'header')
# requests.get('https://api.example.com/endpoint', auth=auth)
# 
# # Or if you need just the header:
# headers = auth.get_auth_header()
# requests.get('https://api.example.com/endpoint', headers=headers)