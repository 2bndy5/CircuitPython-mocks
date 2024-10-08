from circuitpython_mocks.busio.operations import (
    SPIRead,
    SPIWrite,
    SPITransfer,
)
from circuitpython_mocks.digitalio.operations import SetState

pytest_plugins = ["circuitpython_mocks.fixtures"]


def test_spi(mock_blinka_imports):
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
            spi.readinto(buf, end=1)
        with spi_dev as spi:
            spi.write(buf, end=1)
        with spi_dev as spi:
            spi.write_readinto(buf, buf, out_end=1, in_end=1)

        # assert all expectation were used
        spi_bus.done()
