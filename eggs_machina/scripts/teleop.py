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

LEADER_CHANNEL = "can0"
FOLLOWER_CHANNEL = "can0"

LEADER_SERVO_IDS = [42, 44]
FOLLOWER_SERVO_IDS = [50, 40]

JOINT_MAPPING = {44:50, 42:40}

HOST_ID = 0xFD

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


def convert_leader_to_follower_joints(leader_position: Dict[int, float], servo_joint_mapping: Dict[int, int]) -> Dict[int, float]:
    """
    Figure out what motors on the follower to set positions to.    

    :param servo_joint_mapping: Mapping of what joints on the leader correspond to what joints on the follower.
        Keys are the can ids of the joints on the leader, values are the can id of joints on the follower.
    :returns psoitions_to_set: keys are can ids of follower, values are position value to set
    """
    positions_to_set = {}
    for leader_can_id, position in leader_position.items():
        corresponding_follower_joint_id = servo_joint_mapping[leader_can_id]
        positions_to_set[corresponding_follower_joint_id] = position
    return positions_to_set


def set_position(leader: RoboRob, follower: RoboRob, servo_joint_mapping: Dict[int, int]):
    """
    Set the position of the follower to the position of the leader.
    
    :param servo_joint_mapping: Mapping of what joints on the leader correspond to what joints on the follower.
    Keys are the can ids of the joints on the leader, values are the can id of joints on the follower.
    """
    print()
    pos = leader.read_position()
    print(f"Read pos:{pos}, writing to follower")
    positions_to_set = convert_leader_to_follower_joints(pos, servo_joint_mapping)
    follower.set_position(positions_to_set)


def instantiate_single_transport(channel, baud_rate):
    transport = USB2CANX2(channel=channel, baud_rate=baud_rate)
    transport.open()
    return transport

def instantiate_transports() -> Dict[str, Transport]:
    baud = CAN_Baud_Rate.CAN_BAUD_1_MBS.value
    leader_transport = instantiate_single_transport(channel=LEADER_CHANNEL, baud_rate=baud)
    # follower_transport = instantiate_single_transport(channel=FOLLOWER_CHANNEL, baud_rate=baud)
    follower_transport = leader_transport
    transports = {LEADER_CHANNEL: leader_transport, FOLLOWER_CHANNEL: follower_transport}
    return transports

def shutdown_transports(transports: Dict[str, Transport]):
    """Gracefully shutdown the transport channels."""
    for channel, transport in transports.items():
        transport.close(channel)


def instantiate_robots(transports: Dict[str, Transport]) -> List[Any]:
    """Define and instantiate all robots used during teleop."""
    # transport =  can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS2, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    # transport2 =  can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS1, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    host_can_id = 0xFD
    leader_transport = transports[LEADER_CHANNEL]
    follower_transport = transports[FOLLOWER_CHANNEL]
    leader_servo_ids = LEADER_SERVO_IDS
    follower_servo_ids = FOLLOWER_SERVO_IDS
    leader_servos = {}
    for can_id in leader_servo_ids:
        leader_servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=leader_transport)
    leader = RoboRob(leader_servos)

    follower_servos = {}
    for can_id in follower_servo_ids:
        follower_servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=follower_transport)
    follower = RoboRob(follower_servos)

    print(leader.read_position())
    print(follower.read_position())


    follower.set_control_mode(Robstride_Control_Modes.POSITION_MODE)
    leader.stop_motors()
    follower.enable_motors()
    time.sleep(0.05)   
    set_position(leader, follower, JOINT_MAPPING)
    time.sleep(1)
    follower.stop_motors()
    return [leader, follower]


def start_teleop(leader: Robstride, follower: Robstride):
    """Trigger teleop when user input is entered."""
    teleop(leader, follower)


def teleop(leader: RoboRob, follower: RoboRob):
    """Start tele-operation."""
    while True:
        follower.enable_motors()
        set_position(leader, follower, JOINT_MAPPING)
        time.sleep(0.05)


def main(robots):
    leader = robots[0]
    follower = robots[1]
    start_teleop(leader, follower)


def shutdown_robots_gracefully(robots: List[Any]):
    """Gracefully turn off all robots."""
    for robot in robots:
        robot.stop_motors()


if __name__ == "__main__":
    # All motors on single CAN transport
    transport = USB2CANX2(channel="can0", baud_rate=1000000)
    host_id = 0xFD

    # Follower motors
    follower_x = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=40)
    follower_y = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=50)
    follower_robot = RoboRob(
        servos={
            follower_x.motor_can_id: follower_x,
            follower_y.motor_can_id: follower_y
        }
    )

    # Leader motors
    leader_x = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=42)
    leader_y = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=44)
    leader_robot = RoboRob(
        servos={
            leader_x.motor_can_id: leader_x,
            leader_y.motor_can_id: leader_y
        }
    )

    teleoperator = Teleoperator(
        leader=leader_robot,
        follower=follower_robot,
        joint_map={
            leader_x: follower_x,
            leader_y: follower_y
        }
    )

    teleoperator.run(delay_ms=0.05)
    input("Press Enter to end teleop...")
    teleoperator.stop()






