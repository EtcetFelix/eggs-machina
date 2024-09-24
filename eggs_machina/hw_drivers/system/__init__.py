from eggs_machina.hw_drivers.api.base import API_Comm


class Robstride_01:
    def __init__(self, api: API_Comm) -> None:
        self.api = api