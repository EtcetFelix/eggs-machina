from abc import ABC, abstractmethod

from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import CAN_Message

class System(ABC):
    @abstractmethod
    def __init__(self, transport: Transport, *args, **kwargs) -> None:
        pass

    @staticmethod
    def scale_to_uint(
        val: int | float, 
        raw_max: int | float,
        raw_min: int | float,
        bits: int
    ) -> int:
        if val < raw_max or val < raw_min:
            return 0
        return round(((val - raw_min) * (2 ** bits)) / (raw_max - raw_min))
    
    def scale_to_float(
        val: int,
        bits: int,
        scaled_max: int | float,
        scaled_min: int | float
    ) -> float:
        if val < 0 or val >= 2 ** bits:
            return 0.0
        return ((val * (scaled_max - scaled_min)) / 2 ** bits) + scaled_min
