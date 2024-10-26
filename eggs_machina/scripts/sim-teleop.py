import os
import sys
from typing import Any, List, Dict
import time
import mujoco
import mujoco.viewer
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.can import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import can_transport
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2
from eggs_machina.utils.robstride_robot import RoboRob
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum
import time
from eggs_machina.simulation.interface import SimulatedRobot

LEADER_SERVO_IDS = [44, 42, 30]
SIM_MAPPING = {
    LEADER_SERVO_IDS[0]: 1,
    LEADER_SERVO_IDS[1]: 0,
    LEADER_SERVO_IDS[2]: 2
}
HOST_ID = 0xFD


def set_position(leader: RoboRob, model, data):
    pos = leader.read_position()
    mapped_joint_positions = map_joint_positions(pos)
    data.qpos = mapped_joint_positions 


def get_real_robot_pos(leader: Robstride):
    pos = leader.read_single_param()
    return pos

def map_joint_positions(positions: Dict[Robstride, float]):
    """Map the real world joints to the sim joints.
    
    The order of positions of the sim joints is determined by the order 
    in which the joints appear in the urdf. 
    """
    sim_joint_positions = [None for _ in range(len(SIM_MAPPING))]
    for real_servo, position in positions.items():
        sim_joint_index = SIM_MAPPING[real_servo.motor_can_id]
        sim_joint_positions[sim_joint_index] = position
    for index, pos in enumerate(sim_joint_positions):
        if pos == None:
            raise KeyError(f"Sim joint with index {index} was not assigned a position.")
    return sim_joint_positions

def instantiate_robots(data, model) -> List[Any]:
    """Define and instantiate all robots used during teleop."""
    transport = USB2CANX2(channel="can0", baud_rate=1000000)
    leader_servos = {}
    for can_id in LEADER_SERVO_IDS:
        leader_servos[can_id] = Robstride(host_can_id=HOST_ID, motor_can_id=can_id, can_transport=transport)
    leader = RoboRob(leader_servos)
    follower = SimulatedRobot(model, data)
    leader.stop_motors()
    time.sleep(1)

    print(leader.read_position())

    leader.stop_motors()
    time.sleep(0.05)   
    set_position(leader, model, data)
    time.sleep(1)
    return [leader, follower]


def teleop(leader: Robstride, follower: Robstride, model, data):
    """Start tele-operation."""
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.time()
            set_position(leader, model, data)
            mujoco.mj_step(model, data)
            viewer.sync()
            # Rudimentary time keeping, will drift relative to wall clock.
            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)


def main(leader, follower, model, data):    
    teleop(leader, follower, model, data)



def shutdown_robots_gracefully(robots: List[Any]):
    """Gracefully turn off all robots."""
    pass


if __name__ == "__main__":
    m = mujoco.MjModel.from_xml_path('/home/abohannon/code_repos/eggs-machina/eggs_machina/model/meshes/assembly.urdf')
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
