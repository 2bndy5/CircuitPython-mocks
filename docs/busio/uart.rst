``busio.UART``
==============

.. autoclass:: circuitpython_mocks.busio.UART
    :members: readinto, readline, write, in_waiting, reset_input_buffer, timeout, baudrate

    .. py:class:: circuitpython_mocks.busio.UART.Parity

        A mock enumeration of :external:py:class:`busio.Parity`.

        .. py:attribute:: ODD
            :type: Parity
        .. py:attribute:: EVEN
            :type: Parity

UART operations
***************

.. autoclass:: circuitpython_mocks.busio.operations.UARTRead
.. autoclass:: circuitpython_mocks.busio.operations.UARTWrite
.. autoclass:: circuitpython_mocks.busio.operations.UARTFlush
