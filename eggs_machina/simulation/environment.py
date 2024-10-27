import numpy as np
import os
import collections
import matplotlib.pyplot as plt
from dm_control import mujoco
from dm_control.rl import control
from dm_control.suite import base
from eggs_machina.constants import XML_DIR

def make_sim_env():
    """
    Environment for simulated robot.
    """
    xml_path = os.path.join(XML_DIR, f'transfer_cube.xml')
    physics = mujoco.Physics.from_xml_path(xml_path)
    # task = TransferCubeTask(random=False)
    # env = control.Environment(physics, task, time_limit=20, control_timestep=DT,
    #                             n_sub_steps=None, flat_observation=False)
    # return env
    return physics

if __name__ == '__main__':
    phys = make_sim_env()
    pixels = phys.render()
    plt.imshow(pixels)
    plt.axis('off')  # Hide axes
    plt.show()