from enum import Enum

from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import CAN_Message


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

    def _send_frame(self, msg_type: Robstride_Msg_Type, data: bytes):
        extended_can_id = self.motor_can_id | (self.host_can_id << 8) | (msg_type.value << 24)
        print(extended_can_id)
        self.can_transport.send(can_id=extended_can_id, data=data)

    def _read_frame(self, msg_id: int, timeout_s: int) -> bytes:
        message: CAN_Message = self.can_transport.recv(can_id=msg_id, timeout_s=timeout_s)
        if message != None:
            return message.data
