from enum import Enum, auto
from typing import Union, Optional
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
    """A class that mocks :external:py:class:digitalio.DigitalInOut`"""

    def __init__(self, pin: Pin, **kwargs):
        super().__init__(**kwargs)
        self._pin = pin
        self.switch_to_input()

    def switch_to_output(
        self,
        value: Union[bool, int] = False,
        drive_mode: DriveMode = DriveMode.PUSH_PULL,
    ):
        """Switch the Digital Pin Mode to Output"""
        self.direction = Direction.OUTPUT
        self.value = value
        self.drive_mode = drive_mode

    def switch_to_input(self, pull: Optional[Pull] = None):
        """Switch the Digital Pin Mode to Input"""
        self.direction = Direction.INPUT
        self.pull = pull

    def deinit(self):
        """Deinitialize the Digital Pin"""
        del self._pin

    @property
    def direction(self) -> Direction:
        """Get or Set the Digital Pin Direction"""
        return self.__direction

    @direction.setter
    def direction(self, value: Direction):
        self.__direction = value
        if value == Direction.OUTPUT:
            # self.value = False
            self.drive_mode = DriveMode.PUSH_PULL
        elif value == Direction.INPUT:
            self.pull = None
        else:
            raise AttributeError("Not a Direction")

    @property
    def value(self) -> Union[bool, int]:
        """The Digital Pin Value.
        This property will check against `SetState` and `GetState`
        :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`."""
        assert self.expectations, "No expectations found for DigitalInOut.value.getter"
        op = self.expectations.popleft()
        assert isinstance(
            op, GetState
        ), f"Expected a GetState operation, found {repr(op)}"
        return op.state

    @value.setter
    def value(self, val: Union[bool, int]):
        if self.direction != Direction.OUTPUT:
            raise AttributeError("Not an output")
        assert self.expectations, "No expectations found for DigitalInOut.value.setter"
        op = self.expectations.popleft()
        assert isinstance(
            op, SetState
        ), f"Expected a GetState operation, found {repr(op)}"
        op.assert_state(val)

    @property
    def pull(self) -> Optional[Pull]:
        """The pin pull direction"""
        if self.direction == Direction.INPUT:
            return self.__pull
        raise AttributeError("Not an input")

    @pull.setter
    def pull(self, pul: Optional[Pull]):
        if self.direction != Direction.INPUT:
            raise AttributeError("Not an input")
        self.__pull = pul

    @property
    def drive_mode(self) -> DriveMode:
        """The Digital Pin Drive Mode"""
        if self.direction != Direction.OUTPUT:
            raise AttributeError("Not an output")
        return self.__drive_mode

    @drive_mode.setter
    def drive_mode(self, mod: DriveMode):
        self.__drive_mode = mod
