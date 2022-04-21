import asyncio
import copy

from frontend.graphs.data.BackendReader import BackendReader
from frontend.graphs.observe.Observable import Observable
from frontend.graphs.observe.Observer import Observer


class DictHolder(Observable):
    _json_dict = []
    # Dont touch that one during graph manipulation task
    _dict_copy = []
    _observers = []

    def __init__(self, string_url: str):
        reader = BackendReader(string_url)
        self._json_dict = reader.deserialize_response()
        self._dict_copy = copy.deepcopy(self._json_dict)

        #self._dict_copy['graph']['nodes'][0]['name'] = "HHHHH"
        self.async_loop()

    def async_loop(self) -> None:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.monitor_dict())
        loop.run_forever()

    async def monitor_dict(self) -> None:
        await self.check_dict()
        print('t')
        # TODO: continue

    async def check_dict(self):

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
                        self.notify_observer()

    def attach(self, observer: Observer) -> None:
        print('Observer added')
        self._observers.append(observer)

    def detatch(self, observer: Observer) -> None:
        print('Observer removed')
        self._observers.remove(observer)

    # TODO: if changes are monitored, notify observer
    def notify_observer(self) -> None:
        print('notified')
        for observer in self._observers:
            # TODO: on update, perform http post
            observer.update()

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
test.check_dict()
print("t")
