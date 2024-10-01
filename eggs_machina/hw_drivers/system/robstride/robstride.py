import math
import struct
import time

from eggs_machina.hw_drivers.system.base import System
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum
from eggs_machina.hw_drivers.transport.can import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import can_transport

from eggs_machina.hw_drivers.system.robstride.constants import ROBSTRIDE_PARMS
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2

EMPTY_CAN_FRAME = bytes([0, 0, 0, 0, 0, 0, 0, 0])

class Robstride(System):
    def __init__(self,  can_transport: Transport, host_can_id: int, motor_can_id: int):
        self.host_can_id = host_can_id
        self.motor_can_id = motor_can_id
        self.can_transport = can_transport

    def get_device_id(self):
        self._send_frame(
            msg_type=Robstride_Msg_Enum.DEVICE_ID, 
            data=EMPTY_CAN_FRAME,
        )
        return self.get_broadcast_frame()
    
    def enable_motor(self):
        self._send_frame(
            msg_type=Robstride_Msg_Enum.MOTOR_ENABLE,
            data=EMPTY_CAN_FRAME,
        )

    def stop_motor(self):
        self._send_frame(
            msg_type=Robstride_Msg_Enum.MOTOR_STOP,
            data=EMPTY_CAN_FRAME,
        )
    
    def set_curr_position_zero(self):
        self._send_frame(
            msg_type=Robstride_Msg_Enum.MOTOR_ZERO,
            data=bytes([1, 0, 0, 0, 0, 0, 0, 0])
        )

    def set_motor_can_id(self, new_can_id: int):
        can_frame_id = self.motor_can_id | (new_can_id << 8) | (new_can_id << 16) | ( Robstride_Msg_Enum.SET_CAN_ID << 24)
        self.can_transport.send(can_id=can_frame_id, data=EMPTY_CAN_FRAME, is_extended_id=True)

    def set_motor_baud_rate(self, new_baud_rate: can_transport.CAN_Baud_Rate):
        data = bytes([0, 0, 0, 0, 0, 0, 0, 0])
        if new_baud_rate == can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS:
            data[0] = 1
        elif new_baud_rate == can_transport.CAN_Baud_Rate.CAN_BAUD_500_KBS:
            data[0] = 2
        elif new_baud_rate == can_transport.CAN_Baud_Rate.CAN_BAUD_250_KBS:
            data[0] = 3
        elif new_baud_rate == can_transport.CAN_Baud_Rate.CAN_BAUD_125_KBS:
            data[0] = 4
        self._send_frame(
            msg_type=Robstride_Msg_Enum.BAUD_RATE_CHANGE,
            data=data
        )
        # TODO - reinit transport with new baud rate
    
    def read_single_param(self, param: Robstride_Param_Enum) -> float | int:
        param_data = ROBSTRIDE_PARMS[param]
        data = bytearray(EMPTY_CAN_FRAME)
        data[0:2] = struct.pack("<H", param_data.address)
        self._send_frame(
            msg_type=Robstride_Msg_Enum.PARAM_READ,
            data=data
        )
        response_id = self.host_can_id | (self.motor_can_id << 8) | (Robstride_Msg_Enum.PARAM_READ.value << 24)
        param_response_frame = self._read_frame(response_id)
        return struct.unpack(f"<{param_data.data_type._type_}", param_response_frame[4:4+param_data.byte_len])[0]


    def write_single_param(self, param: Robstride_Param_Enum, value: float | int) -> bool:
        param_data = ROBSTRIDE_PARMS[param]
        if value < param_data.min or value > param_data.max:
            return False
        data = EMPTY_CAN_FRAME
        data[0:2] = struct.pack("<H", param_data.address)
        data[8 - param_data.byte_len:] = struct.pack(f"<{param_data.data_type._type_}", value)
        self._send_frame(
            msg_type=Robstride_Msg_Enum.PARAM_WRITE,
            data=data
        )

    def move_to_position(self,
            torque_Nm: float,
            target_angle_deg: float, 
            angular_vel_rads: float, 
            pid_kp: float = 250, 
            pid_kd: float = 5
        ):
        data = bytearray(EMPTY_CAN_FRAME)
        torque_scaled = self.scale_to_uint(torque_Nm, 17, -17, 16)
        data[0:2] = struct.pack("<H", self.scale_to_uint(self._deg_to_radians(target_angle_deg) , 4 * math.pi, -4 * math.pi, 16))
        data[2:4] = struct.pack("<H", self.scale_to_uint(angular_vel_rads, 44, -44, 16))
        data[4:6] = struct.pack("<H", self.scale_to_uint(pid_kp, 500, 0, 16))
        data[6:] = struct.pack("<H", self.scale_to_uint(pid_kd, 5, 0, 16))

        position_cmd_can_id = self.motor_can_id | (torque_scaled << 8) | (Robstride_Msg_Enum.MOTOR_CTRL.value << 24)
        self.can_transport.send(can_id=position_cmd_can_id, data=data, is_extended_id=True)

    def get_motor_feedback_frame(self) -> FeedbackResp:
        # feedback frame puts error reporting data in the CAN_ID - so we need to listen for a range of IDs instead of a specific one
        ret = FeedbackResp()
        can_id, message = self.transport.recv_in_range(
            can_id_min=(Robstride_Msg_Enum.MOTOR_FEEDBACK << 28), 
            can_id_max=((Robstride_Msg_Enum.MOTOR_FEEDBACK + 1 ) << 28) - 1, 
            is_extended_id=True
        )
        if message == None:
            return ret

        error_bits = (can_id >> 16) & 0x3F
        for fault in Robstride_Fault_Enum:
            if error_bits & (1 << fault.value):
                ret.errors.append(fault)

        ret.mode = Robstride_Motor_Mode_Enum((can_id >> 22) & 0x3)

        ret.angle_deg = self._radians_to_deg(self.scale_to_float(struct.unpack("<H", message[0:2]), 16, 4 * math.pi, -4 * math.pi)[0])
        ret.velocity_rads = self.scale_to_float(struct.unpack("<H", message[2:4])[0], 16, -44, 44)
        ret.torque_nm = self.scale_to_float(struct.unpack("<H", message[4:6])[0], 16, -17, 17)
        ret.temp_c = self.scale_to_float(struct.unpack("<H", message[6:])[0] / 10, 16, 0, 2 ** 16 / 2)

        return ret

    def get_fault_feedback_frame(self) -> Robstride_Fault_Frame_Enum:
        fault_feedback_frame_id = self.motor_can_id | (self.host_can_id << 8) | (Robstride_Msg_Enum.FAULT_FEEDBACK << 24)
        fault_frame = self._read_frame(msg_id=fault_feedback_frame_id)
        fault_bits = struct.unpack("<H", fault_frame[0:4])
        for fault in Robstride_Fault_Frame_Enum:
            if fault_bits & (1 << fault.value):
                return fault

    def get_broadcast_frame(self):
        broadcast_can_id = 0xFE | (self.motor_can_id << 8)
        return self._read_frame(msg_id=broadcast_can_id)

    def _send_frame(self, msg_type: Robstride_Msg_Enum, data: bytes):
        extended_can_id = self.motor_can_id | (self.host_can_id << 8) | (msg_type.value << 24)
        self.can_transport.send(can_id=extended_can_id, data=data, is_extended_id=True)

    def _read_frame(self, msg_id: int, timeout_s: int = 1) -> bytes:
        message: can_transport.CAN_Message = self.can_transport.recv(can_id=msg_id, is_extended_id=True, timeout_s=timeout_s)
        if message != None:
            return message.data
        
    @staticmethod
    def _deg_to_radians(deg: float):
        return (deg * math.pi) / 180
    
    @staticmethod
    def _radians_to_deg(rad: float):
        return (rad * 180) / math.pi
                

if __name__ == "__main__":
    # pcan_transport = can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS1, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    can_channel = "can1"
    usb2can_transport = USB2CANX2(channel=can_channel, baud_rate=1000000)
    
    for i in range(1):
        print(i)
        robstride = Robstride(host_can_id=0xFD, motor_can_id=127, can_transport=usb2can_transport)
        device_id = robstride.get_device_id()
        if device_id != None:
            print(device_id)
            break

    robstride.enable_motor()
    robstride.move_to_position(
        torque_Nm=0.1, 
        target_angle_deg=300,
        angular_vel_rads=0.5,
    )

    control_mode = robstride.read_single_param(Robstride_Param_Enum.RUN_MODE)
    print(control_mode)
    usb2can_transport.close_channel(can_channel)

