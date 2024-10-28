"""Collect data from teleoperation."""

from eggs_machina.utils.teleop import Teleoperator
import dm_env
from eggs_machina.utils.robstride_robot import RoboRob
from typing import Dict, Literal, Any, List
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from numpy.typing import NDArray
import numpy as np
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum, Robstride_Control_Modes
import time
import collections
from eggs_machina.data.data_collected import DataSaved
from eggs_machina.data.image_collection import ImageCollector

TIMESTEP_LENGTH = 0.05

class DataCollectionTeleop(Teleoperator):
    def __init__(self, leader: RoboRob, follower: RoboRob, joint_map: Dict[Robstride, Robstride], with_cameras: bool=False):
        super().__init__(leader, follower, joint_map) 
        camera_names = {"camera1": 4}
        self.image_collector = ImageCollector(camera_names)
        self.with_cameras = with_cameras
        # TODO: Add effort (milliamps), and velocity (rads/second)
    
    def run(self, delay_s: int, num_timesteps: int):
        leader_actions = []
        timestamp_history = []
        timesteps = []
        if self.with_cameras:
            self.image_collector.start_cameras()
        for _ in range(num_timesteps):
            t0 = time.time()
            action = self._get_leader_action()
            t1 = time.time()
            timestep = self._step(action)
            t2 = time.time()
            timesteps.append(timestep)
            leader_action_by_can_id = self._format_leader_action_for_data_saving(action)
            leader_actions.append(leader_action_by_can_id)
            timestamp_history.append([t0, t1, t2])
            time.sleep(delay_s)
        return leader_actions, timestamp_history, timesteps
    
    def _format_leader_action_for_data_saving(self, leader_action: Dict[Robstride, float]) -> Dict[int, float]:
        """Convert keys in leader action feedback to the servo's can id."""
        leader_positions_by_can_id = {}
        for robstride, position in leader_action.items():
            leader_positions_by_can_id[robstride.motor_can_id] = position
        return leader_positions_by_can_id
        

    def _get_leader_action(self) -> Dict[int, float]:
        """
        Get the action of the leader bot.

        :returns lead_positions_by_can_id: keys are the motor can id, values are positions in rads.
        """
        leader_positions: Dict[Robstride, float] = self.leader.read_position()
        return leader_positions

    def _set_position(self, leader_positions: Dict[Robstride, float]):
        for leader_robstride, position in leader_positions.items():
            follower_robstride = self.joint_map.get(leader_robstride, None)
            if follower_robstride == None:
                self.stop()
                raise ValueError
            follower_robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, position)


    def _get_effort(self, feedback_responses: Dict[Robstride, FeedbackResp]) -> List[float]:
        """
        Get effort feedback from every servo in the follower.

        :returns efforts: Torque values in NM from every robstride servo
        """
        #TODO: fix mapping of which servos are which joints and return in correct order
        responses: List[FeedbackResp] = list(feedback_responses.values())
        efforts = [response.torque_nm for response in responses]
        return efforts

    def _get_positions(self, feedback_responses: Dict[Robstride, FeedbackResp]):
        """Get position feedback from every servo in the follower."""
        responses: List[FeedbackResp] = list(feedback_responses.values())
        positions = [response.angle_deg for response in responses]
        #TODO: fix mapping of which servos are which joints and return in correct order
        return positions

    def _get_velocity(self, feedback_responses: Dict[Robstride, FeedbackResp]):
        """Get velocity feedback from every servo in the follower."""
        #TODO: fix mapping of which servos are which joints and return in correct order
        responses: List[FeedbackResp] = list(feedback_responses.values())
        velocities = [response.velocity_rads for response in responses]
        return velocities

    def _get_images(self) -> Dict[str, NDArray[Any]]:
        """Get images from cameras in the follower."""
        images = self.image_collector.get_images()
        return images
    
    def _follower_observation(self) -> collections.OrderedDict:
        """Return the real observed action of follower."""
        observation = collections.OrderedDict()
        follower_feedback = self.follower.get_feedback()
        observation[DataSaved.FOLLOWER_EFFORT.value] = self._get_effort(follower_feedback)
        observation[DataSaved.FOLLOWER_POSITION.value] = self._get_positions(follower_feedback)
        observation[DataSaved.FOLLOWER_VELOCITY.value] = self._get_velocity(follower_feedback)
        if self.with_cameras:
            observation[DataSaved.IMAGES.value] = self._get_images()
        return observation

    def get_reward(self) -> Literal[0]:
        return 0

    def _step(self, action: NDArray[np.int32]) -> dm_env.TimeStep:
        """Set action of the follower bot and save its real returned actions."""
        leader_positions = action
        self._set_position(leader_positions)
        return dm_env.TimeStep(
            step_type=dm_env.StepType.MID,
            reward=self.get_reward(),
            discount=None,
            observation=self._follower_observation())


    def reset(self):
        """Reset teleop environment."""
        pass
