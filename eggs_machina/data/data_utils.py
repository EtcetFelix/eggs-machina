"""Data saving utilty functions."""
import os
import time
from typing import Any, Dict, List
from eggs_machina.data.data_collected import DataSaved
import json

import h5py

from eggs_machina.constants import NUM_JOINTS_ON_ROBOT, NUM_LEADER_ROBOTS

TOTAL_NUM_LEADER_JOINTS = NUM_LEADER_ROBOTS * NUM_JOINTS_ON_ROBOT


FOLLOWER_POSITION_HDF5_GROUP = f"/observations/{DataSaved.FOLLOWER_POSITION.value}"
FOLLOWER_VELOCITY_HDF5_GROUP = f"/observations/{DataSaved.FOLLOWER_VELOCITY.value}"
FOLLOWER_EFFORT_HDF5_GROUP = f"/observations/{DataSaved.FOLLOWER_EFFORT.value}"
LEADER_ACTION_HDF5_GROUP = f"/{DataSaved.LEADER_ACTION.value}"
IMAGES_HDF5_GROUP = f"/observations/{DataSaved.IMAGES.value}/"


def prepare_data_for_export(camera_names, actions, timesteps) -> Dict[str, Any]:
    data_dict = {
        FOLLOWER_POSITION_HDF5_GROUP: [],
        FOLLOWER_VELOCITY_HDF5_GROUP: [],
        FOLLOWER_EFFORT_HDF5_GROUP: [],
        LEADER_ACTION_HDF5_GROUP: [],
    }
    for cam_name in camera_names:
        data_dict[f"{IMAGES_HDF5_GROUP}{cam_name}"] = []

    while actions:
        action = actions.pop(0)
        timestep = timesteps.pop(0)
        data_dict[FOLLOWER_POSITION_HDF5_GROUP].append(timestep.observation[DataSaved.FOLLOWER_POSITION.value])
        data_dict[FOLLOWER_VELOCITY_HDF5_GROUP].append(timestep.observation[DataSaved.FOLLOWER_VELOCITY.value])
        data_dict[FOLLOWER_EFFORT_HDF5_GROUP].append(timestep.observation[DataSaved.FOLLOWER_EFFORT.value])
        data_dict[LEADER_ACTION_HDF5_GROUP].append(action)
        for cam_name in camera_names:
            data_dict[f"{IMAGES_HDF5_GROUP}{cam_name}"].append(
                timestep.observation[DataSaved.IMAGES.value][cam_name]
            )
    return data_dict

def save_to_json(data_dict: Dict[str, Any], dataset_path: str):
    """Save data_dict to a JSON file at dataset_path."""
    t0 = time.time()
    with open(dataset_path, 'w') as f:
        json.dump(data_dict, f, indent=4)
    print(f"Saving JSON: {time.time() - t0:.1f} secs")


def create_dataset_path(dataset_dir, dataset_filename: str, overwrite: bool) -> str:
    """Create the path in the filesystem for the dataset."""
    if not os.path.isdir(dataset_dir):
        os.makedirs(dataset_dir)
    dataset_path = os.path.join(dataset_dir, dataset_filename)
    if os.path.isfile(dataset_path) and not overwrite:
        print(
            f"Dataset already exist at \n{dataset_path}\nHint: set overwrite to True."
        )
        raise SystemExit()
    return dataset_path


def save_to_hdf5(
    data_dict: Dict[str, Any],
    dataset_path: str,
    camera_names: List[str],
    max_timesteps: int,
    values_to_save: List[DataSaved]
):
    """Save data_dict to HDF5 file at dataset_path."""
    # HDF5
    t0 = time.time()
    with h5py.File(dataset_path, "w", rdcc_nbytes=1024**2 * 2) as root:
        root.attrs["sim"] = False
        obs = root.create_group("observations")
        if DataSaved.IMAGES in values_to_save:
            image = obs.create_group(DataSaved.IMAGES.value)
            for cam_name in camera_names:
                _ = image.create_dataset(
                    cam_name,
                    (max_timesteps, 480, 640, 3),
                    dtype="uint8",
                    chunks=(1, 480, 640, 3),
                )
                # compression='gzip',compression_opts=2,)
                # compression=32001, compression_opts=(0, 0, 0, 0, 9, 1, 1), shuffle=False)
        if DataSaved.FOLLOWER_POSITION in values_to_save:
            _ = obs.create_dataset(DataSaved.FOLLOWER_POSITION.value, (max_timesteps, TOTAL_NUM_LEADER_JOINTS))
        if DataSaved.FOLLOWER_VELOCITY in values_to_save: 
            _ = obs.create_dataset(DataSaved.FOLLOWER_VELOCITY.value, (max_timesteps, TOTAL_NUM_LEADER_JOINTS))
        if DataSaved.FOLLOWER_EFFORT in values_to_save:
            _ = obs.create_dataset(DataSaved.FOLLOWER_EFFORT.value, (max_timesteps, TOTAL_NUM_LEADER_JOINTS))
        if DataSaved.LEADER_ACTION in values_to_save:
            _ = root.create_dataset(DataSaved.LEADER_ACTION.value, (max_timesteps, TOTAL_NUM_LEADER_JOINTS))

        for name, array in data_dict.items():
            try:
                dataset = root[name]
                dataset[...] = array # type: ignore
            except KeyError:
                print(f"{name} not saved to dataset because not in values_to_save")
    print(f"Saving: {time.time() - t0:.1f} secs")
    print(f"Saved to path {dataset_path}")


def load_hdf5(dataset_dir, dataset_name, values_to_load: List[DataSaved]):
    dataset_path = os.path.join(dataset_dir, dataset_name + '.hdf5')
    if not os.path.isfile(dataset_path):
        print(f'Dataset does not exist at \n{dataset_path}\n')
        exit()

    qpos, qvel, effort, action, image_dict = None, None, None, None, None
    with h5py.File(dataset_path, 'r') as root:
        is_sim = root.attrs['sim']
        if DataSaved.FOLLOWER_POSITION in values_to_load:
            qpos = root[FOLLOWER_POSITION_HDF5_GROUP][()]
        if DataSaved.FOLLOWER_VELOCITY in values_to_load:
            qvel = root[FOLLOWER_VELOCITY_HDF5_GROUP][()]
        if DataSaved.FOLLOWER_EFFORT in values_to_load:
            effort = root[FOLLOWER_EFFORT_HDF5_GROUP][()]
        if DataSaved.LEADER_ACTION in values_to_load:
            action = root[LEADER_ACTION_HDF5_GROUP][()]
        if DataSaved.IMAGES in values_to_load:
            image_dict = dict()
            for cam_name in root[IMAGES_HDF5_GROUP].keys():
                image_dict[cam_name] = root[f'{IMAGES_HDF5_GROUP}{cam_name}'][()]

    return qpos, qvel, effort, action, image_dict
