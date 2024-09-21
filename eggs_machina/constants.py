import os

DELTA_TIME_STEP = 0.02

DATA_DIR = os.getenv("DATA_DIR", default="~/.eggs_machina/data")

TASK_CONFIGS = {
    "crack_an_egg": {
        "dataset_dir": DATA_DIR + "/crack_an_egg",
        "num_episodes": 50,
        "episode_len": 1000,
        "camera_names": [],
    },
}
