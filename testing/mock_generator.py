# api_client_generator/testing/mock_generator.py

import json
from typing import Dict, Any
from unittest.mock import Mock

class MockResponse:
    def __init__(self, json_data: Dict[str, Any], status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP Error: {self.status_code}")

def create_mock_response(endpoint: Dict[str, Any], status_code: int = 200) -> MockResponse:
    response_schema = endpoint['responses'].get(str(status_code), {}).get('content', {}).get('application/json', {}).get('schema', {})
    mock_data = generate_mock_data(response_schema)
    return MockResponse(mock_data, status_code)

def generate_mock_data(schema: Dict[str, Any]) -> Any:
    if 'type' not in schema:
        return {}

    if schema['type'] == 'object':
        return {prop: generate_mock_data(prop_schema) for prop, prop_schema in schema.get('properties', {}).items()}
    elif schema['type'] == 'array':
        return [generate_mock_data(schema['items']) for _ in range(3)]  # Generate 3 items for each array
    elif schema['type'] == 'string':
        return "mock_string"
    elif schema['type'] == 'integer':
        return 42
    elif schema['type'] == 'number':
        return 3.14
    elif schema['type'] == 'boolean':
        return True
    else:
        return None

def mock_client(client_class, parsed_spec: Dict[str, Any]):
    mocked_client = Mock(spec=client_class)

    for endpoint_name, endpoint in parsed_spec['endpoints'].items():
        method_name = endpoint_name.lower()
        mock_response = create_mock_response(endpoint)
        getattr(mocked_client, method_name).return_value = mock_response.json()

    return mocked_client

# Usage in tests:
# from your_client_module import YourAPIClient
# from api_client_generator.testing.mock_generator import mock_client
#
# def test_api_call():
#     parsed_spec = {...}  # Your parsed OpenAPI spec
#     mocked_client = mock_client(YourAPIClient, parsed_spec)
#     result = mocked_client.some_endpoint()
#     assert 'expected_key' in result