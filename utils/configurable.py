import json
from typing import List, Any


class EventsProperty:
    registry: List[str]

    def __init__(self):
        self.registry = []

    def __call__(self, m):
        self.registry.append(m.__name__)
        return m

    def get_properties(self, parent_class):
        to_return: dict = {}
        for reg in self.registry:
            to_return[reg] = getattr(parent_class, reg)
        return to_return


class Configurable:
    values: dict = {}
    __file_path: str
    parent_class: Any

    def __init__(self, parent_class, config_filename: str, __configurable_properties: EventsProperty):
        self.__file_path = config_filename
        self.events_property = __configurable_properties
        self.parent_class = parent_class

        try:
            f = open(self.__file_path, "r")
            self.values = json.loads(f.read())
            f.close()
        except FileNotFoundError:
            print("CONF: File for configurable missing, creating a new one...")
            self.__write_values()
            print("CONF: Configurable created successfully.")

    def __getitem__(self, item):
        return getattr(self.parent_class, item)

    def read_values(self) -> dict:
        return self.events_property.get_properties(self.parent_class)

    def __write_values(self) -> None:
        properties: dict = self.read_values()
        f = open(self.__file_path, "w+")
        json_data = json.dumps(properties, indent=2)
        f.write(json_data)
        f.close()

    def try_read_value(self, key: str, fallback: Any) -> Any:
        if key in self.values.keys():
            return self.values[key]
        else:
            print(f"CONF: Saving new config property '{key}'.")
            self.values[key] = fallback
            self.__write_values()
            return fallback
