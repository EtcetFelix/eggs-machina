from enum import Enum

class DataSaved(Enum):
    FOLLOWER_POSITION = "qpos"
    FOLLOWER_EFFORT = "effort"
    FOLLOWER_VELOCITY = "qvel"
    IMAGES = "images"
    LEADER_ACTION = "action"