"""The driver for using the USB2CAN-X2 device by innomaker."""

from dataclasses import dataclass
from eggs_machina.hw_drivers.transport.base import Transport
import can
import os
import time

@dataclass
class CAN_Message:
    can_id: int
    data_len: int
    data: bytes

class USB2CANX2(Transport):
    def __init__(self, channel: str, baud_rate: int):
        os.system(f'sudo ifconfig {channel} down')
        os.system(f'sudo ip link set {channel} type can bitrate {baud_rate}')
        os.system(f"sudo ifconfig {channel} txqueuelen {baud_rate}")
        os.system(f'sudo ifconfig {channel} up')
        self.baud_rate = baud_rate
        self.bus = can.interface.Bus(channel = channel, interface = 'socketcan')
        

    def recv(self, can_id: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
        end_time = time.time() + timeout_s
        while time.time() < end_time:
            with self.bus as bus:
                for msg in bus:
                    if int(msg.arbitration_id) == can_id:
                        return CAN_Message(
                            can_id=int(msg.arbitration_id),
                            data_len=int(len(msg.data)),
                            data=bytes(msg.data)
                        )
        return None


    def send(self, can_id: int, data: bytes, is_extended_id: bool, *args, **kwargs) -> bool:
        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=is_extended_id)
        try:
            self.bus.send(msg)
        except:
            print(f"Failed to write CAN-ID: {can_id}")
            return False
        return True

if __name__ == "__main__":
    usb2can = USB2CANX2(channel="can0", baud_rate=10000)
    usb2can.send(can_id=1,data=bytes([0, 0, 0, 0, 0, 0, 0, 0]), is_extended_id=True)
    os.system('sudo ifconfig can0 down')