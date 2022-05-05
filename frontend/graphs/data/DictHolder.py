import asyncio
import copy

from frontend.graphs.data.BackendReader import BackendReader
from frontend.graphs.data.BackendWriter import BackendWriter
from frontend.graphs.observe.Observable import Observable
from frontend.graphs.observe.Observer import Observer


class DictHolder(Observable):
    _json_dict = []
    _dict_copy = []
    _observers = []

    def __init__(self, string_url: str):
        reader = BackendReader(string_url)
        self._json_dict = reader.deserialize_response()
        self._dict_copy = copy.deepcopy(self._json_dict)
        # Hardcoded change for test purpose only
        self._json_dict['graph']['nodes'][0]['name'] = "HHHHH"

    # Starts an async loop that runs forever in order to
    # continuously check the dictionary
    def async_loop(self) -> None:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.monitor_dict())
        loop.run_forever()

    # Calls the checker function
    async def monitor_dict(self) -> None:
        await self.check_dict(1)

    # Checks the dictionary for changes against a
    # deepcopy of the same dictionary. If
    # changes are recognized, the observer is notified
    async def check_dict(self, threshold: int):
        num_changes = 0

        for key in self._json_dict['graph']:
            for dict_entry in range(len(key)):
                for entry_item in self._json_dict['graph'][key][dict_entry]:
                    orig_val = self.get_orig_dict_entry_at(key,
                                                           dict_entry,
                                                           entry_item)
                    copy_val = self.get_copy_dict_entry_at(key,
                                                           dict_entry,
                                                           entry_item)
                    if orig_val != copy_val:
                        num_changes += 1

                    if num_changes == threshold:
                        self.notify_observer()
                        return

    # Adds an observer to the current observable
    # in order to listen for changes
    def attach(self, observer: Observer) -> None:
        print('Observer added')
        self._observers.append(observer)

    # Removes an observer of the current observable
    def detach(self, observer: Observer) -> None:
        print('Observer removed')
        self._observers.remove(observer)

    # If changes in the observable are recognized,
    # all attached observers are updated
    def notify_observer(self) -> None:
        print('notified')
        for observer in self._observers:
            observer.update(self._json_dict)

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

    def get_orig_dict_entry_at(self, key: str, dict_idx: int, idx_entry):
        return self._json_dict['graph'][key][dict_idx][idx_entry]

    def get_copy_dict_entry_at(self, key: str, dict_idx: int, idx_entry):
        return self._dict_copy['graph'][key][dict_idx][idx_entry]


test = DictHolder('http://localhost:8000/graphs/')
observer1 = BackendWriter('http://localhost:8000/graphs/')
test.attach(observer1)
test.async_loop()