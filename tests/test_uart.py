from circuitpython_mocks import monkey_patch_sys_paths  # noqa: F401
from circuitpython_mocks.busio.operations import (
    Read,
    Write,
)


def test_uart():
    from busio import UART
    import board

    # do setup
    with UART(board.TX, board.RX) as serial:
        # set expectations for SPI bus
        serial.expectations.extend(
            [
                Read(bytearray(1)),
                Read(bytearray(1)),
                Read(bytearray(1)),
                Write(bytearray(1)),
            ]
        )

        # do test
        buf = bytearray(1)
        _result = serial.read(1)
        serial.readinto(buf)
        _result = serial.readline()
        assert serial.write(buf) == 1
