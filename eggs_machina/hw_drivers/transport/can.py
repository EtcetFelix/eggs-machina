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
    can_id: int
    data_len: int
    data: bytes
    
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

        self.transport = PCANBasic.PCANBasic()
        self.transport.Initialize(channel, pcan_baud_rate)

    def recv(self, can_id: int, is_extended_id: bool = False, timeout_s: int = 0.5) -> CAN_Message:
        msg_type = PCANBasic.PCAN_MESSAGE_STANDARD
        if is_extended_id:
            msg_type = PCANBasic.PCAN_MESSAGE_EXTENDED
        end_time = time.time() + timeout_s
        while time.time() < end_time:
            # returns tuple of status, msg, timestamp
            _, msg, _ = self.transport.Read(self.channel)
            if int(msg.ID) == can_id and msg.MSGTYPE == msg_type:
                return CAN_Message(
                    can_id=int(msg.ID), 
                    data_len=int(msg.LEN), 
                    data=bytes(msg.DATA)
                )
        return None
        
    def send(self, can_id: int, data: bytes, is_extended_id: bool = False) -> bool:
        msg = PCANBasic.TPCANMsg()
        msg.ID = can_id
        msg.MSGTYPE = PCANBasic.PCAN_MESSAGE_STANDARD
        if is_extended_id:
            msg.MSGTYPE = PCANBasic.PCAN_MESSAGE_EXTENDED
        msg.LEN = len(data)
        msg.DATA = data
        try:
            self.transport.Write(self.channel, msg)
        except:
            print(f"Failed to write CAN-ID: {can_id}")
            return False
        return True       
