from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def recv(self, can_id: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def recv_in_range(self, can_id_min: int, can_id_max: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def send(self, can_id: int, data: bytes, is_extended_id: bool, *args, **kwargs) -> bool:
        pass
