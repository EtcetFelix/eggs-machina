"""Collect data from teleoperation."""

from eggs_machina.utils.teleop import Teleoperator
import dm_env
from eggs_machina.utils.robstride_robot import RoboRob
from typing import Dict
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from numpy.typing import NDArray
import numpy as np
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum, Robstride_Control_Modes


TIMESTEP_LENGTH = 0.05

class DataCollectionTeleop(Teleoperator):
    def __init__(self, leader: RoboRob, follower: RoboRob, joint_map: Dict[Robstride, Robstride]):
        super().__init__(leader, follower, joint_map) 

    def get_leader_action(self) -> Dict[Robstride, float]:
        """Get the action of the leader bot."""
        leader_positions: Dict[Robstride, float] = self.leader.read_position()
        return leader_positions

    def _set_position(self, leader_positions: Dict[Robstride, float]):
        for leader_robstride, position in leader_positions.items():
            follower_robstride = self.joint_map.get(leader_robstride, None)
            if follower_robstride == None:
                self.stop()
                raise ValueError
            follower_robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, position)
    
    def follower_observation(self):
        """Return the real observed action of follower."""
        # TODO: Get data feedback from follower and return
        pass

    def get_reward(self):
        return 0

    def step(self, action: NDArray[np.int32]) -> dm_env.TimeStep:
        """Set action of the follower bot and save its real returned actions."""
        leader_positions = action
        self._set_position(leader_positions)
        return dm_env.TimeStep(
            step_type=dm_env.StepType.MID,
            reward=self.get_reward(),
            discount=None,
            observation=self.follower_observation())

# TODO: add reset function
