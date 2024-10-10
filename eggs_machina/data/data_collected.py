"""Data definitions."""
from enum import Enum

class DataSaved(Enum):
    """Define what type of data will be saved and fed to ai model."""
    FOLLOWER_POSITION = "qpos"
    FOLLOWER_EFFORT = "effort"
    FOLLOWER_VELOCITY = "qvel"
    IMAGES = "images"
    LEADER_ACTION = "action"