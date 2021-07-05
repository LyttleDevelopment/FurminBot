from utils.configurable import Configurable, EventsProperty


class Config(Configurable):
    events_property = EventsProperty()

    def __init__(self):
        file = "config.json"
        super().__init__(self, file, self.events_property)

    @property
    @events_property
    def prod_token(self) -> str:
        return self.try_read_value("prod_token", "insert token here")

    @property
    @events_property
    def dev_token(self) -> str:
        return self.try_read_value("dev_token", "insert token here")

    @property
    @events_property
    def status(self) -> str:
        return self.try_read_value("status", ["testing"])

    @property
    @events_property
    def status_nr(self) -> str:
        return self.try_read_value("status_nr", ["testing"])

    @property
    @events_property
    def admin_guild(self) -> int:
        return self.try_read_value("admin_guild", 831222717793304606)

    @property
    @events_property
    def error_channel(self) -> int:
        return self.try_read_value("error_channel", 833274053271486494)

    @property
    @events_property
    def roles(self) -> dict:
        return self.try_read_value("roles", {})

    @property
    @events_property
    def groups(self) -> dict:
        return self.try_read_value("groups", {})


config = Config()
