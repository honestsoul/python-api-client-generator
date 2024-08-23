# python-api-client-generator

# API Client Generator

Automatically generate Python API clients from OpenAPI/Swagger specifications.

## Features

- Parse OpenAPI and Swagger specifications
- Generate Python client code with type hints
- Support for various authentication methods (API Key, OAuth)
- Rate limiting to respect API constraints
- Asynchronous support for efficient concurrent requests
- Mock response generation for testing

## Installation

You can install the API Client Generator using pip:

```bash
pip install api-client-generator
```

## Quick Start

Here's a quick example of how to use the API Client Generator:

```python
from api_client_generator import OpenAPIParser, ClientGenerator, AuthHandler

# Parse the OpenAPI spec
parser = OpenAPIParser('https://api.example.com/openapi.json')
parsed_spec = parser.parse()

# Generate the client
generator = ClientGenerator(parsed_spec)
generator.write_client('generated_client')

# Set up authentication
auth_handler = AuthHandler(parsed_spec['security_schemes'])
auth_handler.setup_auth('api_key', api_key='your-api-key')

# Use the generated client
from generated_client.client import ExampleAPIClient

client = ExampleAPIClient('https://api.example.com', auth_handler)
response = client.get_user(user_id=123)
print(response)
```

## Asynchronous Usage

The library also supports asynchronous operations:

```python
import asyncio
from api_client_generator import AsyncAPIClient

async def main():
    async with AsyncAPIClient('https://api.example.com', auth_handler) as client:
        data = await client.get('/users/123')
        print(data)

asyncio.run(main())
```

## Testing

The library provides utilities for mocking API responses in your tests:

```python
from api_client_generator.testing import mock_client

def test_get_user():
    mocked_client = mock_client(ExampleAPIClient, parsed_spec)
    result = mocked_client.get_user(user_id=123)
    assert 'id' in result
    assert 'name' in result
```

## Documentation

For more detailed information about the API Client Generator, please refer to our [documentation](link-to-your-documentation).

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on our [GitHub issue tracker](https://github.com/yourusername/api-client-generator/issues).
