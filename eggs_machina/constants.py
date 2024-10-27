import os
import pathlib

DELTA_TIME_STEP = 0.02

DATA_DIR = os.getenv("DATA_DIR", default="~/.eggs_machina/data")
XML_DIR = str(pathlib.Path(__file__).parent.resolve()) + '/simulation/assets/'

TASK_CONFIGS = {
    "crack_an_egg": {
        "dataset_dir": DATA_DIR + "/crack_an_egg",
        "num_episodes": 50,
        "episode_len": 1000,
        "camera_names": [],
    },
}

NUM_JOINTS_ON_ROBOT = 3
NUM_LEADER_ROBOTS = 1

GRIPPER_INDEX = None  # TODO: Set this to something
PUPPET_GRIPPER_POSITION_NORMALIZE_FN = None  # TODO: Set this to something
