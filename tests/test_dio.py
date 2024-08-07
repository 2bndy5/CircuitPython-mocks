import pytest
from circuitpython_mocks import board
from circuitpython_mocks.digitalio import DigitalInOut, Direction, DriveMode, Pull
from circuitpython_mocks.digitalio.operations import SetState, GetState


def test_dio():
    with DigitalInOut(board.D42) as dio:
        assert dio.direction == Direction.INPUT
        assert dio.pull is None

        # set expectations for the pin state changes
        dio.expectations.append(GetState(True))
        assert dio.value
        dio.expectations.extend([SetState(False), SetState(True)])
        dio.switch_to_output()
        dio.value = True

        # assert all expectation were used
        dio.done()


def test_dio_errors():
    with DigitalInOut(board.D42) as dio:
        with pytest.raises(AttributeError):
            dio.value = True
        with pytest.raises(AttributeError):
            dio.direction = 99
        with pytest.raises(AttributeError):
            dio.drive_mode

        # set expectations for the pin state changes
        dio.expectations.extend([SetState(False)])
        dio.switch_to_output()
        with pytest.raises(AttributeError):
            dio.pull
        with pytest.raises(AttributeError):
            dio.pull = Pull.UP
        assert dio.drive_mode == DriveMode.PUSH_PULL

        # assert all expectation were used
        dio.done()
