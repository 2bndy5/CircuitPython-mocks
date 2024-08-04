from enum import Enum, auto

from circuitpython_mocks._mixins import ContextManaged, Expecting
from circuitpython_mocks.digitalio.operations import GetState, SetState
from circuitpython_mocks.board import Pin


class DriveMode(Enum):
    """Drive Mode Enumeration"""

    PUSH_PULL = auto()
    OPEN_DRAIN = auto()


class Direction(Enum):
    """Direction Enumeration"""

    INPUT = auto()
    OUTPUT = auto()


class Pull(Enum):
    """PullUp/PullDown Enumeration"""

    UP = auto()
    DOWN = auto()


class DigitalInOut(Expecting, ContextManaged):
    def __init__(self, pin: Pin, **kwargs):
        super().__init__(**kwargs)
        self._pin = pin
        self.switch_to_input()

    def switch_to_output(self, value=False, drive_mode=DriveMode.PUSH_PULL):
        """Switch the Digital Pin Mode to Output"""
        self.direction = Direction.OUTPUT
        self.value = value
        self.drive_mode = drive_mode

    def switch_to_input(self, pull=None):
        """Switch the Digital Pin Mode to Input"""
        self.direction = Direction.INPUT
        self.pull = pull

    def deinit(self):
        """Deinitialize the Digital Pin"""
        del self._pin

    @property
    def direction(self):
        """Get or Set the Digital Pin Direction"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        if value == Direction.OUTPUT:
            # self.value = False
            self.drive_mode = DriveMode.PUSH_PULL
        elif value == Direction.INPUT:
            self.pull = None
        else:
            raise AttributeError("Not a Direction")

    @property
    def value(self):
        """The Digital Pin Value"""
        assert self.expectations, "No expectations found for DigitalInOut.value.getter"
        op = self.expectations.popleft()
        assert isinstance(
            op, GetState
        ), f"Expected a GetState operation, found {repr(op)}"
        return op.state

    @value.setter
    def value(self, val):
        if self.direction != Direction.OUTPUT:
            raise AttributeError("Not an output")
        assert self.expectations, "No expectations found for DigitalInOut.value.setter"
        op = self.expectations.popleft()
        assert isinstance(
            op, SetState
        ), f"Expected a GetState operation, found {repr(op)}"
        op.assert_state(val)

    @property
    def pull(self):
        """The pin pull direction"""
        if self.direction == Direction.INPUT:
            return self.__pull
        raise AttributeError("Not an input")

    @pull.setter
    def pull(self, pul):
        if self.direction != Direction.INPUT:
            raise AttributeError("Not an input")
        self.__pull = pul

    @property
    def drive_mode(self):
        """The Digital Pin Drive Mode"""
        if self.direction != Direction.OUTPUT:
            raise AttributeError("Not an output")
        return self.__drive_mode

    @drive_mode.setter
    def drive_mode(self, mod):
        self.__drive_mode = mod
