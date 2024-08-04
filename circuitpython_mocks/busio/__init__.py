from enum import Enum, auto
import sys
from typing import List

import circuitpython_typing

from circuitpython_mocks.busio.operations import (
    Read,
    Write,
    Transfer,
    I2CRead,
    I2CWrite,
    I2CTransfer,
)
from circuitpython_mocks._mixins import Expecting, Lockable
from circuitpython_mocks.board import Pin


class I2C(Expecting, Lockable):
    def __init__(
        self,
        scl: Pin,
        sda: Pin,
        *,
        frequency: int = 100000,
        timeout: int = 255,
    ):
        super().__init__()

    def scan(self) -> List[int]:
        return []

    def readfrom_into(
        self,
        address: int,
        buffer: circuitpython_typing.WriteableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
    ) -> None:
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
    def __init__(
        self,
        clock: Pin,
        MOSI: Pin | None = None,
        MISO: Pin | None = None,
        half_duplex: bool = False,
    ):
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
        self._frequency = baudrate

    @property
    def frequency(self) -> int:
        return self._frequency

    def write(
        self,
        buffer: circuitpython_typing.ReadableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
    ) -> None:
        assert self.expectations, "no expectation found for SPI.write()"
        op = self.expectations.popleft()
        assert isinstance(op, Write), f"Read operation expected, found {repr(op)}"
        op.assert_expected(buffer, start, end)

    def readinto(
        self,
        buffer: circuitpython_typing.WriteableBuffer,
        *,
        start: int = 0,
        end: int = sys.maxsize,
        write_value: int = 0,
    ) -> None:
        assert self.expectations, "no expectation found for SPI.readinto()"
        op = self.expectations.popleft()
        assert isinstance(op, Read), f"Read operation expected, found {repr(op)}"
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
        assert self.expectations, "no expectation found for I2C.writeto_then_readfrom()"
        op = self.expectations.popleft()
        assert isinstance(
            op, Transfer
        ), f"Transfer operation expected, found {repr(op)}"
        op.assert_transaction(
            out_buffer, in_buffer, out_start, out_end, in_start, in_end
        )


class UART(Expecting, Lockable):
    class Parity(Enum):
        """Parity Enumeration"""

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
        super().__init__()

    def read(self, nbytes: int | None = None) -> bytes | None:
        assert self.expectations, "no expectation found for UART.read()"
        op = self.expectations.popleft()
        assert isinstance(op, Read), f"Read operation expected, found {repr(op)}"
        length = nbytes or len(op.response)
        buffer = bytearray(length)
        op.assert_response(buffer, 0, length)
        return bytes(buffer)

    def readinto(self, buf: circuitpython_typing.WriteableBuffer) -> int | None:
        assert self.expectations, "no expectation found for UART.readinto()"
        op = self.expectations.popleft()
        assert isinstance(op, Read), f"Read operation expected, found {repr(op)}"
        len_buf = len(op.response)
        op.assert_response(buf, 0, len_buf)
        return len_buf

    def readline(self) -> bytes:
        assert self.expectations, "no expectation found for UART.readline()"
        op = self.expectations.popleft()
        assert isinstance(op, Read), f"Read operation expected, found {repr(op)}"
        len_buf = len(op.response)
        buf = bytearray(len_buf)
        op.assert_response(buf, 0, len_buf)
        return bytes(buf)

    def write(self, buf: circuitpython_typing.ReadableBuffer) -> int | None:
        assert self.expectations, "no expectation found for UART.write()"
        op = self.expectations.popleft()
        assert isinstance(op, Write), f"Read operation expected, found {repr(op)}"
        len_buf = len(op.expected)
        op.assert_expected(buf, 0, len_buf)
        return len(buf) or None
