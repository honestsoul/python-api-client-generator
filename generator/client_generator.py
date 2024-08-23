# api_client_generator/generator/client_generator.py

import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

class ClientGenerator:
    def __init__(self, parsed_spec: Dict[str, Any]):
        self.parsed_spec = parsed_spec
        self.env = Environment(loader=FileSystemLoader('templates'))

    def generate_client(self) -> str:
        template = self.env.get_template('client_template.py.jinja')
        return template.render(
            info=self.parsed_spec['info'],
            endpoints=self.parsed_spec['endpoints'],
            schemas=self.parsed_spec['schemas']
        )

    def generate_models(self) -> Dict[str, str]:
        models = {}
        template = self.env.get_template('model_template.py.jinja')
        for schema_name, schema in self.parsed_spec['schemas'].items():
            models[schema_name] = template.render(
                schema_name=schema_name,
                properties=schema.get('properties', {})
            )
        return models

    def write_client(self, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, 'client.py'), 'w') as f:
            f.write(self.generate_client())
        
        models_dir = os.path.join(output_dir, 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        for model_name, model_code in self.generate_models().items():
            with open(os.path.join(models_dir, f"{model_name.lower()}.py"), 'w') as f:
                f.write(model_code)

# Usage:
# generator = ClientGenerator(parsed_spec)
# generator.write_client('generated_client')