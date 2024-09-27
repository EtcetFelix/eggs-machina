"""The driver for using the USB2CAN-X2 device by innomaker."""

from eggs_machina.hw_drivers.transport.base import Transport
import can
import os

class USB2CANX2(Transport):
    def __init__(self, baud_rate: int):
        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system("sudo ifconfig can0 txqueuelen 100000")
        os.system('sudo ifconfig can0 up')
        self.baud_rate = baud_rate
        self.bus = can.interface.Bus(channel = 'can0', interface = 'socketcan')
        

    def recv(self, can_id: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        pass

    # def send(self, can_id: int, data: bytes, is_extended_id: bool, *args, **kwargs) -> any:
    def send(self, can_id: int, is_extended_id: bool, *args, **kwargs) -> any:

        msg = can.Message(arbitration_id=0x123, data=[0,1,2,3,4,5,6,7])
        self.bus.send(msg)

if __name__ == "__main__":
    usb2can = USB2CANX2(baud_rate=10000)
    usb2can.send(1,True)
    os.system('sudo ifconfig can0 down')