# Welcome to API Client Generator

API Client Generator is a powerful tool that automatically generates Python API clients from OpenAPI specifications. It simplifies the process of integrating with RESTful APIs by providing type-hinted, well-structured Python code.

## Features

- Parse OpenAPI 3.0 specifications
- Generate Python client code with type hints
- Support for various authentication methods (API Key, OAuth2)
- Implement rate limiting to respect API constraints
- Provide asynchronous support for efficient concurrent requests
- Include mock response generation for testing

## Quick Start

```python
from api_client_generator import OpenAPIParser, ClientGenerator

# Parse the OpenAPI spec
parser = OpenAPIParser('https://api.example.com/openapi.json')
parsed_spec = parser.parse()

# Generate the client
generator = ClientGenerator(parsed_spec)
generator.write_client('generated_client')

# Use the generated client
from generated_client import ApiClient

client = ApiClient('https://api.example.com')
response = client.get_user(user_id=123)
print(response)
```

For more detailed information on installation, usage, and API reference, please check the respective sections in this documentation.