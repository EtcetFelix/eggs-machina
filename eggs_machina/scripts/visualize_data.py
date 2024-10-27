import os
import numpy as np
import cv2
import h5py
import argparse

import matplotlib.pyplot as plt
from eggs_machina.simulation.environment import make_sim_env
from eggs_machina.constants import DATA_DIR
from eggs_machina.data.data_utils import load_hdf5
from eggs_machina.data.data_collected import DataSaved


def load_data(dataset_dir, dataset_name):    
    qpos, qvel, effort, action, image_dict = load_hdf5(dataset_dir, dataset_name, [DataSaved.LEADER_ACTION])
    print(qpos)
    return qpos, qvel, effort, action, image_dict

def render_env(env):
    pixels = env.physics.render()
    plt.imshow(pixels)
    plt.axis('off') 
    plt.show()


def main():
    dataset_dir = ""
    episode_idx = ""
    dataset_name = "synthetic"

    qpos, qvel, effort, actions, image_dict = load_data(DATA_DIR, dataset_name)
    print(actions)
    
    # env = make_sim_env()
    # ts = env.reset()
    # episode_replay = [ts]
    # for action in actions:
    #     ts = env.step(action)
        
    
if __name__ == '__main__':
    main()