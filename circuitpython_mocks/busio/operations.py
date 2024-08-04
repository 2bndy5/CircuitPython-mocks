import sys
import circuitpython_typing as cir_py_types


class Write:
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


class Read:
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


class Transfer(Read, Write):
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


class I2CWrite(Write, _I2CAddress):
    """A class to identify a write operation over a I2C bus."""

    def __init__(self, address: int, expected: bytearray) -> None:
        super().__init__(expected=expected, address=address)

    def __repr__(self) -> str:
        stringify = " ".join(["%02X" % x for x in self.expected])
        addr_hex = "%02X" % self.address
        return f"<Write address='{addr_hex}' expected='{stringify}'>"


class I2CRead(Read, _I2CAddress):
    """A class to identify a read operation over a I2C bus."""

    def __init__(self, address: int, response: bytearray) -> None:
        super().__init__(response=response, address=address)

    def __repr__(self) -> str:
        stringify = " ".join(["%02X" % x for x in self.response])
        addr_hex = "%02X" % self.address
        return f"<Read address={addr_hex} response='{stringify}'>"


class I2CTransfer(Transfer, _I2CAddress):
    """A class to identify a write operation over a I2C bus."""

    def __init__(self, address: int, expected: bytearray, response: bytearray) -> None:
        super().__init__(expected=expected, response=response, address=address)

    def __repr__(self) -> str:
        expected = " ".join(["%02X" % x for x in self.expected])
        response = " ".join(["%02X" % x for x in self.response])
        addr_hex = "%02X" % self.address
        return (
            f"<Transfer address={addr_hex} expected='{expected}' response='{response}'>"
        )


class SPIRead(Read):
    """A class to identify a read operation over a SPI bus."""

    pass


class SPIWrite(Write):
    """A class to identify a write operation over a SPI bus."""

    pass


class SPITransfer(Transfer):
    """A class to identify a read/write (transfer) operation over a SPI bus."""

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


class UARTRead(Read):
    """A class to identify a read operation over a UART bus."""

    pass


class UARTWrite(Write):
    """A class to identify a write operation over a UART bus."""

    pass
