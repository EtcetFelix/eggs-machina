import os
from typing import List

import numpy as np

from eggs_machina.constants import (
    DELTA_TIME_STEP,
    TASK_CONFIGS,
)
from eggs_machina.utils.data_utils import (
    create_dataset_path,
    prepare_data_for_export,
    save_to_hdf5,
)
from eggs_machina.utils.env_utils import make_real_env

TASK_CONFIG = TASK_CONFIGS["crack_an_egg"]


def print_dt_diagnosis(actual_dt_history):
    actual_dt_history = np.array(actual_dt_history)
    get_action_time = actual_dt_history[:, 1] - actual_dt_history[:, 0]
    step_env_time = actual_dt_history[:, 2] - actual_dt_history[:, 1]
    total_time = actual_dt_history[:, 2] - actual_dt_history[:, 0]

    dt_mean = np.mean(total_time)
    dt_std = np.std(total_time)
    freq_mean = 1 / dt_mean
    print(
        f"Avg freq: {freq_mean:.2f} Get action: {np.mean(get_action_time):.3f} Step env: {np.mean(step_env_time):.3f}"
    )
    return freq_mean


def get_auto_index(dataset_dir, dataset_name_prefix="", data_suffix="hdf5"):
    max_idx = 1000
    if not os.path.isdir(dataset_dir):
        os.makedirs(dataset_dir)
    for i in range(max_idx + 1):
        if not os.path.isfile(
            os.path.join(dataset_dir, f"{dataset_name_prefix}episode_{i}.{data_suffix}")
        ):
            return i
    raise Exception(f"Error getting auto index, or more than {max_idx} episodes")


def loop_timesteps(env, max_timesteps):
    timestep = env.reset(fake=True)
    timesteps = [timestep]
    actions = []
    actual_dt_history = []
    for _ in tqdm(range(max_timesteps)):
        t0 = time.time()
        user_action = env.get_action()
        t1 = time.time()
        timestep = env.step(user_action)
        t2 = time.time()
        timesteps.append(timestep)
        actions.append(user_action)
        actual_dt_history.append([t0, t1, t2])
    return actual_dt_history, actions, timesteps


def capture_one_episode(
    dt,
    max_timesteps: int,
    camera_names: List[str],
    dataset_dir,
    dataset_name: str,
    overwrite: bool,
):
    dataset_path = create_dataset_path(dataset_dir, dataset_name + ".hdf5", overwrite)
    env = make_real_env([], setup_robots=False)
    actual_dt_history, actions, timesteps = loop_timesteps(env, max_timesteps)

    data_dict = prepare_data_for_export(camera_names, actions, timesteps)

    save_to_hdf5(data_dict, dataset_path, camera_names, max_timesteps)

    return True


def main():
    """Define the main entrypoint for script."""
    dataset_dir = TASK_CONFIG["dataset_dir"]
    episode_idx = get_auto_index(dataset_dir)
    dataset_name = f"episode_{episode_idx}"
    print(dataset_name + "\n")
    while True:
        is_healthy = capture_one_episode(
            DELTA_TIME_STEP,
            TASK_CONFIG["episode_len"],
            TASK_CONFIG["camera_names"],
            dataset_dir,
            dataset_name,
            True,
        )
        is_healthy = True
        if is_healthy:
            break


if __name__ == "__main__":
    print("Starting main...")
    main()
