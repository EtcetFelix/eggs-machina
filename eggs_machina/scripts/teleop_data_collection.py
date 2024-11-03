import os
import sys
import threading
import cv2
from typing import Any, List, Dict
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.can import PCANBasic
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.transport.can import can_transport
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum, Robstride_Control_Modes
from eggs_machina.utils.robstride_robot import RoboRob
from eggs_machina.data.data_collected import DataSaved
from eggs_machina.hw_drivers.transport.can.types import CAN_Baud_Rate, CAN_Message
import time
from typing import Dict
from eggs_machina.utils.data_collection_teleop import DataCollectionTeleop
from eggs_machina.data.data_utils import prepare_data_for_export, create_dataset_path, save_to_hdf5, save_to_json

DATASET_DIR = "/home/abohannon/Desktop"
DATASET_FILENAME = "ACT_DATA.hdf5"
JSON_DUMP_FILENAME = "ACT_DATA.json"
WITH_CAMERAS = True
MAIN_CAM_NAME = "main_cam"
IMAGES_HDF5_GROUP = f"/observations/{DataSaved.IMAGES.value}/"

def save_vid_of_images(camera_names: List[str], data_dict: Dict[str, Any], delta_time: float = 0.1, output_folder: str = f"{DATASET_DIR}/output_videos"):
    """
    Saves videos of images extracted from the data dictionary for each camera.

    Args:
        camera_names (List[str]): A list of camera names.
        data_dict (Dict[str, Any]): A dictionary containing image data.
        delta_time (float, optional): The time interval between frames in seconds. Defaults to 0.1.
        output_folder (str, optional): The folder to save the videos. Defaults to "output_videos".
    """
    os.makedirs(output_folder, exist_ok=True)

    for cam_name in camera_names:
        images = data_dict[f"{IMAGES_HDF5_GROUP}{cam_name}"]
        
        # Determine the output video path
        video_path = os.path.join(output_folder, f"{cam_name}_video.mp4")

        # Get the dimensions of the first image
        height, width, layers = images[0].shape

        # Define the video codec (XVID is a common choice)
        fourcc = cv2.VideoWriter_fourcc(*'H264')  # Use mp4v for MP4 format
        video = cv2.VideoWriter(video_path, fourcc, 1/delta_time, (width, height))

        for image in images:
            video.write(image)
            cv2.imshow(f"Camera: {cam_name}", image)
            cv2.waitKey(int(delta_time * 1000))

        cv2.destroyAllWindows()
        video.release()


def sort_actions_by_servo(actions: List[Dict[int, float]], servo_order: List[int]):
  """
  Sorts values from a list of dictionaries based on a given order of servo motor ids.
  In other words, it removes the servo motor ids and rearranges to a given order for each action.
  This is so that we can dictate the order in which we want to save action data.

  Args:
    actions: A list of dictionaries where keys are integers and values are floats.
    order: A list of integers representing the order in which to sort the values.

  Returns:
    A list of lists, where each inner list contains the sorted values 
    from the corresponding dictionary in `actions`.
  """
  result = []
  for action in actions:
    temp = []
    for key in servo_order:
      temp.append(action.get(key))
    result.append(temp)
  return result


if __name__ == "__main__":
    dataset_path = create_dataset_path(DATASET_DIR, DATASET_FILENAME, True)
    json_data_dump_path = create_dataset_path(DATASET_DIR, JSON_DUMP_FILENAME, True)

     # All motors on single CAN transport
    transport = USB2CANX2(channel="can0", baud_rate=1000000)
    host_id = 0xFD

    # Follower motors
    follower_x = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=44)
    follower_y = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=42)
    follower_z = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=30)
    follower_robot = RoboRob(
        servos={
            follower_x.motor_can_id: follower_x,
            follower_y.motor_can_id: follower_y,
            follower_z.motor_can_id: follower_z
        }
    )

    # Leader motors
    leader_x = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=50)
    leader_y = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=40)
    leader_z = Robstride(can_transport=transport, host_can_id=host_id, motor_can_id=23)
    leader_robot = RoboRob(
        servos={
            leader_x.motor_can_id: leader_x,
            leader_y.motor_can_id: leader_y,
            leader_z.motor_can_id: leader_z
        }
    )
    
    teleoperator = DataCollectionTeleop(
        leader=leader_robot,
        follower=follower_robot,
        joint_map={
            leader_x: follower_x,
            leader_y: follower_y,
            leader_z: follower_z
        },
        with_cameras=WITH_CAMERAS,
        cameras={MAIN_CAM_NAME: 4}
    )

    # teleoperator.run(delay_ms=0.05)
    print("Started, GO!!!")
    teleoperator.prepare_servos()
    delay_s = 0.05
    leader_actions, timestamp_history, timesteps = teleoperator.run(delay_s, 100)
    # input("Press Enter to end teleop...")
    teleoperator.stop()
    leader_actions = sort_actions_by_servo(leader_actions, [leader_x.motor_can_id, leader_y.motor_can_id, leader_z.motor_can_id])


    data_dict = prepare_data_for_export([MAIN_CAM_NAME], leader_actions, timesteps)
    save_vid_of_images([MAIN_CAM_NAME], data_dict, delay_s)
    if not WITH_CAMERAS:
        save_to_json(data_dict, json_data_dump_path)


    save_to_hdf5(data_dict, dataset_path, [MAIN_CAM_NAME], 100, [DataSaved.LEADER_ACTION, DataSaved.FOLLOWER_VELOCITY, DataSaved.FOLLOWER_POSITION, DataSaved.FOLLOWER_EFFORT, DataSaved.IMAGES])



