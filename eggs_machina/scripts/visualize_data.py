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

def render_env(images, delta_time):
    cv2.imshow('Environment', images[0])  # Show the first image
    cv2.waitKey(500)
    for image in images:
        cv2.imshow('Environment', image)
        cv2.waitKey(int(delta_time * 1000))  # Wait for the calculated time in milliseconds
    cv2.destroyAllWindows()
    
 
def main():
    dataset_dir = ""
    episode_idx = ""
    dataset_name = "synthetic"

    qpos, qvel, effort, actions, image_dict = load_data(DATA_DIR, dataset_name)

    delta_time = 0.05
    
    env = make_sim_env(delta_time)
    ts = env.reset()
    episode_replay = [ts]
    images=[]
    for action in actions:
        ts = env.step(action)
        images.append(env.physics.render())
    render_env(images, delta_time)
    print("done")
        
    
if __name__ == '__main__':
    main()