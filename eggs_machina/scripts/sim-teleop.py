import os
import sys
from typing import Any, List
import time
import mujoco
import mujoco.viewer
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.can import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import can_transport
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum
import time
from eggs_machina.simulation.interface import SimulatedRobot

def set_position(leader: Robstride, follower: Robstride):
    pos = leader.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)
    follower.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, pos)


def get_real_robot_pos(leader: Robstride):
    pos = leader.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)

def map_joint_positions(real_robot_joint_positions):
    mujoco_joint_positions = [] 
    return real_robot_joint_positions

def instantiate_robots(data, model) -> List[Any]:
    """Define and instantiate all robots used during teleop."""
    transport =  can_transport.PCAN(channel=PCANBasic.PCAN_USBBUS2, baud_rate=can_transport.CAN_Baud_Rate.CAN_BAUD_1_MBS)
    host_can_id = 150
    # TODO: set control mode to position
    # TODO: enable motor
    leader = Robstride(transport, host_can_id, motor_can_id=127)
    follower = SimulatedRobot(model, data)
    leader.stop_motor()
    # set_position(leader, follower)
    time.sleep(1)
    return [leader, follower]

def teleop(leader: Robstride, follower: Robstride, model, data):
    """Start tele-operation."""
    with mujoco.viewer.launch_passive(m, d) as viewer:
        while viewer.is_running():
            step_start = time.time()
            real_robot_joint_positions = get_real_robot_pos(leader)
            mapped_joint_positions = map_joint_positions(real_robot_joint_positions)
            d.qpos[:] = mapped_joint_positions  
            mujoco.mj_step(m, d)
            viewer.sync()
            # Rudimentary time keeping, will drift relative to wall clock.
            time_until_next_step = m.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)


def main(leader, follower, model, data):    
    teleop(leader, follower, model, data)



def shutdown_robots_gracefully(robots: List[Any]):
    """Gracefully turn off all robots."""
    pass


if __name__ == "__main__":
    m = mujoco.MjModel.from_xml_path('simulation/low_cost_robot/scene.xml')
    d = mujoco.MjData(m)
    robots = instantiate_robots(d, m)
    leader = robots[0]
    follower = robots[1]
    try:
        main(leader, follower, m, d)
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        shutdown_robots_gracefully(robots)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
