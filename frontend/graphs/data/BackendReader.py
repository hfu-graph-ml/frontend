import requests
from requests import Response
import json

'''Reads the JSON data from the url and saves it in appropriate python format (dictionary)'''
class BackendReader:
    _req_resp = None

    def __init__(self, string_url: str):
        self.string_url = string_url
        self._req_resp = self.get_graph_data()

    # Performs a get request to the desired url and returns the request result
    def get_graph_data(self) -> Response:
        request_response = requests.get(self.string_url)

        if not request_response.status_code == 200:
            raise RuntimeError(
                'Request to page ' + self.string_url + ' failed with status code ' + str(request_response.status_code))

        return request_response

    # Deserializes the JSON document to a python object (dictionary)
    # Uses built-in method json.loads()
    def deserialize_response(self) -> dict:
        json_dict = json.loads(self._req_resp.content)
        self.trim_dict(json_dict, ['status'])

        return json_dict

    # Trims off unnecessary keys from the dictionary
    def trim_dict(self, json_dict: dict, trim_keys: list[str]) -> None:
        for key in trim_keys:
            json_dict.pop(key)
