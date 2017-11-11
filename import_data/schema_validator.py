import os
import requests
import json

from jsonschema import ValidationError, RefResolver
from jsonschema.validators import Draft4Validator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
module_root = os.path.join(BASE_DIR, 'import_data')
IMPORT_URL = 'https://jsonplaceholder.typicode.com/photos'

def _get_json_and_dir(name, json_root, msg_id):
    """
    Get a tuple of the root directory and the loaded json file.
    Arguments:
    `name` -- the name of the json file to load
    Returns:
    Json root dir and the json (alternatively the module root
    and none if file is not found)
    """
    try:
        for root, sub_dirs, files in os.walk(json_root):
            if name in files:
                with open(os.path.join(root, name), 'r') as json_file:
                    return root, json.load(json_file)
        print("{} file not found".format(msg_id))
    except AttributeError:
        print("Error getting {} file:\nTry checking it exists and the right name was supplied.".format(msg_id))

    return BASE_DIR, None

def _get_schema_and_dir(name):
    """
    Gets a tuple of the root directory and the loaded json schema file.
    Note:
    Schema files can be nested
    Arguments:
    `name` -- the name of the schema file to validate the fetched json data
    Returns:
    Json root dir and the json (alternatively the module root
    and none if file is not found)
    """
    schema_root = os.path.join(module_root, 'schemas')
    return _get_json_and_dir(name, schema_root, "Schema")


def pull_data_from_url():
    """
    Makes a GET request to the  API.
    """
    headers = {'Content-Type': 'application/json'}
    response = requests.get(
        url=IMPORT_URL,
        headers=headers,
    )

    response.raise_for_status()
    data = response.json()
    return data

def _get_validated_json(json_data, schema_dir, schema):
    try:
        # makes it possible for schemas to reference relatively
        # https://github.com/Julian/jsonschema/issues/98#issuecomment-17531405
        resolver = RefResolver('file://' + schema_dir + '/', schema)
        Draft4Validator(schema, resolver=resolver).validate(json_data)
        print('data validated successfully')
        return json_data
    except ValidationError as ex:
        print("Data failed schema validation: {}".format(ex.message))
        print('Data failed schema validation: Ensure data is in the right format: {}'.format(ex.message))
        return None
    

def get_data(name):
    """
    Validates json data from the url before returning the data
    Arguments:
    name -- the name of the schema file to validate the fetched json data
    Returns:
    Validated json data or none
    """
    schema_dir, schema = _get_schema_and_dir(name)
    if schema is None:
        return None

    data = pull_data_from_url()
    if data is None:
        return None

    return _get_validated_json(data, schema_dir, schema)


get_data("movie.schema.json")
# pull_data_from_url()
# def _get_schema_file():
#     """
#     Gets a tuple of the root directory and the loaded json schema file.
#     Note:
#     Schema files can be nested
#     Arguments:
#     `name` -- the name of the schema file to validate the fetched json data
#     Returns:
#     Json root dir and the json (alternatively the module root
#     and none if file is not found)
#     """
#     schema_root = os.path.join(module_root, 'schemas')
#     for data_file in os.listdir(schema_root):
#         try:
#             with open(os.path.join(schema_root, data_file), encoding='utf-8') as data_file:
#                 data = json.loads(data_file.read())
#                 print(data)
#                 return data or None
#         except Exception as ex:
#             print(exception)
#     print(schema_root, 'schema root')
#     # return self._get_json_and_dir(name, schema_root, "Schema")

# def _get_validated_json(self, json_data, schema_dir, schema):
#     try:
#         # makes it possible for schemas to reference relatively
#         # https://github.com/Julian/jsonschema/issues/98#issuecomment-17531405
#         resolver = RefResolver('file://' + schema_dir + '/', schema)
#         Draft4Validator(schema, resolver=resolver).validate(json_data)
#         return json_data
#     except ValidationError as ex:
#         logging.error("Data failed schema validation: {}".format(ex.message))
#         self.log_import_fail('Data failed schema validation: Ensure data is in the right format: {}'.format(ex.message))
#         return None

