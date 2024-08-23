# tests/test_mock_generator.py

from api_client_generator.testing.mock_generator import create_mock_response, generate_mock_data

def test_create_mock_response():
    endpoint = {
        'responses': {
            '200': {
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
    mock_response = create_mock_response(endpoint)
    assert mock_response.status_code == 200
    assert 'id' in mock_response.json()
    assert 'name' in mock_response.json()

def test_generate_mock_data():
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'is_active': {'type': 'boolean'}
        }
    }
    mock_data = generate_mock_data(schema)
    assert isinstance(mock_data, dict)
    assert 'id' in mock_data
    assert isinstance(mock_data['id'], int)
    assert 'name' in mock_data
    assert isinstance(mock_data['name'], str)
    assert 'is_active' in mock_data
    assert isinstance(mock_data['is_active'], bool)

# Add more tests as needed
