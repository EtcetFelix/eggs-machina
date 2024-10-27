import numpy as np
import os
import collections
import matplotlib.pyplot as plt
from dm_control import mujoco
from dm_control.rl import control
from dm_control.suite import base
from eggs_machina.constants import XML_DIR


class TransferCubeTask(base.Task):
    def __init__(self, random=None):
        super().__init__(random=random)
        self.max_reward = 4
    
    def before_step(self, action, physics):
        """Define the environment action to take."""
        robot_action = action
        super().before_step(robot_action, physics)
        return

    def initialize_episode(self, physics):
        """Sets the state of the environment at the start of each episode."""
        super().initialize_episode(physics)

    def get_observation(self, physics):
        obs = collections.OrderedDict()
        self.get_qpos(physics)
        return obs
    
    @staticmethod
    def get_qpos(physics):
        pass

    
    def get_reward(self, physics):
        # return whether left gripper is holding the box
        return 0


def make_sim_env(delta_time: float):
    """
    Environment for simulated robot.
    """
    xml_path = os.path.join(XML_DIR, f'transfer_cube.xml')
    physics = mujoco.Physics.from_xml_path(xml_path)
    task = TransferCubeTask(random=False)
    env = control.Environment(physics, task, time_limit=20, control_timestep=delta_time,
                                n_sub_steps=None, flat_observation=False)
    return env


if __name__ == '__main__':
    # phys = make_sim_env
    env = make_sim_env()
    # pixels = phys.render()
    # plt.imshow(pixels)
    # plt.axis('off')  # Hide axes
    # plt.show()