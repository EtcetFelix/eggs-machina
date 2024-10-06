"""Test functions for the robstride robot class."""

from eggs_machina.utils.robstride_robot import RoboRob
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2
from eggs_machina.hw_drivers.system.robstride.robstride_types import Robstride_Param_Enum, Robstride_Control_Modes

import time


CAN_CHANNEL = "can0"

CAN_IDS = [42, 44]
HOST_ID = 0xFD

def test_read_positions():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        servos = {}
        for can_id in CAN_IDS:
            servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
        robot = RoboRob(servos)
        print(robot.read_position())
    
def test_enable_motors():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        servos = {}
        for can_id in CAN_IDS:
            servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
        robot = RoboRob(servos)
        robot.enable_motors()

def test_set_control_mode():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        servos = {}
        for can_id in CAN_IDS:
            servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
        robot = RoboRob(servos)
        robot.set_control_mode(Robstride_Control_Modes.POSITION_MODE)


def test_set_positions():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        servos = {}
        for can_id in CAN_IDS:
            servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
        robot = RoboRob(servos)
        positions_to_set = {42: -0.8, 44: -0.472}
        robot.set_position(positions_to_set)

def test_stop_motors():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        servos = {}
        for can_id in CAN_IDS:
            servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
        robot = RoboRob(servos)
        robot.stop_motors()


def test_read_control_modes():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        servos = {}
        for can_id in CAN_IDS:
            servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
        robot = RoboRob(servos)
        print(robot.read_control_mode())




if __name__ == "__main__":
    test_read_positions()
    test_set_control_mode()
    test_read_control_modes()
    test_enable_motors()
    test_set_positions()
    time.sleep(1)
    test_stop_motors()
    test_read_positions()



