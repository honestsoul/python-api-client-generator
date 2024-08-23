# src/api_client_generator/mock_generator.py

from typing import Dict, Any

class MockResponse:
    def __init__(self, json_data: Dict[str, Any], status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def create_mock_response(endpoint: Dict[str, Any], status_code: int = 200) -> MockResponse:
    # Simple implementation - you can expand this later
    return MockResponse({"message": "This is a mock response"}, status_code)

def generate_mock_data(schema: Dict[str, Any]) -> Any:
    # Simple implementation - you can expand this later
    if schema.get('type') == 'object':
        return {key: generate_mock_data(value) for key, value in schema.get('properties', {}).items()}
    elif schema.get('type') == 'array':
        return [generate_mock_data(schema.get('items', {})) for _ in range(2)]
    elif schema.get('type') == 'string':
        return "mock_string"
    elif schema.get('type') in ['integer', 'number']:
        return 0
    elif schema.get('type') == 'boolean':
        return False
    return None
