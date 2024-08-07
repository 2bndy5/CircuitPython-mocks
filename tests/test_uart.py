from collections import deque
from circuitpython_mocks import board, busio
from circuitpython_mocks.busio.operations import UARTRead, UARTWrite, UARTFlush


def test_singleton():
    board_uart = board.UART()
    assert hasattr(board_uart, "expectations")
    assert isinstance(board_uart.expectations, deque)
    busio_uart = busio.UART(board.TX, board.RX)
    assert board_uart == busio_uart
    board_uart.timeout = 0.5
    assert 0.5 == busio_uart.timeout
    busio_uart.baudrate = 115200
    assert 115200 == board_uart.baudrate

    board_uart.expectations.append(UARTRead(bytearray(1)))
    assert busio_uart.expectations == board_uart.expectations
    buffer = bytearray(1)
    assert 1 == board_uart.in_waiting
    board_uart.readinto(buffer)
    assert not busio_uart.expectations

    busio_uart.expectations.append(UARTWrite(bytearray(1)))
    assert busio_uart.expectations == board_uart.expectations
    assert not busio_uart.in_waiting
    busio_uart.write(bytearray(1))

    busio_uart.expectations.append(UARTFlush())
    assert busio_uart.expectations == board_uart.expectations
    busio_uart.reset_input_buffer()

    # assert all expectations were used
    board_uart.done()
    assert busio_uart.expectations == board_uart.expectations
