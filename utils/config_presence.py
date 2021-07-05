from utils.configurable import Configurable, EventsProperty


class ConfigPresence(Configurable):
    events_property = EventsProperty()

    def __init__(self):
        file = "cogs/data/presence.json"
        super().__init__(self, file, self.events_property)

    @property
    @events_property
    def status(self) -> str:
        return self.try_read_value("status", ["testing"])

    @property
    @events_property
    def status_nr(self) -> str:
        return self.try_read_value("status_nr", ["testing"])


config_presence = ConfigPresence()
