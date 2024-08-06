"""A module that hosts mock pins and default :py:class:`~busio.SPI`,
:py:class:`~busio.I2C`, and :py:class:`~busio.UART` data buses."""

#: A dummy identifier to allow detection when using this mock library.
board_id = "CIRCUITPYTHON_MOCK"


class Pin:
    """A dummy type for GPIO pins."""

    pass


A0 = Pin()
A1 = Pin()
A2 = Pin()
A3 = Pin()
A4 = Pin()
A5 = Pin()
A6 = Pin()
A7 = Pin()
A8 = Pin()
A9 = Pin()
A10 = Pin()
A11 = Pin()
A12 = Pin()
A13 = Pin()
A14 = Pin()
A15 = Pin()
A16 = Pin()
A17 = Pin()
A18 = Pin()
A19 = Pin()
A20 = Pin()
A21 = Pin()
A22 = Pin()
A23 = Pin()
A24 = Pin()
A25 = Pin()

D0 = Pin()
D1 = Pin()
D2 = Pin()
D3 = Pin()
D4 = Pin()
D5 = Pin()
D6 = Pin()
D7 = Pin()
D8 = Pin()
D9 = Pin()
D10 = Pin()
D11 = Pin()
D12 = Pin()
D13 = Pin()
D14 = Pin()
D15 = Pin()
D16 = Pin()
D17 = Pin()
D18 = Pin()
D19 = Pin()
D20 = Pin()
D21 = Pin()
D22 = Pin()
D23 = Pin()
D24 = Pin()
D25 = Pin()
D26 = Pin()
D27 = Pin()
D28 = Pin()
D29 = Pin()
D30 = Pin()
D31 = Pin()
D32 = Pin()
D33 = Pin()
D34 = Pin()
D35 = Pin()
D36 = Pin()
D37 = Pin()
D38 = Pin()
D39 = Pin()
D40 = Pin()
D41 = Pin()
D42 = Pin()
D43 = Pin()
D44 = Pin()
D45 = Pin()
D46 = Pin()
D47 = Pin()
D48 = Pin()
D49 = Pin()
D50 = Pin()
D51 = Pin()
D52 = Pin()
D53 = Pin()
D54 = Pin()
D55 = Pin()
D56 = Pin()
D57 = Pin()
D58 = Pin()
D59 = Pin()
D60 = Pin()
D61 = Pin()
D62 = Pin()
D63 = Pin()
D64 = Pin()
D65 = Pin()
D66 = Pin()
D67 = Pin()
D68 = Pin()
D69 = Pin()
D70 = Pin()
D71 = Pin()
D72 = Pin()
D73 = Pin()
D74 = Pin()
D75 = Pin()
D76 = Pin()
D77 = Pin()
D78 = Pin()
D79 = Pin()
D80 = Pin()
D81 = Pin()
D82 = Pin()
D83 = Pin()
D84 = Pin()
D85 = Pin()
D86 = Pin()
D87 = Pin()
D88 = Pin()
D89 = Pin()
D90 = Pin()
D91 = Pin()
D92 = Pin()
D93 = Pin()
D94 = Pin()
D95 = Pin()
D96 = Pin()
D97 = Pin()
D98 = Pin()
D99 = Pin()

SDA = Pin()
SCL = Pin()
SDA1 = Pin()
SCL1 = Pin()

CE1 = Pin()
CE0 = Pin()
MISO = Pin()
MOSI = Pin()
SCLK = Pin()
SCK = Pin()

TXD = Pin()
RXD = Pin()

TX = Pin()
RX = Pin()

MISO_1 = Pin()
MOSI_1 = Pin()
SCLK_1 = Pin()
SCK_1 = Pin()
CS = Pin()

WS = Pin()
SD = Pin()

LED = Pin()
NEOPIXEL = Pin()
DOTSTAR = Pin()


def SPI():
    """Creates a default instance (singleton) of :py:class:`~busio.SPI`"""
    from circuitpython_mocks.busio import SPI as ImplSPI

    return ImplSPI(SCK, MOSI, MISO)


def I2C():
    """Creates a default instance (singleton) of :py:class:`~busio.I2C`"""
    from circuitpython_mocks.busio import I2C as ImplI2C

    return ImplI2C(SCL, SDA)


def STEMMA_I2C():
    """Creates a default instance (singleton) of :py:class:`~busio.I2C`"""
    from circuitpython_mocks.busio import I2C as ImplI2C

    return ImplI2C(SCL1, SDA1)


def UART():
    """Creates a default instance (singleton) of :py:class:`~busio.UART`"""
    from circuitpython_mocks.busio import UART as ImplUART

    return ImplUART(TX, RX)
