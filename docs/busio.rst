``busio``
=================

.. automodule:: circuitpython_mocks.busio

    .. autoclass:: circuitpython_mocks.busio.I2C
        :members: readfrom_into, writeto, writeto_then_readfrom, scan
    .. autoclass:: circuitpython_mocks.busio.SPI
        :members: readinto, write, write_readinto, configure, frequency
    .. autoclass:: circuitpython_mocks.busio.UART
        :members: readinto, readline, write

        .. py:class:: circuitpython_mocks.busio.UART.Parity

            A mock enumeration of :external:py:class:`busio.Parity`.

            .. py:attribute:: ODD
                :type: Parity
            .. py:attribute:: EVEN
                :type: Parity

``busio.operations``
--------------------

.. automodule:: circuitpython_mocks.busio.operations

    I2C operations
    **************

    .. autoclass:: circuitpython_mocks.busio.operations.I2CRead
    .. autoclass:: circuitpython_mocks.busio.operations.I2CWrite
    .. autoclass:: circuitpython_mocks.busio.operations.I2CTransfer

    SPI operations
    **************

    .. autoclass:: circuitpython_mocks.busio.operations.SPIRead
    .. autoclass:: circuitpython_mocks.busio.operations.SPIWrite
    .. autoclass:: circuitpython_mocks.busio.operations.SPITransfer

    UART operations
    ***************

    .. autoclass:: circuitpython_mocks.busio.operations.UARTRead
    .. autoclass:: circuitpython_mocks.busio.operations.UARTWrite
