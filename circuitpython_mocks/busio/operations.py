from typing import List, Optional
import sys
import circuitpython_typing as cir_py_types


class _Write:
    """A class to identify a write operation over a data bus."""

    def __init__(self, expected: bytearray, **kwargs) -> None:
        self.expected = expected
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        stringify = " ".join(["%02X" % x for x in self.expected])
        return f"<Write expected='{stringify}'>"

    def assert_expected(
        self,
        buffer: cir_py_types.WriteableBuffer,
        start: int = 0,
        end: int = sys.maxsize,
    ):
        val_len = len(self.expected)
        end = min(end, len(buffer))
        assert (
            self.expected == buffer[start:val_len]
        ), "Write.response does not match given buffer (or slice)"


class _Read:
    """A class to identify a read operation over a data bus."""

    def __init__(self, response: bytearray, **kwargs) -> None:
        self.response = response
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        stringify = " ".join(["%02X" % x for x in self.response])
        return f"<Read response='{stringify}'>"

    def assert_response(
        self,
        buffer: cir_py_types.WriteableBuffer,
        start: int = 0,
        end: int = sys.maxsize,
    ):
        ret_len = len(self.response)
        end = min(end, len(buffer))
        assert (
            end - start == ret_len
        ), "Read.response length does not match length of given buffer (or slice)"
        buffer[start:end] = self.response


class _Transfer(_Read, _Write):
    """A class to identify a read/write (transfer) operation over a data bus."""

    def __init__(self, expected: bytearray, response: bytearray, **kwargs) -> None:
        super().__init__(response=response, expected=expected, **kwargs)

    def __repr__(self) -> str:
        expected = " ".join(["%02X" % x for x in self.expected])
        response = " ".join(["%02X" % x for x in self.response])
        return f"<Transfer expected='{expected}' response='{response}'>"

    def assert_transaction(
        self,
        out_buffer: cir_py_types.ReadableBuffer,
        in_buffer: cir_py_types.WriteableBuffer,
        out_start: int = 0,
        out_end: int = sys.maxsize,
        in_start: int = 0,
        in_end: int = sys.maxsize,
    ):
        out_end = min(out_end, len(out_buffer))
        in_end = min(in_end, len(in_buffer))

        out_len = out_end - out_start
        in_len = in_end - in_start
        # prevent out-of-bounds errors
        assert len(out_buffer) - out_start >= out_len, "given out_buffer is too small"
        assert len(in_buffer) - in_start >= in_len, "given in_buffer is too small"

        assert (
            self.expected == out_buffer[out_start:out_end]
        ), "Transfer.expected does not match given out_buffer (or slice)"
        assert (
            len(self.response) == in_end - in_start
        ), "Transfer.response length does not match the length of given in_buffer (or slice)"
        in_buffer[in_start:in_end] = self.response


class _I2CAddress:
    def __init__(self, address: int, **kwargs) -> None:
        self.address = address
        super().__init__(**kwargs)

    def assert_address(self, address: int):
        assert address == self.address, "I2C address does not match given address"


class I2CWrite(_Write, _I2CAddress):
    """A class to identify a write operation over a
    :py:class:`~circuitpython_mocks.busio.I2C` bus."""

    def __init__(self, address: int, expected: bytearray) -> None:
        super().__init__(expected=expected, address=address)

    def __repr__(self) -> str:
        stringify = " ".join(["%02X" % x for x in self.expected])
        addr_hex = "%02X" % self.address
        return f"<Write address='{addr_hex}' expected='{stringify}'>"


class I2CRead(_Read, _I2CAddress):
    """A class to identify a read operation over a
    :py:class:`~circuitpython_mocks.busio.I2C` bus."""

    def __init__(self, address: int, response: bytearray) -> None:
        super().__init__(response=response, address=address)

    def __repr__(self) -> str:
        stringify = " ".join(["%02X" % x for x in self.response])
        addr_hex = "%02X" % self.address
        return f"<Read address={addr_hex} response='{stringify}'>"


class I2CTransfer(_Transfer, _I2CAddress):
    """A class to identify a write operation over a
    :py:class:`~circuitpython_mocks.busio.I2C` bus."""

    def __init__(self, address: int, expected: bytearray, response: bytearray) -> None:
        super().__init__(expected=expected, response=response, address=address)

    def __repr__(self) -> str:
        expected = " ".join(["%02X" % x for x in self.expected])
        response = " ".join(["%02X" % x for x in self.response])
        addr_hex = "%02X" % self.address
        return (
            f"<Transfer address={addr_hex} expected='{expected}' response='{response}'>"
        )


class I2CScan:
    """A class to identify a scan operation over a
    :py:class:`~circuitpython_mocks.busio.I2C` bus.

    The given ``expected`` value will be the result of `I2C.scan()`.
    """

    def __init__(self, expected: List[int]) -> None:
        for val in expected:
            assert val <= 0x7F, f"scan result {val} is not a valid I2C address"
        self.expected = expected

    def __repr__(self) -> str:
        stringify = ", ".join(["%02X" % x for x in self.expected])
        return f"<I2CScan expected='[{stringify}]'>"


class SPIRead(_Read):
    """A class to identify a read operation over a
    :py:class:`~circuitpython_mocks.busio.SPI` bus."""

    pass


class SPIWrite(_Write):
    """A class to identify a write operation over a
    :py:class:`~circuitpython_mocks.busio.SPI` bus."""

    pass


class SPITransfer(_Transfer):
    """A class to identify a read/write (transfer) operation over a
    :py:class:`~circuitpython_mocks.busio.SPI` bus."""

    def assert_transaction(
        self,
        out_buffer: cir_py_types.WriteableBuffer,
        in_buffer: cir_py_types.ReadableBuffer,
        out_start: int = 0,
        out_end: int = sys.maxsize,
        in_start: int = 0,
        in_end: int = sys.maxsize,
    ):
        # ensure buffer lengths match
        assert (
            out_end - out_start == in_end - in_start
        ), "given buffer lengths do not match"
        super().assert_transaction(
            out_buffer, in_buffer, out_start, out_end, in_start, in_end
        )


class UARTRead(_Read):
    """A class to identify a read operation over a
    :py:class:`~circuitpython_mocks.busio.UART` bus.

    .. tip::
        To emulate a timeout condition, pass a `None` value to the ``response``
        parameter.
    """

    def __init__(self, response: Optional[bytearray], **kwargs) -> None:
        super().__init__(response, **kwargs)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        if not self.response:
            return "<Read response='None'>"
        return super().__repr__()

    def assert_response(
        self,
        buffer: cir_py_types.ReadableBuffer,
        start: int = 0,
        end: int = sys.maxsize,
    ):
        if not self.response:
            buffer = self.response
            return
        return super().assert_response(buffer, start, end)


class UARTWrite(_Write):
    """A class to identify a write operation over a
    :py:class:`~circuitpython_mocks.busio.UART` bus."""

    pass


class UARTFlush:
    """A class to identify a flush operation over a
    :py:class:`~circuitpython_mocks.busio.UART` bus.

    This operation corresponds to the function
    :py:meth:`~circuitpython_mocks.busio.UART.reset_input_buffer()`.
    """

    pass
