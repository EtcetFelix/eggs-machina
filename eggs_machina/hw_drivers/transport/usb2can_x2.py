# """The driver for using the USB2CAN-X2 device by innomaker."""

# from eggs_machina.hw_drivers.transport.base import Transport
# import can
# import os

# class USB2CANX2(Transport):
#     def __init__(self, baud_rate: int):
#         self.baud_rate = baud_rate
#         bus = can.interface.Bus(interface='socketcan', channel='can1', bitrate=baud_rate)
        

#     def recv(self, can_id: int, is_extended_id: bool, timeout_s: int, *args, **kwargs) -> any:
#         pass

#     def send(self, can_id: int, data: bytes, is_extended_id: bool, *args, **kwargs) -> any:
#         pass

# if __name__ == "main":
#     os.system('sudo ifconfig can1 down')
#     os.system('sudo ip link set can1 type can bitrate 1000000')
#     os.system("sudo ifconfig can1 txqueuelen 100000")
#     os.system('sudo ifconfig can1 up')
#     bus = can.interface.Bus(interface='socketcan', channel='can1', bitrate=20000)
#     msg = can.Message(arbitration_id=0x123, data=[0,1,2,3,4,5,6,7])
#     bus.send(msg)


import os
import can
import time

os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 1000000')
os.system("sudo ifconfig can0 txqueuelen 100000")
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', interface = 'socketcan')
send_count = 0

while True:
    msg = can.Message(arbitration_id=0x123, data=[0,1,2,3,4,5,6,7])
    can0.send(msg)
    send_count = send_count + 1
    print("Currecnt send frame count:", send_count)
    time.sleep(0.001)