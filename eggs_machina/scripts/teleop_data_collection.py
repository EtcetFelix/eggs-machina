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
from eggs_machina.utils.data_collection_teleop import DataCollectionTeleop



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

    teleoperator = DataCollectionTeleop(
        leader=leader_robot,
        follower=follower_robot,
        joint_map={
            leader_x: follower_x,
            leader_y: follower_y
        }
    )

    # teleoperator.run(delay_ms=0.05)
    print("Started, GO!!!")
    teleoperator.follower.enable_motors()
    teleoperator.leader.stop_motors()
    teleoperator.follower.set_control_mode(Robstride_Control_Modes.POSITION_MODE)
    leader_actions = []
    timestamp_history = []
    timesteps = []
    for _ in range(100):
        t0 = time.time()
        action = teleoperator.get_leader_action()
        t1 = time.time()
        timestep = teleoperator.step(action)
        t2 = time.time()
        timesteps.append(timestep)
        leader_actions.append(action)
        timestamp_history.append([t0, t1, t2])
        time.sleep(0.05)
    # TODO: write commands to do teleop with data collection class
    # TODO: use data utils to save data properly
    # input("Press Enter to end teleop...")
    teleoperator.stop()






