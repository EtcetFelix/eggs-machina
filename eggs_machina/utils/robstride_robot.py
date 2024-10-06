from typing import Dict
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.transport.base import Transport
from eggs_machina.hw_drivers.system.robstride.robstride_types import Robstride_Param_Enum, Robstride_Control_Modes



class RoboRob():
    def __init__(self, servos: Dict[int, Robstride]):
        """
        Class to handle multiple robstride servos.

        :param servos: dictionary of servos where key is the servo's can id and value 
        is an instance of the Robstride class.
        """
        self.servos = servos


    def read_position(self) -> Dict[Robstride, float]:
        positions = {}
        for can_id, servo in self.servos.items():
            positions[servo] = servo.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)
        return positions


    def set_position(self, positions: Dict[int, float]):
        """
        Set the positions of the servos.
        
        :param positions: Key is the can_id of servo to set position of, value is the position in radians.
        """
        for can_id, servo in self.servos.items():
            position_to_set = positions[can_id]
            self.servos[can_id].write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, position_to_set)


    def stop_motors(self):
        for can_id, servo in self.servos.items():
            servo.stop_motor()


    def enable_motors(self):
        for can_id, servo in self.servos.items():
            servo.enable_motor()


    def set_control_mode(self, control_mode: Robstride_Control_Modes):
        for can_id, servo in self.servos.items():
            servo.write_single_param(Robstride_Param_Enum.RUN_MODE, control_mode.value)

    
    def read_control_mode(self):
        control_modes = {}
        for can_id, servo in self.servos.items():
            control_modes[can_id] = servo.read_single_param(Robstride_Param_Enum.RUN_MODE)
        return control_modes
