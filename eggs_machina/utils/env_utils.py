import collections
import time

import dm_env

# import IPython
# import matplotlib.pyplot as plt
import numpy as np
from minialoha.utils.constants import (
    DELTA_TIME_STEP,
    GRIPPER_INDEX,
    NUM_JOINTS_ON_ROBOT,
    PUPPET_GRIPPER_POSITION_NORMALIZE_FN,
)
from minialoha.utils.robot_manager import RobotManager

# from interbotix_xs_modules.arm import InterbotixManipulatorXS
# from interbotix_xs_msgs.msg import JointSingleCommand
from minialoha.utils.robot_recorder import (
    Recorder,
)
from minialoha.utils.robot_utils import (
    # ImageRecorder,
    # move_arms,
    # move_grippers,
    # setup_master_bot,
    setup_puppet_bot,
)
from numpy.typing import NDArray

# e = IPython.embed


class RealEnv:
    """
    Environment for real robot bi-manual manipulation
    Action space:      [left_arm_qpos (6),             # absolute joint position
                        left_gripper_positions (1),    # normalized gripper position (0: close, 1: open)
                        right_arm_qpos (6),            # absolute joint position
                        right_gripper_positions (1),]  # normalized gripper position (0: close, 1: open)

    Observation space: {"qpos": Concat[ left_arm_qpos (6),          # absolute joint position
                                        left_gripper_position (1),  # normalized gripper position (0: close, 1: open)
                                        right_arm_qpos (6),         # absolute joint position
                                        right_gripper_qpos (1)]     # normalized gripper position (0: close, 1: open)
                        "qvel": Concat[ left_arm_qvel (6),         # absolute joint velocity (rad)
                                        left_gripper_velocity (1),  # normalized gripper velocity (pos: opening, neg: closing)
                                        right_arm_qvel (6),         # absolute joint velocity (rad)
                                        right_gripper_qvel (1)]     # normalized gripper velocity (pos: opening, neg: closing)
                        "images": {"cam_high": (480x640x3),        # h, w, c, dtype='uint8'
                                   "cam_low": (480x640x3),         # h, w, c, dtype='uint8'
                                   "cam_left_wrist": (480x640x3),  # h, w, c, dtype='uint8'
                                   "cam_right_wrist": (480x640x3)} # h, w, c, dtype='uint8'
    """

    def __init__(
        self,
        robot_manager: RobotManager,
        setup_robots=True,
    ):
        if setup_robots:
            self.setup_robots()

        self.robot_manager = robot_manager
        self.recorders = {}
        for robot_name in robot_manager.puppet_robot_names:
            self.recorders[robot_name] = Recorder(robot_name, self.robot_manager)

    def setup_robots(self):
        setup_puppet_bot(self.puppet_bot_left)
        setup_puppet_bot(self.puppet_bot_right)

    def get_qpos(self) -> NDArray[np.float64]:
        positions = []
        for recorder in self.recorders.values():
            recorder.update_puppet_state()
            qpos_raw = recorder.qpos
            qpos = qpos_raw[:NUM_JOINTS_ON_ROBOT]
            gripper_qpos = [
                PUPPET_GRIPPER_POSITION_NORMALIZE_FN(qpos_raw[GRIPPER_INDEX])
            ]  # this is position not joint
            positions.append(qpos)
            # positions.append(gripper_qpos)
        return np.concatenate(positions)

    def get_observation(self):
        obs = collections.OrderedDict()
        obs["qpos"] = self.get_qpos()
        return obs

    def get_reward(self):
        return 0

    def reset(self, fake=False):
        if not fake:
            # Reboot puppet robot gripper motors
            self.puppet_bot_left.dxl.robot_reboot_motors("single", "gripper", True)
            self.puppet_bot_right.dxl.robot_reboot_motors("single", "gripper", True)
            self._reset_joints()
            self._reset_gripper()
        return dm_env.TimeStep(
            step_type=dm_env.StepType.FIRST,
            reward=self.get_reward(),
            discount=None,
            observation=self.get_observation(),
        )

    def step(self, action):
        puppet_robots = self.robot_manager.puppet_robot_names
        state_len = int(len(action) / len(puppet_robots))

        # Set the goal pos for all puppet bots
        for puppet_index, puppet_bot_name in enumerate(puppet_robots):
            joint_index = NUM_JOINTS_ON_ROBOT * puppet_index
            action_for_puppet = action[joint_index : joint_index + NUM_JOINTS_ON_ROBOT]
            self.robot_manager.set_robot_goal_pos(
                puppet_bot_name, action_for_puppet[:NUM_JOINTS_ON_ROBOT]
            )

        time.sleep(DELTA_TIME_STEP)
        return dm_env.TimeStep(
            step_type=dm_env.StepType.MID,
            reward=self.get_reward(),
            discount=None,
            observation=self.get_observation(),
        )

    def get_action(self) -> NDArray[np.int32]:
        leader_robots = self.robot_manager.leader_robot_names
        action = np.zeros((NUM_JOINTS_ON_ROBOT) * len(leader_robots), dtype=np.int32)

        # Get all the leader robot actions
        for robot_index, leader_robot in enumerate(leader_robots):
            robot_action = self.robot_manager.get_robot_pos(leader_robot)[
                :NUM_JOINTS_ON_ROBOT
            ]
            # Update the list of joint positions to the action array
            joint_index = NUM_JOINTS_ON_ROBOT * robot_index
            action[joint_index : NUM_JOINTS_ON_ROBOT + joint_index] = robot_action

        return action


def make_real_env(robot_manager: RobotManager, setup_robots=True) -> RealEnv:
    env = RealEnv(robot_manager, setup_robots)
    return env
