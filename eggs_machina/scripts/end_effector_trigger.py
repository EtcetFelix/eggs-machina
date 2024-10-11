"""Testing n development of end effector."""
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.system.robstride.robstride_types import FeedbackResp, Robstride_Fault_Enum, Robstride_Fault_Frame_Enum, Robstride_Motor_Mode_Enum, Robstride_Msg_Enum, Robstride_Param_Enum, Robstride_Control_Modes
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2


CAN_ID = 30

def read_position(servo):
    servo.read_single_param(Robstride_Param_Enum.MECH_POS_END_COIL)

if __name__ == "__main__":
    can_channel = "can0"
    with USB2CANX2(channel=can_channel, baud_rate=1000000) as transport:
        robstride = Robstride(host_can_id=0xFD, motor_can_id=CAN_ID, can_transport=transport)
        print(read_position(robstride))
        robstride.write_single_param(Robstride_Param_Enum.SPEED_KP, 1)
        speed_kp = robstride.read_single_param(Robstride_Param_Enum.SPEED_KP)
        print(f"speed_lkp: {speed_kp}")

        robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_SPEED_LIMIT, 4)
        speed_limit = robstride.read_single_param(Robstride_Param_Enum.POSITION_MODE_SPEED_LIMIT)
        print(f"speed_limit: {speed_limit}")

        robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_CURRENT_LIMIT, .3)
        torque_limit = robstride.read_single_param(Robstride_Param_Enum.POSITION_MODE_CURRENT_LIMIT)
        print(torque_limit)
        robstride.write_single_param(Robstride_Param_Enum.RUN_MODE, Robstride_Control_Modes.POSITION_MODE.value)
        robstride.enable_motor()
        position_to_set = .1
        robstride.write_single_param(Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD, position_to_set)
        robstride.stop_motor()

    