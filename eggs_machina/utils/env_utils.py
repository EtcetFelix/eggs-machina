import collections
import time

import dm_env
import numpy as np
from numpy.typing import NDArray

from eggs_machina.constants import (
    DELTA_TIME_STEP,
    GRIPPER_INDEX,
    NUM_JOINTS_ON_ROBOT,
    PUPPET_GRIPPER_POSITION_NORMALIZE_FN,
)


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
        setup_robots=True,
    ):
        if setup_robots:
            self.setup_robots()

        self.robot_manager = None
        self.recorders = {}

    def setup_robots(self):
        pass

    def get_qpos(self) -> NDArray[np.float64]:
        positions = []
        for recorder in self.recorders.values():
            recorder.update_puppet_state()
            qpos_raw = recorder.qpos
            qpos = qpos_raw[:NUM_JOINTS_ON_ROBOT]
            gripper_qpos = [
                PUPPET_GRIPPER_POSITION_NORMALIZE_FN(qpos_raw[GRIPPER_INDEX])
            ]
            positions.append(qpos)
        return np.concatenate(positions)

    def get_observation(self):
        obs = collections.OrderedDict()
        obs["qpos"] = self.get_qpos()
        return obs

    def get_reward(self):
        return 0

    def reset(self, fake=False):
        pass

    def step(self, action):
        puppet_robots = []

        # Set the goal pos for all puppet bots
        for puppet_index, puppet_bot_name in enumerate(puppet_robots):
            joint_index = NUM_JOINTS_ON_ROBOT * puppet_index
            action_for_puppet = action[joint_index : joint_index + NUM_JOINTS_ON_ROBOT]
            # TODO: set goal position for robot

        time.sleep(DELTA_TIME_STEP)
        return dm_env.TimeStep(
            step_type=dm_env.StepType.MID,
            reward=self.get_reward(),
            discount=None,
            observation=self.get_observation(),
        )

    def get_action(self) -> NDArray[np.int32]:
        leader_robots = []
        action = np.zeros((NUM_JOINTS_ON_ROBOT) * len(leader_robots), dtype=np.int32)

        # Get all the leader robot actions
        for robot_index, leader_robot in enumerate(leader_robots):
            # TODO: get robot action
            continue

        return action


def make_real_env(robot_manager, setup_robots=True) -> RealEnv:
    env = RealEnv(robot_manager, setup_robots)
    return env
