"""A mock of the :external:py:mod:`busio` module.

.. md-tab-set::

    .. md-tab-item:: I2C

        .. literalinclude:: ../../tests/test_i2c.py
            :language: python

    .. md-tab-item:: SPI

        .. literalinclude:: ../../tests/test_spi.py
            :language: python

    .. md-tab-item:: UART

        .. literalinclude:: ../../tests/test_uart.py
            :language: python
"""

from enum import Enum, auto
import sys
from typing import List, Optional

import circuitpython_typing

from circuitpython_mocks.busio.operations import (
    UARTRead,
    UARTWrite,
    UARTFlush,
    I2CRead,
    I2CWrite,
    I2CTransfer,
    I2CScan,
    SPIRead,
    SPIWrite,
    SPITransfer,
)
from circuitpython_mocks._mixins import Expecting, Lockable
from circuitpython_mocks.board import (
    Pin,
    SDA,
    SDA1,
    SCL,
    SCL1,
    SCK,
    MOSI as PinMOSI,
    MISO as PinMISO,
    TX,
    RX,
    MISO_1,
    MOSI_1,
    SCK_1,
)


class I2C(Expecting, Lockable):
    """A mock of :external:py:class:`busio.I2C` class."""

    _primary_singleton: Optional["I2C"] = None
    _secondary_singleton: Optional["I2C"] = None

    def __new__(cls, scl: Pin, sda: Pin, **kwargs) -> "I2C":
        if scl == SCL and sda == SDA:
            if cls._primary_singleton is None:
                cls._primary_singleton = super().__new__(cls)
            return cls._primary_singleton
        if scl == SCL1 and sda == SDA1:
            if cls._secondary_singleton is None:
                cls._secondary_singleton = super().__new__(cls)
            return cls._secondary_singleton
        return super().__new__(cls)

    def __init__(
        self,
        scl: Pin,
        sda: Pin,
        *,
        frequency: int = 100000,
        timeout: int = 255,
    ):
        if hasattr(self, "expectations"):
            return
        super().__init__()

    def scan(self) -> List[int]:
        """Scan all I2C addresses between 0x08 and 0x77 inclusive and return a list of
        those that respond.

        .. mock-expects::

            This function will check against `I2CScan`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for I2C.scan()"
        op = self.expectations.popleft()
        assert isinstance(op, I2CScan), f"I2CScan operation expected, found {repr(op)}"
        return op.expected

    def readfrom_into(
        self,
        address: int,
        buffer: circuitpython_typing.WriteableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
    ) -> None:
        """A mock imitation of :external:py:meth:`busio.I2C.readfrom_into()`.

        .. mock-expects::

            This function checks against `I2CRead`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for I2C.readfrom_into()"
        op = self.expectations.popleft()
        assert isinstance(op, I2CRead), f"Read operation expected, found {repr(op)}"
        assert address == op.address, "Read.address does not match given address"
        op.assert_address(address)
        op.assert_response(buffer, start, end)

    def writeto(
        self,
        address: int,
        buffer: circuitpython_typing.ReadableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
    ) -> None:
        """A mock imitation of :external:py:meth:`busio.I2C.writeto()`.

        .. mock-expects::

            This function checks against `I2CWrite`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for I2C.writeto()"
        op = self.expectations.popleft()
        assert isinstance(op, I2CWrite), f"Read operation expected, found {repr(op)}"
        op.assert_address(address)
        op.assert_expected(buffer, start, end)

    def writeto_then_readfrom(
        self,
        address: int,
        out_buffer: circuitpython_typing.ReadableBuffer,
        in_buffer: circuitpython_typing.WriteableBuffer,
        *,
        out_start: int = 0,
        out_end: int = sys.maxsize,
        in_start: int = 0,
        in_end: int = sys.maxsize,
    ) -> None:
        """A mock imitation of :external:py:meth:`busio.I2C.writeto_then_readfrom()`.

        .. mock-expects::

            This function checks against `I2CTransfer`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for I2C.writeto_then_readfrom()"
        op = self.expectations.popleft()
        assert isinstance(
            op, I2CTransfer
        ), f"Transfer operation expected, found {repr(op)}"
        op.assert_address(address)
        op.assert_transaction(
            out_buffer, in_buffer, out_start, out_end, in_start, in_end
        )


class SPI(Expecting, Lockable):
    """A mock of :external:py:class:`busio.SPI` class."""

    _primary_singleton: Optional["SPI"] = None
    _secondary_singleton: Optional["SPI"] = None

    def __new__(cls, clock: Pin, MOSI: Pin, MISO: Pin, **kwargs) -> "SPI":
        if clock == SCK and MOSI == PinMOSI and MISO == PinMISO:
            if cls._primary_singleton is None:
                cls._primary_singleton = super().__new__(cls)
            return cls._primary_singleton
        if clock == SCK_1 and MOSI == MOSI_1 and MISO == MISO_1:
            if cls._secondary_singleton is None:
                cls._secondary_singleton = super().__new__(cls)
            return cls._secondary_singleton
        return super().__new__(cls)

    def __init__(
        self,
        clock: Pin,
        MOSI: Pin | None = None,
        MISO: Pin | None = None,
        half_duplex: bool = False,
    ):
        """A class to mock :external:py:class:`busio.SPI`."""
        super().__init__()
        self._frequency = 1000000

    def configure(
        self,
        *,
        baudrate: int = 100000,
        polarity: int = 0,
        phase: int = 0,
        bits: int = 8,
    ) -> None:
        """A dummy function to mock :external:py:meth:`busio.SPI.configure()`"""
        self._frequency = baudrate

    @property
    def frequency(self) -> int:
        """Returns the value passed to ``baudrate`` parameter of `configure()`."""
        return self._frequency

    def write(
        self,
        buffer: circuitpython_typing.ReadableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
    ) -> None:
        """A function that mocks :external:py:meth:`busio.SPI.write()`.

        .. mock-expects::

            This function checks against `SPIWrite`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for SPI.write()"
        op = self.expectations.popleft()
        assert isinstance(op, SPIWrite), f"Read operation expected, found {repr(op)}"
        op.assert_expected(buffer, start, end)

    def readinto(
        self,
        buffer: circuitpython_typing.WriteableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
        write_value: int = 0,
    ) -> None:
        """A function that mocks :external:py:meth:`busio.SPI.readinto()`.

        .. mock-expects::

            This function checks against `SPIRead`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for SPI.readinto()"
        op = self.expectations.popleft()
        assert isinstance(op, SPIRead), f"Read operation expected, found {repr(op)}"
        op.assert_response(buffer, start, end)

    def write_readinto(
        self,
        out_buffer: circuitpython_typing.ReadableBuffer,
        in_buffer: circuitpython_typing.WriteableBuffer,
        *,
        out_start: int = 0,
        out_end: int = sys.maxsize,
        in_start: int = 0,
        in_end: int = sys.maxsize,
    ) -> None:
        """A function that mocks :external:py:meth:`busio.SPI.write_readinto()`.

        .. mock-expects::

            This function checks against `SPITransfer`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for SPI.write_readinto()"
        op = self.expectations.popleft()
        assert isinstance(
            op, SPITransfer
        ), f"Transfer operation expected, found {repr(op)}"
        op.assert_transaction(
            out_buffer, in_buffer, out_start, out_end, in_start, in_end
        )


class UART(Expecting, Lockable):
    """A class that mocks :external:py:class:`busio.UART`."""

    _primary_singleton: Optional["UART"] = None

    def __new__(cls, tx: Pin, rx: Pin, **kwargs) -> "UART":
        if tx == TX and rx == RX:
            if cls._primary_singleton is None:
                cls._primary_singleton = super().__new__(cls)
            return cls._primary_singleton
        return super().__new__(cls)

    class Parity(Enum):
        ODD = auto()
        EVEN = auto()

    def __init__(
        self,
        tx: Pin | None = None,
        rx: Pin | None = None,
        *,
        rts: Pin | None = None,
        cts: Pin | None = None,
        rs485_dir: Pin | None = None,
        rs485_invert: bool = False,
        baudrate: int = 9600,
        bits: int = 8,
        parity: Parity | None = None,
        stop: int = 1,
        timeout: float = 1,
        receiver_buffer_size: int = 64,
    ) -> None:
        self._baudrate = baudrate
        self._timeout = timeout
        super().__init__()

    def read(self, nbytes: int | None = None) -> Optional[bytes]:
        """A function that mocks :external:py:meth:`busio.UART.read()`.

        .. mock-expects::

            This function checks against `UARTRead`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for UART.read()"
        op = self.expectations.popleft()
        assert isinstance(op, UARTRead), f"Read operation expected, found {repr(op)}"
        length = nbytes or 0 if not op.response else len(op.response)
        buffer = bytearray(length)
        op.assert_response(buffer, 0, length)
        return None if not buffer else bytes(buffer)

    def readinto(self, buf: circuitpython_typing.WriteableBuffer) -> Optional[int]:
        """A function that mocks :external:py:meth:`busio.UART.readinto()`.

        .. mock-expects::

            This function checks against `UARTRead`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for UART.readinto()"
        op = self.expectations.popleft()
        assert isinstance(op, UARTRead), f"Read operation expected, found {repr(op)}"
        len_buf = 0 if not op.response else len(op.response)
        op.assert_response(buf, 0, len_buf)
        return len_buf

    def readline(self) -> Optional[bytes]:
        """A function that mocks :external:py:meth:`busio.UART.readline()`.

        .. mock-expects::

            This function checks against `UARTRead`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for UART.readline()"
        op = self.expectations.popleft()
        assert isinstance(op, UARTRead), f"Read operation expected, found {repr(op)}"
        len_buf = 0 if not op.response else len(op.response)
        buf = bytearray(len_buf)
        op.assert_response(buf, 0, len_buf)
        return None if buf else bytes(buf)

    def write(self, buf: circuitpython_typing.ReadableBuffer) -> int | None:
        """A function that mocks :external:py:meth:`busio.UART.write()`.

        .. mock-expects::

            This function checks against `UARTWrite`
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`.
        """
        assert self.expectations, "no expectation found for UART.write()"
        op = self.expectations.popleft()
        assert isinstance(op, UARTWrite), f"Read operation expected, found {repr(op)}"
        len_buf = len(op.expected)
        op.assert_expected(buf, 0, len_buf)
        return len(buf) or None

    @property
    def baudrate(self) -> int:
        """The current baudrate."""
        return self._baudrate

    @baudrate.setter
    def baudrate(self, val: int):
        self._baudrate = int(val)

    @property
    def timeout(self) -> float:
        """The current timeout, in seconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, val: float):
        self._timeout = float(val)

    @property
    def in_waiting(self) -> int:
        """The number of bytes in the input buffer, available to be read.

        .. mock-expects::

            This property peeks at the number of bytes in next available operation in
            :py:attr:`~circuitpython_mocks._mixins.Expecting.expectations`. If a
            `UARTRead` operation is not immediately expected, then ``0`` is returned.
        """
        if self.expectations and isinstance(self.expectations[0], UARTRead):
            return len(self.expectations[0].response)
        return 0

    def reset_input_buffer(self) -> None:
        """Discard any unread characters in the input buffer.

        .. mock-expects::

            This function merely checks the immediately queued
            :py:class:`~circuitpython_mocks._mixins.Expecting.expectations` for
            a `UARTFlush` operation. It does not actually discard any data.
        """
        assert self.expectations
        op = self.expectations.popleft()
        assert isinstance(op, UARTFlush), f"Flush operation expected, found {repr(op)}"
