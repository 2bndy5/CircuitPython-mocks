from circuitpython_mocks import monkey_patch_sys_paths  # noqa: F401 (1)
from circuitpython_mocks.busio.operations import (
    UARTRead,
    UARTWrite,
)


def test_uart():
    from busio import UART
    import board

    # do setup
    with UART(board.TX, board.RX) as serial:
        # set expectations for SPI bus
        serial.expectations.extend(
            [
                UARTRead(bytearray(1)),
                UARTRead(bytearray(1)),
                UARTRead(bytearray(1)),
                UARTWrite(bytearray(1)),
            ]
        )

        # do test
        buf = bytearray(1)
        _result = serial.read(1)
        serial.readinto(buf)
        _result = serial.readline()
        assert serial.write(buf) == 1


def test_default():
    # here we cannot import from the monkey-patched sys path because
    # the mock modules use absolute imports.
    from circuitpython_mocks import board, busio
    from collections import deque

    uart = board.UART()
    assert hasattr(uart, "expectations")
    assert isinstance(uart.expectations, deque)
    uart_dupe = busio.UART(board.TX, board.RX)
    assert uart == uart_dupe
    uart.expectations.append(UARTRead(bytearray(1)))
    assert uart_dupe.expectations == uart.expectations
    _ = uart_dupe.expectations.popleft()
    assert not uart.expectations
