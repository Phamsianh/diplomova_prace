from typing import Type, Union

from pydantic import BaseModel


def create_markdown_table(schema_class: Union[Type[BaseModel], dict]):
    if isinstance(schema_class, dict):
        schema = schema_class
    else:
        schema = schema_class.schema()
    table = f"""
{schema['description'] if "description" in schema else ''}

| Field name | Type | Required | Description |
| --- | --- | --- | --- |
"""
    for p_name, v in schema['properties'].items():
        name = p_name
        type_ = v['type'] if 'type' in v else ''
        required = 'required' if 'required' in schema and p_name in schema['required'] else 'optional'
        description = v['description'] if 'description' in v else ''
        table += f"| ``{name}`` | " \
                 f"{type_} | " \
                 f"{required} | " \
                 f"{description} |\n"

    if 'definitions' in schema:
        for p_name, v in schema['definitions'].items():
            if 'enum' not in v:
                table += f"""{create_markdown_from_definition(v).lstrip()}"""

    return table


def create_markdown_from_definition(definition):
    table = f"""
{definition['description'] if "description" in definition else ''}

| Field name | Type | Required | Description |
| --- | --- | --- | --- |
"""
    for p_name, v in definition['properties'].items():
        name = p_name
        type_ = v['type'] if 'type' in v else ''
        required = 'required' if 'required' in definition and p_name in definition['required'] else 'optional'
        description = v['description'] if 'description' in v else ''
        table += f"| ``{ name }`` | " \
                 f"{ type_ } | " \
                 f"{ required } | " \
                 f"{ description } |\n"
    return table

