from dataclasses import dataclass
from enum import Enum


class CAN_ID_Type(Enum):
    STANDARD = 0,
    EXTENDED = 1

@dataclass
class CAN_Message:
    can_id: int
    data_len: int
    data: bytes
    
class CAN_Baud_Rate(Enum):
    CAN_BAUD_125_KBS = 1
    CAN_BAUD_250_KBS = 2
    CAN_BAUD_500_KBS = 3
    CAN_BAUD_1_MBS = 4