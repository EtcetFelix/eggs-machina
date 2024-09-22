from enum import Enum

from eggs_machina.hw_drivers.api.base import API_Comm


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
    def __init__(self, host_can_id: int, motor_can_id: int, can_api: API_Comm):
        self.host_can_id = host_can_id
        self.motor_can_id = motor_can_id
        self.can_api = can_api

    def _send_frame(self, msg_type: Robstride_Msg_Type, data: bytearray):
        extended_can_id = self.motor_can_id | (self.host_can_id << 8) | (msg_type.value << 24)
        print(extended_can_id)
        self.can_api.write(message=extended_can_id, data=data, is_extended=True)

    def _read_frame(self, msg_id: int, timeout: int) -> bytearray:
        pass
