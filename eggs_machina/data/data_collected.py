"""Data definitions."""
from enum import Enum

class DataSaved(Enum):
    """Define what type of data will be saved and fed to ai model."""
    FOLLOWER_POSITION = "qpos"
    """Used to specify servo data feedback of positions of follower robot, units are radians."""
    FOLLOWER_EFFORT = "effort"
    """Used to specify servo data feedback of torque for follower robot, units are mA (current)."""
    FOLLOWER_VELOCITY = "qvel"
    """Used to specify servo data feedback of velocity for follower robot, units are radians/second."""
    IMAGES = "images"
    """Used to specify image observations of cameras on the robot."""
    LEADER_ACTION = "action"
    """Used to specify servo data feedback of leader robot, units are radians."""