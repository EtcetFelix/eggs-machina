import os
import sys
from typing import Any, List
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.can import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import can_transport
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum
import time

def set_position(leader: Robstride, follower: Robstride):
    pos = leader.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)
    follower.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, pos)

def instantiate_transport() -> Transport:
    channel = "can1"
    transport = USB2CANX2(channel=channel, baud_rate=1000000)
    return transport, channel

def shutdown_transport(transport: Transport, can_channel):
    """Gracefully shutdown the transport channel."""
    transport.close_channel(can_channel)


def instantiate_robots() -> List[Any]:
    """Define and instantiate all robots used during teleop."""
    transport =  can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS2, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    transport2 =  can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS1, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    host_can_id = 150
    # TODO: set control mode to position
    # TODO: enable motor
    leader = Robstride(transport, host_can_id, motor_can_id=127)
    follower = Robstride(transport2, host_can_id, motor_can_id=127)
    follower.write_single_param(Robstride_Param_Enum.RUN_MODE, 1)
    leader.stop_motor()
    follower.enable_motor()   
    set_position(leader, follower)
    time.sleep(1)
    return [leader, follower]


def start_teleop(leader: Robstride, follower: Robstride):
    """Trigger teleop when user input is entered."""
    teleop(leader, follower)


def teleop(leader: Robstride, follower: Robstride):
    """Start tele-operation."""
    while True:
        follower.enable_motor()
        set_position(leader, follower)
        time.sleep(0.05)


def main():
    robots = instantiate_robots()
    leader = robots[0]
    follower = robots[1]
    start_teleop(leader, follower)



def shutdown_robots_gracefully(robots: List[Any]):
    """Gracefully turn off all robots."""
    pass


if __name__ == "__main__":
    transport, channel = instantiate_transport()
    try:
        main()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        shutdown_robots_gracefully(robots)
        shutdown_transport(transport, channel)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
