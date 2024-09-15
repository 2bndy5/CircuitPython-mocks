from typing import Union


class _State:
    def __init__(self, state: Union[bool, int]) -> None:
        self.state = bool(state)

    def assert_state(self, value: Union[bool, int]):
        assert self.state is bool(
            value
        ), "Expected pin state does not match given pin state"


class SetState(_State):
    """A class to represent setting the state of a
    :py:class:`~circuitpython_mocks.digitalio.DigitalInOut` pin."""

    def __repr__(self) -> str:
        return f"<SetState value='{self.state}'>"


class GetState(_State):
    """A class to represent getting the state of a
    :py:class:`~circuitpython_mocks.digitalio.DigitalInOut` pin."""

    def __repr__(self) -> str:
        return f"<GetState value='{self.state}'>"
