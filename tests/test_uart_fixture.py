from circuitpython_mocks.busio.operations import UARTRead, UARTWrite

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
            ]
        )

        # do test
        buf = bytearray(1)
        _result = serial.read(1)
        serial.readinto(buf)
        _result = serial.readline()
        assert serial.write(buf) == 1

        # assert all expectation were used
        serial.done()
