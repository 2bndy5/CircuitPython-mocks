from collections import deque
from circuitpython_mocks import board, busio
from circuitpython_mocks.busio.operations import UARTRead, UARTWrite


def test_singleton():
    board_uart = board.UART()
    assert hasattr(board_uart, "expectations")
    assert isinstance(board_uart.expectations, deque)

    busio_uart = busio.UART(board.TX, board.RX)
    assert board_uart == busio_uart

    board_uart.expectations.append(UARTRead(bytearray(1)))
    assert busio_uart.expectations == board_uart.expectations
    buffer = bytearray(1)
    board_uart.readinto(buffer)
    assert not busio_uart.expectations

    busio_uart.expectations.append(UARTWrite(bytearray(1)))
    assert busio_uart.expectations == board_uart.expectations
    busio_uart.write(bytearray(1))

    # assert all expectations were used
    board_uart.done()
    assert busio_uart.expectations == board_uart.expectations
