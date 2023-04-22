"""Модуль инициализации документации Swagger."""

from os import path

from src.api.v1.user_preferences import get_user_preferences_list, drop_custom_user_preference, upsert_user_preferences


def convert_docstring_to_swagger_description(docstring: str) -> str:
    """функция преобразует документ-строку функции в описание для Swagger."""
    docstring = docstring[1:-2]
    result = []
    for row in docstring.split('\n'):
        if 'service' not in row and 'credentials' not in row:
            result.append(row)

    return '<br>'.join(result).replace('    ', '&emsp;')


def write_documentations_to_file():
    with open('api_documentations.py', 'w', encoding='utf-8') as file:
        file.write('"""\nМодуль объектов документации swagger.\n'
                   f'Создано автоматически модулем `{path.basename(__file__)}`\n"""\n\n')

        api_endpoints = [
            get_user_preferences_list,
            drop_custom_user_preference,
            upsert_user_preferences,
        ]

        api_endpoint_description_names = [f'{func.__name__.upper()}_DESCRIPTION' for func in api_endpoints]

        for api_endpoint, description_name in zip(api_endpoints, api_endpoint_description_names):
            docstring = convert_docstring_to_swagger_description(api_endpoint.__doc__)
            file.write(f'{description_name} = """{docstring}"""\n')


if __name__ == '__main__':
    write_documentations_to_file()
