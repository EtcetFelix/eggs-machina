from eggs_machina.data.data_utils import LEADER_ACTION_HDF5_GROUP, create_dataset_path, save_to_hdf5, save_to_json
import numpy as np
from eggs_machina.constants import DATA_DIR
from eggs_machina.data.data_collected import DataSaved



def convert_to_float(data):
  """Converts a list of np.float64 values to Python float values."""
  return [float(x) for x in data]


def generate_servo_radian_data(x, signal_type='sine'):
  """Generates radian data from indices 0 to x for controlling a servo.

  Args:
    x: The upper limit of the index range (exclusive).
    signal_type: The type of signal to generate ('sine', 'triangle', 'sawtooth').

  Returns:
    A NumPy array of radian data suitable for servo control.
  """

  indices = np.arange(x)

  if signal_type == 'sine':
    # Sine wave with amplitude pi/4 and frequency 0.1
    frequency = 0.1
    data = (np.pi / 4) * np.sin(frequency * indices)  
  elif signal_type == 'triangle':
    # Triangle wave with amplitude pi/4 and period 40
    period = 40
    data = (np.pi / 4) * (2 * np.abs((indices / period) - np.floor((indices / period) + 0.5)) - 1)
  elif signal_type == 'sawtooth':
    # Sawtooth wave with amplitude pi/4 and period 20
    period = 20
    data = (np.pi / 4) * (2 * (indices / period - np.floor(indices / period + 0.5)))
  else:
    raise ValueError("Invalid signal_type. Choose from 'sine', 'triangle', 'sawtooth'")
  data = convert_to_float(data)
  return data


def create_data(num_timesteps: int):
    data_dict = {
        LEADER_ACTION_HDF5_GROUP: []
    }
    data_x_motor = generate_servo_radian_data(num_timesteps, 'sine')
    data_y_motor = [0 for t in range(num_timesteps)]
    data_z_motor = [0 for t in range(num_timesteps)]
    # Zip the data into a list of tuples
    motor_data = list(zip(data_x_motor, data_y_motor, data_z_motor))
    data_dict[LEADER_ACTION_HDF5_GROUP] = motor_data
    return data_dict

if __name__ == '__main__':
    num_timesteps = 50
    hdf5_dataset_path = create_dataset_path(DATA_DIR, "synthetic.hdf5", overwrite=True)
    json_dataset_path = create_dataset_path(DATA_DIR, "synthetic.json", overwrite=True)
    data = create_data(num_timesteps)
    save_to_json(data, json_dataset_path)
    save_to_hdf5(data, hdf5_dataset_path, [], num_timesteps, values_to_save=[DataSaved.LEADER_ACTION])
    print("done")

