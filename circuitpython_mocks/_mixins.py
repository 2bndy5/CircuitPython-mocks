from collections import deque
from typing import Self, Deque, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from circuitpython_mocks.busio.operations import (
        I2CRead,
        I2CWrite,
        I2CTransfer,
        SPIRead,
        SPIWrite,
        SPITransfer,
        UARTRead,
        UARTWrite,
    )
    from circuitpython_mocks.digitalio.operations import SetState, GetState


class ContextManaged:
    """An object that automatically deinitializes hardware with a context manager."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.deinit()

    def deinit(self) -> None:
        """Free any hardware used by the object."""
        return


class Lockable(ContextManaged):
    """An object that must be locked to prevent collisions on a microcontroller
    resource."""

    _locked = False

    def try_lock(self) -> bool:
        """Attempt to grab the lock. Return `True` on success, `False` if the lock is
        already taken."""
        if self._locked:
            return False
        self._locked = True
        return True

    def unlock(self) -> None:
        """Release the lock so others may use the resource."""
        if self._locked:
            self._locked = False


class Expecting:
    """A base class for the mock classes used to assert expected behaviors.

    .. seealso::
        :title: Mocks that derive from this mixin class

        - `busio.I2C`
        - `board.I2C()`
        - `board.STEMMA_I2C()`
        - `busio.SPI`
        - `board.SPI()`
        - `board.SPI1()`
        - `busio.UART`
        - `board.UART()`
        - `digitalio.DigitalInOut`
    """

    def __init__(self, **kwargs) -> None:
        self.expectations: Deque[
            Union[
                I2CRead,
                I2CWrite,
                I2CTransfer,
                SPIRead,
                SPIWrite,
                SPITransfer,
                UARTRead,
                UARTWrite,
                SetState,
                GetState,
            ]
        ] = deque()
        """A double-ended queue (:py:class:`~collections.deque`) used to assert
        expected behavior.

        .. example::

            Examples that use `expectations` can be found in the

            - :doc:`busio` documentation
            - :doc:`digitalio`  documentation
            - :py:func:`~circuitpython_mocks.fixtures.mock_blinka_imports`
              (pytest fixture) documentation

            .. _this package's tests files:
                https://github.com/2bndy5/CircuitPython-mocks/tree/main/tests

            All examples' source is located in `this package's tests files`_.
        """

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
