import requests
from requests import Response
import json


'''Reads the JSON data from the url and saves it in appropriate python format (dictionary)'''
class BackendReader:
    json_dict = []

    def __init__(self, string_url: str):
        self.string_url = string_url
        self.process_response(self.get_graph_data())

    # Performs a get request to the desired url and returns the request result
    def get_graph_data(self) -> Response:
        request_response = requests.get(self.string_url)

        if not request_response.status_code == 200:
            raise RuntimeError('Request to page ' + self.string_url + ' failed with status code ' + str(request_response.status_code))

        return request_response

    # Deserializes the JSON document to a python object (dictionary)
    # Uses built-in method json.loads()
    def process_response(self, response: Response) -> None:
        # TODO: continue
        self.json_dict = json.loads(response.content)
        self.trim_dict(['status'])

    # Trims off unnecessary keys from the dictionary
    def trim_dict(self, trim_keys: list[str]) -> None:
        for key in trim_keys:
            self.json_dict.pop(key)

    def get_json_dict(self) -> dict:
        return self.json_dict

    def get_dict_graph(self) -> dict:
        return self.json_dict['graph']

    def get_dict_nodes(self) -> dict:
        return self.json_dict['graph']['nodes']

    def get_dict_node_at(self, index: int) -> dict:
        return self.json_dict['graph']['nodes'][index]

    def get_dict_edges(self) -> dict:
        return self.json_dict['graph']['edges']

    def get_dict_edge_at(self, index: int) -> dict:
        return self.json_dict['graph']['edges'][index]


reader = BackendReader('http://localhost:8000/graphs/')
reader.get_json_dict()
