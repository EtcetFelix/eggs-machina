from dataclasses import dataclass
from enum import Enum
import time

from eggs_machina.hw_drivers.transport import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport

class CAN_ID_Type(Enum):
    STANDARD = 0,
    EXTENDED = 1
@dataclass
class CAN_Message:
    can_id: bytes
    data_len: int
    data: bytes
    can_id_type: CAN_ID_Type
    
class CAN_Baud_Rate(Enum):
    CAN_BAUD_125_KBS = 1
    CAN_BAUD_250_KBS = 2
    CAN_BAUD_500_KBS = 3
    CAN_BAUD_1_MBS = 4

class PCAN(Transport):
    def __init__(self, channel: PCANBasic.TPCANHandle, baud_rate: CAN_Baud_Rate):
        self.channel = channel
        self.baud_rate = baud_rate

        pcan_baud_rate: PCANBasic.TPCANBaudrate = PCANBasic.PCAN_BAUD_1M
        if baud_rate == CAN_Baud_Rate.CAN_BAUD_125_KBS:
            pcan_baud_rate = PCANBasic.PCAN_BAUD_125K
        elif baud_rate == CAN_Baud_Rate.CAN_BAUD_250_KBS:
            pcan_baud_rate = PCANBasic.PCAN_BAUD_250K
        elif baud_rate == CAN_Baud_Rate.CAN_BAUD_500_KBS:
            pcan_baud_rate = PCANBasic.PCAN_BAUD_500K

        self.transport = PCANBasic()
        self.transport.Initialize(channel, pcan_baud_rate)

    def recv(self, can_id: int, timeout_s: int) -> CAN_Message:
        end_time = time.time() + timeout_s
        while time.time() < end_time:
            status, msg, timestamp = self.transport.Read(self.channel)
            if msg.ID == can_id:
                return CAN_Message(can_id=msg.ID, data_len=msg.LEN, data=msg.DATA)
        return None
        
    def send(self, can_id: int, data: bytes) -> bool:
        msg = PCANBasic.TPCANMsg()
        msg.ID = can_id
        msg.MSGTYPE = PCANBasic.PCAN_MESSAGE_STANDARD
        if can_id > 0x7FF:
            msg.MSGTYPE = PCANBasic.PCAN_MESSAGE_EXTENDED
        msg.LEN = len(data)
        msg.DATA = data
        try:
            self.transport.Write(self.channel, msg)
        except:
            print(f"Failed to write CAN-ID: {can_id}")
            return False
        return True       
