"""The driver for using the USB2CAN-X2 device by innomaker."""

from eggs_machina.hw_drivers.transport.base import Transport

class USB2CANX2(Transport):
    def __init__(self, baud_rate: int):
        self.baud_rate = baud_rate
        pass

    def recv(self, can_id: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    def send(self, can_id: int, data: bytes, is_extended_id: bool, *args, **kwargs) -> any:
        pass