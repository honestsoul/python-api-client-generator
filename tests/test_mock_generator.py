# testing/test_mock_generator.py

from api_client_generator.mock_generator import create_mock_response, generate_mock_data

def test_create_mock_response():
    endpoint = {}  # You can add more complex endpoint data here if needed
    response = create_mock_response(endpoint)
    assert response.status_code == 200
    assert response.json() == {"message": "This is a mock response"}

def test_generate_mock_data():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "is_active": {"type": "boolean"},
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
    mock_data = generate_mock_data(schema)
    assert isinstance(mock_data, dict)
    assert isinstance(mock_data.get('name'), str)
    assert isinstance(mock_data.get('age'), int)
    assert isinstance(mock_data.get('is_active'), bool)
    assert isinstance(mock_data.get('tags'), list)
    assert all(isinstance(tag, str) for tag in mock_data.get('tags', []))
