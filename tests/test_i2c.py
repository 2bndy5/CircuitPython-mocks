import pytest
from collections import deque
from circuitpython_mocks import busio, board
from circuitpython_mocks.busio.operations import I2CTransfer


@pytest.mark.parametrize(
    argnames=["board_i2c", "busio_i2c"],
    argvalues=[
        (board.I2C(), busio.I2C(board.SCL, board.SDA)),
        (board.STEMMA_I2C(), busio.I2C(board.SCL1, board.SDA1)),
    ],
    ids=["primary_bus", "secondary_bus"],
)
def test_singleton(board_i2c: busio.I2C, busio_i2c: busio.I2C):
    address = 0x42

    assert hasattr(board_i2c, "expectations")
    assert isinstance(board_i2c.expectations, deque)
    assert board_i2c == busio_i2c

    board_i2c.expectations.append(I2CTransfer(address, bytearray(1), bytearray(1)))
    assert busio_i2c.expectations == board_i2c.expectations
    buffer = bytearray(1)
    assert board_i2c.try_lock()
    assert not busio_i2c.try_lock()
    board_i2c.writeto_then_readfrom(address, buffer, buffer)
    board_i2c.unlock()
    busio_i2c.unlock()  # for coverage measurement only

    # assert all expectations were used
    board_i2c.done()
    assert board_i2c.expectations == busio_i2c.expectations
