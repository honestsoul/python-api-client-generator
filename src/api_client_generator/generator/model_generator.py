# api_client_generator/generator/model_generator.py

from typing import Dict, Any
import jinja2

class ModelGenerator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate(self) -> str:
        template = self.env.get_template('model_template.py.jinja')
        return template.render(schema=self.schema)

# Example model_template.py.jinja:
'''
class {{ schema.name }}:
    def __init__(self{% for prop, details in schema.properties.items() %}, {{ prop }}: {{ details.type }}{% endfor %}):
        {% for prop in schema.properties %}
        self.{{ prop }} = {{ prop }}
        {% endfor %}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            {% for prop in schema.properties %}
            {{ prop }}=data.get('{{ prop }}'),
            {% endfor %}
        )

    def to_dict(self) -> dict:
        return {
            {% for prop in schema.properties %}
            '{{ prop }}': self.{{ prop }},
            {% endfor %}
        }
'''