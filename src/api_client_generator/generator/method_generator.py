# api_client_generator/generator/method_generator.py

from typing import Dict, Any
import jinja2

class MethodGenerator:
    def __init__(self, endpoint: Dict[str, Any]):
        self.endpoint = endpoint
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate(self) -> str:
        template = self.env.get_template('method_template.py.jinja')
        return template.render(endpoint=self.endpoint)

# Example method_template.py.jinja:
'''
def {{ endpoint.operationId }}(self{% for param in endpoint.parameters %}, {{ param.name }}: {{ param.type }}{% endfor %}):
    """
    {{ endpoint.summary }}
    """
    url = f"{self.base_url}{{ endpoint.path }}"
    {% if endpoint.method == 'GET' %}
    response = self.session.get(url, params={ {% for param in endpoint.parameters %}'{{ param.name }}': {{ param.name }}, {% endfor %} })
    {% elif endpoint.method == 'POST' %}
    response = self.session.post(url, json={ {% for param in endpoint.parameters %}'{{ param.name }}': {{ param.name }}, {% endfor %} })
    {% endif %}
    response.raise_for_status()
    return response.json()
'''