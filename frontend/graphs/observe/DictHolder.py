from frontend.graphs.data.BackendReader import BackendReader
from frontend.graphs.observe.Observable import Observable
from frontend.graphs.observe.Observer import Observer


class DictHolder(Observable):
    _json_dict = []
    _observers = []

    def __init__(self, string_url: str):
        reader = BackendReader(string_url)
        self._json_dict = reader.deserialize_response()

    def attach(self, observer: Observer) -> None:
        print('Observer added')
        self._observers.append(observer)

    def detatch(self, observer: Observer) -> None:
        print('Observer removed')
        self._observers.remove(observer)

    # TODO: if changes are monitored, notify observer
    def notify_observer(self) -> None:
        for observer in self._observers:
            # TODO: on update, perform http post
            observer.update()

    def monitor_dict(self) -> None:
        print('t')
        # TODO: continue

    def get_json_dict(self) -> dict:
        return self._json_dict

    def get_dict_graph(self) -> dict:
        return self._json_dict['graph']

    def get_dict_nodes(self) -> dict:
        return self._json_dict['graph']['nodes']

    def get_dict_node_at(self, index: int) -> dict:
        return self._json_dict['graph']['nodes'][index]

    def get_dict_edges(self) -> dict:
        return self._json_dict['graph']['edges']

    def get_dict_edge_at(self, index: int) -> dict:
        return self._json_dict['graph']['edges'][index]


test = DictHolder('http://localhost:8000/graphs/')
print("t")
