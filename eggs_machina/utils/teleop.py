"""Teleoperation related code."""
import os
import sys
import threading
from typing import Any, List
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.can import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import can_transport
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum, Robstride_Control_Modes
from eggs_machina.utils.robstride_robot import RoboRob
from eggs_machina.hw_drivers.transport.can.types import CAN_Baud_Rate, CAN_Message
import time
from typing import Dict

class Teleoperator:
    def __init__(self, leader: RoboRob, follower: RoboRob, joint_map: Dict[Robstride, Robstride]):
        self.leader = leader
        self.follower = follower
        self.joint_map = joint_map
        self.run_operation = False
        self.teleop_thread = None

    def run(self, delay_ms: int):
        self.follower.set_control_mode(Robstride_Control_Modes.POSITION_MODE)
        self.follower.enable_motors()
        self.leader.stop_motors()
        self.run_operation = True
        
        if self.teleop_thread is None or not self.teleop_thread.is_alive():
            self.teleop_thread = threading.Thread(target=self._run, args=(delay_ms,), daemon=True)
            self.teleop_thread.start()

    def _run(self, delay_ms: int):
        while self.run_operation:
            self._set_position()
            time.sleep(delay_ms)

    def _set_position(self):
        leader_positions: Dict[Robstride, float] = self.leader.read_position()
        for leader_robstride, position in leader_positions.items():
            follower_robstride = self.joint_map.get(leader_robstride, None)
            if follower_robstride == None:
                self.stop()
                raise ValueError
            follower_robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, position)

    def stop(self):
        self.run_operation = False
        if self.teleop_thread:
            self.teleop_thread.join()

    def __del__(self):
        self.stop()
