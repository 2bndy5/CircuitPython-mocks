from circuitpython_mocks.busio.operations import UARTRead, UARTWrite, UARTFlush

pytest_plugins = ["circuitpython_mocks.fixtures"]


def test_uart(mock_blinka_imports):
    from busio import UART
    import board

    # do setup
    with UART(board.TX, board.RX) as serial:
        # set expectations for UART bus
        serial.expectations.extend(
            [
                UARTRead(bytearray(1)),
                UARTRead(bytearray(1)),
                UARTRead(bytearray(1)),
                UARTWrite(bytearray(1)),
                UARTFlush(),
                UARTRead(None),  # timeout condition
            ]
        )

        # do test
        buf = bytearray(1)
        assert 1 == serial.in_waiting
        _result = serial.read(1)
        serial.readinto(buf)
        _result = serial.readline()
        assert serial.write(buf) == 1
        serial.reset_input_buffer()
        assert serial.read() is None

        # assert all expectation were used
        serial.done()
