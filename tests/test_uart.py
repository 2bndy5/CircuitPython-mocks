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
