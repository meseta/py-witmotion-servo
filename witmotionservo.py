""" Driver for the Witmotion 16-channel servo board """

import time
from typing import List, Union # remove at python 3.9
import hid

WITMOTION_VID = 0x1920
WITMOTION_PID = 0x0100
WITMOTION_CHANNELS = 16

class WitmotionServo():
    """ Driver object containing controls for Witmotion 16-channel servo board """

    @classmethod
    def list_devices(cls) -> List[str]:
        """ Lists all Witmotion servo boards plugged in
        :returns: a list of serial numbers
        """

        devices = hid.enumerate(WITMOTION_VID, WITMOTION_PID)
        return [device["serial_number"] for device in devices]

    def __init__(self, serial: Union[None, str]=None) -> None:
        """ Creates the hid device object
        :param serial: Optional serial number of device to connect
        """
        self.device = hid.device()
        self.serial = serial

    def open(self) -> None:
        """ Connects to the device
        device.open will raise IOError if it can't connect
        """
        self.device.open(WITMOTION_VID, WITMOTION_PID, self.serial)
        self.device.set_nonblocking(1)

    def close(self) -> None:
        """ Closes the device """
        self.device.close()

    def heartbeat(self, timeout: float=0.1) -> List[int]:
        """ Sends the heartbeat
        :param timeout: time to wait for response before returning
        :returns: the status value array
        """
        self.device.write([1, 0x05, 0x03, 0xff, 0x00, 0x12] + [0]*58)

        time_limit = time.time_ns() + timeout*1000000000
        while time.time_ns() < time_limit:
            retval = self.device.read(64)
            if retval:
                return retval
            time.sleep(0.001)

        raise TimeoutError("Read value timed out")

    def set_position(self, channel: int, value: int) -> None:
        """ Sends servo position request
        :param channel: the channel of the servo to send
        :param value: the value (500-2500) to send
        """
        if channel < 0 or channel >= WITMOTION_CHANNELS:
            raise ValueError(f"Channel out of range (0, {WITMOTION_CHANNELS-1})")

        if value < 500 or value > 2500:
            raise ValueError("Value out of range: (500, 2500)")

        datal = value & 0xff
        datah = value >> 8
        self.device.write([1, 0x05, 0x03, 0xff, 0x02, channel, datal, datah] + [0]*56)

    def set_speed(self, channel: int, value: int) -> None:
        """ Sends servo position request
        The actual speed value is 9*value degrees per second.
        e.g. speed value 15 is 135 degres per second

        :param channel: the channel of the servo to send
        :param value: the speed value (1-20)
        """
        if channel < 0 or channel >= WITMOTION_CHANNELS:
            raise ValueError(f"Channel out of range (0, {WITMOTION_CHANNELS-1})")

        if value < 1 or value > 20:
            raise ValueError("Value out of range: (1, 20)")

        self.device.write([1, 0x05, 0x03, 0xff, 0x02, channel, value, 0x00] + [0]*56)

    def execute_action_group(self, action_group: int) -> None:
        """ Executes an action group
        :param action_group: the action_group to execute (1-16)
        """
        if action_group < 1 or action_group > 16:
            raise ValueError("Action Group out of range (1, 16)")

        self.device.write([1, 0x05, 0x03, 0xff, 0x09, 0x00, action_group, 0x00] + [0]*56)

    def emergency_stop(self) -> None:
        """ Sends the emergency stop command """

        self.device.write([1, 0x05, 0x03, 0xff, 0x0b, 0x00, 0x01, 0x00] + [0]*56)

    def emergency_recovery(self) -> None:
        """ Sends the recover from emergency command """

        self.device.write([1, 0x05, 0x03, 0xff, 0x0b, 0x00, 0x00, 0x00] + [0]*56)
