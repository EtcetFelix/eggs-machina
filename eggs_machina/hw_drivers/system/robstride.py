from enum import Enum

from eggs_machina.hw_drivers.transport import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport import can_transport



class Robstride_Msg_Type(Enum):
    DEVICE_ID = 0
    MOTOR_CTRL = 1
    MOTOR_FEEDBACK = 2
    MOTOR_ENABLE = 3
    MOTOR_STOP = 4
    MOTOR_ZERO = 6
    SET_CAN_ID = 7
    PARAM_READ = 17
    PARAM_WRITE = 18
    FAULT_FEEDBACK = 21
    BAUD_RATE_CHANGE = 22

class Robstride:
    def __init__(self, host_can_id: int, motor_can_id: int, can_transport: Transport):
        self.host_can_id = host_can_id
        self.motor_can_id = motor_can_id
        self.can_transport = can_transport

    def get_device_id(self):
        self._send_frame(
            msg_type=Robstride_Msg_Type.DEVICE_ID, 
            data=bytes([0, 0, 0, 0, 0, 0, 0, 0]),
        )
        response_can_id = 0xFE | (self.motor_can_id << 8)
        return self._read_frame(msg_id=response_can_id)

    def _send_frame(self, msg_type: Robstride_Msg_Type, data: bytes):
        extended_can_id = self.motor_can_id | (self.host_can_id << 8) | (msg_type.value << 24)
        self.can_transport.send(can_id=extended_can_id, data=data, is_extended_id=True)

    def _read_frame(self, msg_id: int, timeout_s: int = 1) -> bytes:
        message: can_transport.CAN_Message = self.can_transport.recv(can_id=msg_id, is_extended_id=True, timeout_s=timeout_s)
        if message != None:
            return message.data

if __name__ == "__main__":
    pcan_transport = can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS1, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    
    robstride = Robstride(host_can_id=0xFD, motor_can_id=0x7F, can_transport=pcan_transport)
    device_id = robstride.get_device_id()
    if device_id != None:
        print(device_id)
