from utils.configurable import Configurable, EventsProperty


class Config(Configurable):
    events_property = EventsProperty()

    def __init__(self):
        file = "database/config.json"
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
    def log_channel(self) -> int:
        return self.try_read_value("log_channel", 0)

    @property
    @events_property
    def error_channel(self) -> int:
        return self.try_read_value("error_channel", 0)

    @property
    @events_property
    def advanced_logs(self) -> int:
        return self.try_read_value("advanced_logs", 0)

    @property
    @events_property
    def main_logs(self) -> int:
        return self.try_read_value("main_logs", 0)


config = Config()
