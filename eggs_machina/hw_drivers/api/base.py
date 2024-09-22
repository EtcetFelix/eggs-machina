from abc import ABC, abstractmethod
from dataclasses import dataclass

from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import CAN_Message


class API_Comm(ABC):
    @abstractmethod
    def write(self, message: any) -> bool:
        pass

    @abstractmethod
    def read(self, timeout: int) -> any:
        pass

class CanApi(API_Comm):
    def __init__(self, transport: Transport):
        self.transport = transport

    @abstractmethod
    def write(self, can_id: int, data: bytearray, is_extended: bool = False) -> bool:
        pass

    @abstractmethod
    def read(self, can_id: int, timeout: int) -> CAN_Message:
        pass
