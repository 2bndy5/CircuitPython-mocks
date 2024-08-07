import pytest
from collections import deque
from circuitpython_mocks import board, busio
from circuitpython_mocks.busio.operations import SPITransfer


@pytest.mark.parametrize(
    argnames=["board_spi", "busio_spi"],
    argvalues=[
        (board.SPI(), busio.SPI(board.SCK, board.MOSI, board.MISO)),
        (board.SPI1(), busio.SPI(board.SCK_1, board.MOSI_1, board.MISO_1)),
    ],
    ids=["primary_bus", "secondary_bus"],
)
def test_singleton(board_spi: busio.SPI, busio_spi: busio.SPI):
    assert hasattr(board_spi, "expectations")
    assert isinstance(busio_spi.expectations, deque)
    assert board_spi == busio_spi

    board_spi.expectations.append(SPITransfer(bytearray(1), bytearray(1)))
    assert busio_spi.expectations == board_spi.expectations
    buffer = bytearray(1)
    assert board_spi.try_lock()
    assert not busio_spi.try_lock()
    board_spi.write_readinto(buffer, buffer)
    board_spi.unlock()
    busio_spi.unlock()  # for coverage measurement only

    # assert all expectations were used
    board_spi.done()
    assert busio_spi.expectations == board_spi.expectations
