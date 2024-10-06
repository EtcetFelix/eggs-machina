import pytest
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.system.robstride.robstride_types import Robstride_Param_Enum
import time


CAN_CHANNEL = "can0"
MOTOR_ID = 127

def test_get_vbus():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        robstride = Robstride(host_can_id=0xFD, motor_can_id=MOTOR_ID, can_transport=transport)
        bus_voltage = robstride.read_single_param(Robstride_Param_Enum.VBUS_VOLTAGE)
        print(bus_voltage)
        assert bus_voltage is not None, "Failed to read bus_voltage. Check can channel, power, transport device, or device id."


def test_read_run_mode():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        robstride = Robstride(host_can_id=0xFD, motor_can_id=MOTOR_ID, can_transport=transport)
        control_mode = robstride.read_single_param(Robstride_Param_Enum.RUN_MODE)
        print(control_mode)

def test_position_control(robstride: Robstride):
        robstride.write_single_param(Robstride_Param_Enum.RUN_MODE, 1)
        robstride.enable_motor()
        robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, 2)
        feedback = robstride.get_motor_feedback_frame()
        print(feedback)
        time.sleep(1)
        robstride.stop_motor()
        robstride.write_single_param(Robstride_Param_Enum.RUN_MODE, 0)
        pos = robstride.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)
        print(pos)

def test_position_max_speed_limit():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        robstride = Robstride(host_can_id=0xFD, motor_can_id=MOTOR_ID, can_transport=transport)
        max_speed = robstride.read_single_param(Robstride_Param_Enum.POSITION_MODE_SPEED_LIMIT)
        print(max_speed)

def test_read_position():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        robstride = Robstride(host_can_id=0xFD, motor_can_id=MOTOR_ID, can_transport=transport)
        pos = robstride.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)
        print(pos)

if __name__ == "__main__":
    test_get_vbus()
    test_read_run_mode()
    test_position_max_speed_limit()
    test_read_position()