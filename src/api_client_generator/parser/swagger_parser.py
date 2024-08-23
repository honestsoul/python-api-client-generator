# api_client_generator/parser/swagger_parser.py

import json
from typing import Dict, Any
import requests

class SwaggerParser:
    def __init__(self, spec_url: str):
        self.spec_url = spec_url
        self.spec_data: Dict[str, Any] = {}

    def load_spec(self) -> None:
        response = requests.get(self.spec_url)
        response.raise_for_status()
        self.spec_data = response.json()

    def parse_endpoints(self) -> Dict[str, Dict[str, Any]]:
        endpoints = {}
        paths = self.spec_data.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                endpoint_id = f"{method.upper()}_{path}"
                endpoints[endpoint_id] = {
                    'path': path,
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'parameters': details.get('parameters', []),
                    'responses': details.get('responses', {})
                }
        return endpoints

    def parse_definitions(self) -> Dict[str, Dict[str, Any]]:
        return self.spec_data.get('definitions', {})

    def parse_security_definitions(self) -> Dict[str, Dict[str, Any]]:
        return self.spec_data.get('securityDefinitions', {})

    def parse(self) -> Dict[str, Any]:
        self.load_spec()
        return {
            'info': self.spec_data.get('info', {}),
            'endpoints': self.parse_endpoints(),
            'definitions': self.parse_definitions(),
            'security_definitions': self.parse_security_definitions()
        }