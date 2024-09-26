import ctypes

class InnoMakerUsb2CanLib:
    def __init__(self):
        self.lib = ctypes.cdll.LoadLibrary("InnoMakerUsb2CanLib.dll")  # Load the DLL

        # Define function prototypes with argument and return types
        self.lib.setup.restype = ctypes.c_bool
        self.lib.setdown.restype = ctypes.c_bool
        self.lib.scanInnoMakerDevice.restype = ctypes.c_bool
        self.lib.getInnoMakerDeviceCount.restype = ctypes.c_int
        self.lib.getInnoMakerDevice.restype = ctypes.c_void_p  # Pointer to InnoMakerDevice
        self.lib.openInnoMakerDevice.argtypes = [ctypes.c_void_p]
        self.lib.openInnoMakerDevice.restype = ctypes.c_bool
        self.lib.closeInnoMakerDevice.argtypes = [ctypes.c_void_p]
        self.lib.closeInnoMakerDevice.restype = ctypes.c_bool
        self.lib.sendInnoMakerDeviceBuf.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_byte), ctypes.c_int, ctypes.c_uint]
        self.lib.sendInnoMakerDeviceBuf.restype = ctypes.c_bool
        self.lib.recvInnoMakerDeviceBuf.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_byte), ctypes.c_int, ctypes.c_uint]
        self.lib.recvInnoMakerDeviceBuf.restype = ctypes.c_bool
        self.lib.urbResetDevice.argtypes = [ctypes.c_void_p]
        self.lib.urbResetDevice.restype = ctypes.c_bool
        self.lib.urbSetupDevice.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]  # UsbCanMode enum will be an int
        self.lib.urbSetupDevice.restype = ctypes.c_bool

        # Define the innomaker_host_frame structure
        class innomaker_host_frame(ctypes.Structure):
            _fields_ = [
                ("echo_id", ctypes.c_uint32),
                ("can_id", ctypes.c_uint32),
                ("can_dlc", ctypes.c_byte),
                ("channel", ctypes.c_byte),
                ("flags", ctypes.c_byte),
                ("reserved", ctypes.c_byte),
                ("data", ctypes.c_byte * 8),
                ("timestamp_us", ctypes.c_uint32),
            ]

        self.innomaker_host_frame = innomaker_host_frame

        # Define the Innomaker_device_bittming structure
        class Innomaker_device_bittming(ctypes.Structure):
            _fields_ = [
                ("prop_seg", ctypes.c_uint32),
                ("phase_seg1", ctypes.c_uint32),
                ("phase_seg2", ctypes.c_uint32),
                ("sjw", ctypes.c_uint32),
                ("brp", ctypes.c_uint32),
            ]

        self.Innomaker_device_bittming = Innomaker_device_bittming

        # Define UsbCanMode enum values (as ints)
        self.UsbCanMode = {
            "UsbCanModeNormal": 0,
            "UsbCanModeLoopback": 1,
            "UsbCanModeListenOnly": 2,
        }

    def setup(self):
        return self.lib.setup()

    def setdown(self):
        return self.lib.setdown()