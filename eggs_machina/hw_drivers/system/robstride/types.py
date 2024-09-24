from dataclasses import dataclass
from enum import Enum
from typing import List


class Robstride_Motor_Mode_Enum(Enum):
    RESET_MODE = 0
    CALIBRATION_MODE = 1
    MOTOR_MODE = 2

class Robstride_Msg_Enum(Enum):
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

class Robstride_Fault_Enum(Enum):
    FAULT_UNCALIBRATED = 0
    FAULT_HALL_ENCODING = 1
    FAULT_MAGNETIC_ENCODING = 2
    FAULT_OVER_TEMPERATURE = 3
    FAULT_OVERCURRENT = 4
    FAULT_UNDERVOLTAGE = 5

@dataclass
class FeedbackResp:
    errors: List[Robstride_Fault_Enum]
    mode: Robstride_Motor_Mode_Enum
    angle_deg: float
    velocity_rads: float
    torque_nm: float
    temp_c: float

@dataclass
class Robstride_Param_Type:
    name: str
    address: int
    byte_len: int
    min: float
    max: float
    can_write: bool

class Robstride_Param_Enum(Enum):
    RUN_MODE = 0
    IQ_REF = 1
    SPEED_REF = 2
    TORQUE_LIMIT = 3
    CURRENT_KP = 4
    CURRENT_KI = 5
    CURRENT_FILTER_GAIN = 6
    POSITION_MODE_ANGLE_CMD = 7
    POSITION_MODE_LIMIT = 8
    MECH_POS_END_COIL = 9
    IQ_FILTER_VALUE = 10
    MECH_VEL_END_COIL = 11
    VBUS_VOLTAGE = 12
    NUM_ROTATIONS = 13
    POSITION_KP = 14
    SPEED_KP = 15
    SPEED_KI = 16
