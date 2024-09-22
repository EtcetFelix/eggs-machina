from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def recv(self, timeout_s: int, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def send(self, *args, **kwargs) -> any:
        pass
