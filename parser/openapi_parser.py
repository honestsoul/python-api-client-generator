# api_client_generator/parser/openapi_parser.py

import json
from typing import Dict, Any, List
import requests
import jsonschema

class OpenAPI310Parser:
    def __init__(self, spec_url: str):
        self.spec_url = spec_url
        self.spec_data: Dict[str, Any] = {}

    def load_spec(self) -> None:
        response = requests.get(self.spec_url)
        response.raise_for_status()
        self.spec_data = response.json()
        self._validate_spec()

    def _validate_spec(self) -> None:
        # You would need to download and use the official OpenAPI 3.1.0 JSON Schema
        # This is a placeholder for the actual validation
        schema_url = "https://spec.openapis.org/oas/3.1/schema/2021-09-28"
        schema_response = requests.get(schema_url)
        schema_response.raise_for_status()
        schema = schema_response.json()
        
        jsonschema.validate(instance=self.spec_data, schema=schema)

    def parse_endpoints(self) -> Dict[str, Dict[str, Any]]:
        endpoints = {}
        paths = self.spec_data.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace']:
                    continue
                endpoint_id = f"{method.upper()}_{path}"
                endpoints[endpoint_id] = {
                    'path': path,
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {}),
                    'responses': details.get('responses', {}),
                    'security': details.get('security', [])
                }
        return endpoints

    def parse_schemas(self) -> Dict[str, Dict[str, Any]]:
        return self.spec_data.get('components', {}).get('schemas', {})

    def parse_security_schemes(self) -> Dict[str, Dict[str, Any]]:
        return self.spec_data.get('components', {}).get('securitySchemes', {})

    def parse_servers(self) -> List[Dict[str, Any]]:
        return self.spec_data.get('servers', [])

    def parse(self) -> Dict[str, Any]:
        self.load_spec()
        return {
            'info': self.spec_data.get('info', {}),
            'endpoints': self.parse_endpoints(),
            'schemas': self.parse_schemas(),
            'security_schemes': self.parse_security_schemes(),
            'servers': self.parse_servers()
        }