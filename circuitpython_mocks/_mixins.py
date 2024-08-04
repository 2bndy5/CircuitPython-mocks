from typing import Self
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from circuitpython_mocks.busio.operations import Read, Write, Transfer
    from circuitpython_mocks.digitalio.operations import SetState, GetState


class ContextManaged:
    """An object that automatically deinitializes hardware with a context manager."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def deinit(self):
        """Free any hardware used by the object."""
        return


class Lockable(ContextManaged):
    """An object that must be locked to prevent collisions on a microcontroller resource."""

    _locked = False

    def try_lock(self):
        """Attempt to grab the lock. Return True on success, False if the lock is already taken."""
        if self._locked:
            return False
        self._locked = True
        return True

    def unlock(self):
        """Release the lock so others may use the resource."""
        if self._locked:
            self._locked = False


class Expecting:
    """A base class for the mock classes used to assert expected behaviors."""

    def __init__(self, **kwargs) -> None:
        #: A double ended queue used to assert expected behavior
        self.expectations: deque[Read | Write | Transfer | SetState | GetState] = (
            deque()
        )
        super().__init__(**kwargs)

    def done(self):
        """A function that asserts all `expectations` have been used.
        This is automatically called from the destructor."""
        assert not self.expectations, (
            "Some expectations were unused:\n    "
            + "\n    ".join([repr(x) for x in self.expectations])
        )

    def __del__(self):
        self.done()
