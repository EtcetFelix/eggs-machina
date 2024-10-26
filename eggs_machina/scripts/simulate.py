import mujoco as mj
import mujoco.viewer
import os

def display_urdf(urdf_path):
  """
  Displays a URDF file in a MuJoCo simulation without running the simulation.

  Args:
    urdf_path: Path to the URDF file.
  """

  # Get the full path to the URDF file
  urdf_path = os.path.abspath(urdf_path)

  # Load the model from the URDF
  model = mj.MjModel.from_xml_path(urdf_path)
  data = mj.MjData(model)

  # Launch the passive viewer
  with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
      viewer.sync()  # Update the viewer

if __name__ == "__main__":
  urdf_file = "C:/Users/Alan/Desktop/eggs-machina-stl/robot/meshes/assembly.urdf"  # Replace with your URDF file path
  display_urdf(urdf_file)