from circuitpython_mocks import monkey_patch_sys_paths  # noqa: F401 (1)
import pytest
from circuitpython_mocks.digitalio.operations import SetState, GetState


def test_dio():
    from digitalio import DigitalInOut, Direction, DriveMode, Pull
    import board

    # do setup
    with DigitalInOut(board.D0) as dio:
        assert dio.direction == Direction.INPUT
        assert dio.pull is None
        with pytest.raises(AttributeError):
            dio.value = True
        with pytest.raises(AttributeError):
            dio.direction = 99
        with pytest.raises(AttributeError):
            dio.drive_mode

        # set expectations for the pin state and do the test
        dio.expectations.append(GetState(True))
        assert dio.value
        dio.expectations.extend([SetState(False), SetState(True)])
        dio.switch_to_output()
        with pytest.raises(AttributeError):
            dio.pull
        with pytest.raises(AttributeError):
            dio.pull = Pull.UP
        assert dio.drive_mode == DriveMode.PUSH_PULL
        dio.value = True
