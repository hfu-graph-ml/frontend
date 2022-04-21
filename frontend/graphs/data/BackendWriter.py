from frontend.graphs.observe.Observer import Observer
import json
import requests


class BackendWriter(Observer):

    def __init__(self, string_url: str):
        self.string_url = string_url

    # TODO: remove comment
    def update(self, updated_dict: dict) -> None:
        json_string = self.serialize_response(updated_dict)
        self.send_graph_data(json_string)
        print('updated')

    def serialize_response(self, updated_dict: dict) -> str:
        json_string = json.dumps(updated_dict)

        return json_string

    def send_graph_data(self, json: str) -> None:
        headers = {"Content-Type": "application/json"}
        request_response = requests.post(self.string_url, data=json, headers=headers)

        # Returns 405 not allowed -> router
        '''if not request_response.status_code == 200:
            raise RuntimeError(
                'Post-Request to page ' + self.string_url + ' failed with status code ' + str(request_response.status_code))'''
