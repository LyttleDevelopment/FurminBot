from utils.configurable import Configurable, EventsProperty


class Emojis(Configurable):
    events_property = EventsProperty()

    def __init__(self):
        file = "emojis.json"
        super().__init__(self, file, self.events_property)

    @property
    @events_property
    def error(self):
        return self.try_read_value("error", ":x:")


emojis = Emojis()
