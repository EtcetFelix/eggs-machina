from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type


class Transport(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType]
    ) -> bool:
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def recv(self, can_id: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def recv_in_range(self, can_id_min: int, can_id_max: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def recv_bitmasked_can_id(self, can_id: int, bitmask: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def send(self, can_id: int, data: bytes, is_extended_id: bool, *args, **kwargs) -> bool:
        pass
