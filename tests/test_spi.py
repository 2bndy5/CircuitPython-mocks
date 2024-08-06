from circuitpython_mocks import monkey_patch_sys_paths  # noqa: F401 (1)
from circuitpython_mocks.busio.operations import (
    SPIRead,
    SPIWrite,
    SPITransfer,
)
from circuitpython_mocks.digitalio.operations import SetState


def test_spi():
    from busio import SPI
    from digitalio import DigitalInOut
    import board
    from adafruit_bus_device.spi_device import SPIDevice

    # do setup
    with SPI(board.SCK, board.MOSI, board.MISO) as spi_bus:
        assert spi_bus.frequency == 1000000
        cs = DigitalInOut(board.CE0)

        # set expectations for the CS pin. We'll be doing 3 transactions (toggling pin each time)
        cs.expectations.append(SetState(True))
        cs.expectations.extend([SetState(False), SetState(True)] * 3)
        # set expectations for SPI bus
        spi_bus.expectations.extend(
            [
                SPIRead(bytearray(1)),
                SPIWrite(bytearray(1)),
                SPITransfer(bytearray(1), bytearray(1)),
            ]
        )
        spi_dev = SPIDevice(spi_bus, chip_select=cs)

        # do test
        buf = bytearray(1)
        with spi_dev as spi:
            assert not spi_bus.try_lock()
            spi.readinto(buf, end=1)
        with spi_dev as spi:
            spi.write(buf, end=1)
        with spi_dev as spi:
            spi.write_readinto(buf, buf, out_end=1, in_end=1)


def test_default():
    # here we cannot import from the monkey-patched sys path because
    # the mock modules use absolute imports.
    from circuitpython_mocks import board, busio
    from collections import deque

    spi = board.SPI()
    assert hasattr(spi, "expectations")
    assert isinstance(spi.expectations, deque)
    spi_dupe = busio.SPI(board.SCK, board.MOSI, board.MISO)
    assert spi == spi_dupe
    spi.expectations.append(SPIRead(bytearray(1)))
    assert spi_dupe.expectations == spi.expectations
    op = spi_dupe.expectations.popleft()
    assert not spi.expectations

    spi1 = busio.SPI(board.SCK_1, board.MOSI_1, board.MISO_1)
    assert hasattr(spi1, "expectations")
    assert isinstance(spi1.expectations, deque)
    spi1_dupe = busio.SPI(board.SCK_1, board.MOSI_1, board.MISO_1)
    assert spi1 == spi1_dupe
    spi1.expectations.append(op)
    assert spi1_dupe.expectations == spi1.expectations
    _ = spi1_dupe.expectations.popleft()
    assert not spi1.expectations
