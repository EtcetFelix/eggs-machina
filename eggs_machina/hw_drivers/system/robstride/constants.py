from ctypes import c_float, c_short, c_ubyte
import numpy as np

from eggs_machina.hw_drivers.system.robstride.robstride_types import Robstride_Param_Enum, Robstride_Param_Type

MAX_FLOAT_32 = np.finfo(np.float32).max
MIN_FLOAT_32 = np.finfo(np.float32).min


ROBSTRIDE_PARMS = {
    Robstride_Param_Enum.RUN_MODE: Robstride_Param_Type("Run_Mode", 0x7005, c_ubyte, 1, 0, 3, True),
    Robstride_Param_Enum.IQ_REF: Robstride_Param_Type("Iq_Ref", 0x7006, c_float, 4, -23, 23, True),
    Robstride_Param_Enum.SPEED_REF: Robstride_Param_Type("Spd_Ref", 0x700A, c_float, 4, -44, 44, True),
    Robstride_Param_Enum.TORQUE_LIMIT: Robstride_Param_Type("Limit_Torque", 0x700B, c_float, 4, 0, 17, True),
    Robstride_Param_Enum.CURRENT_KP: Robstride_Param_Type("Cur_Kp", 0x7010, c_float, 4, MIN_FLOAT_32, MAX_FLOAT_32, True),
    Robstride_Param_Enum.CURRENT_KI: Robstride_Param_Type("Cur_Ki", 0x7011, c_float, 4, MIN_FLOAT_32, MAX_FLOAT_32, True),
    Robstride_Param_Enum.CURRENT_FILTER_GAIN: Robstride_Param_Type("Cur_Fit_Gain", 0x7014, c_float, 4, MIN_FLOAT_32, MAX_FLOAT_32, True),
    Robstride_Param_Enum.POSITION_MODE_ANGLE_CMD: Robstride_Param_Type("Ref", 0x7016, c_float, 4, MIN_FLOAT_32, MAX_FLOAT_32, True),
    Robstride_Param_Enum.POSITION_MODE_SPEED_LIMIT: Robstride_Param_Type("Limit_Spd", 0x7017, c_float, 4, 0, 44, True),
    Robstride_Param_Enum.POSITION_MODE_CURRENT_LIMIT: Robstride_Param_Type("Limit_Cur", 0x7018, c_float, 4, 0, 23, True),
    Robstride_Param_Enum.MECH_POS_END_COIL: Robstride_Param_Type("MechPos", 0x7019, c_float, 4, MIN_FLOAT_32, MAX_FLOAT_32, False),
    Robstride_Param_Enum.IQ_FILTER_VALUE: Robstride_Param_Type("IQF", 0x701A, c_float, 4, -23, 23, False),
    Robstride_Param_Enum.MECH_VEL_END_COIL: Robstride_Param_Type("MechVel", 0x701B, c_float, 4, -44, 44, False),
    Robstride_Param_Enum.VBUS_VOLTAGE: Robstride_Param_Type("VBUS", 0x701C, c_float, 4, MIN_FLOAT_32, MAX_FLOAT_32, False),
    Robstride_Param_Enum.NUM_ROTATIONS: Robstride_Param_Type("Rotation", 0x701D, c_short, 2, -2 ** 15, 2 ** 15 - 1, True),
    Robstride_Param_Enum.POSITION_KP: Robstride_Param_Type("Loc_Kp", 0x701E, c_float, 2, MIN_FLOAT_32, MAX_FLOAT_32, True),
    Robstride_Param_Enum.SPEED_KP: Robstride_Param_Type("Spd_Kp", 0x701F, c_float, 2, MIN_FLOAT_32, MAX_FLOAT_32, True),
    Robstride_Param_Enum.SPEED_KI: Robstride_Param_Type("Spd_Ki", 0x7020, c_float, 2, MIN_FLOAT_32,MAX_FLOAT_32, True),
}