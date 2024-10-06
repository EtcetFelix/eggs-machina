import pytest
from eggs_machina.hw_drivers.transport.can.usb2can_x2 import USB2CANX2
from eggs_machina.hw_drivers.system.robstride.robstride import Robstride
from eggs_machina.hw_drivers.system.robstride.robstride_types import Robstride_Param_Enum



CAN_CHANNEL = "can0"
MOTOR_ID = 127

@pytest.fixture
def robstride_transport():
    with USB2CANX2(channel=CAN_CHANNEL, baud_rate=1000000) as transport:
        robstride = Robstride(host_can_id=0xFD, motor_can_id=MOTOR_ID, can_transport=transport)
        yield robstride  # Provide the robstride instance to the test

def test_get_vbus(robstride_transport): 
    bus_voltage = robstride_transport.read_single_param(Robstride_Param_Enum.VBUS_VOLTAGE)
    print(bus_voltage)
    assert bus_voltage is not None, "Failed to read bus_voltage..."

