CircuitPython-mocks documentation
=================================

.. |pytest-used-import| replace:: Some linters may object about "unused imports".
    This should be ignored as pytest does actually use the imported fixture.

This library contains mock data structures to be used when soft-testing CircuitPython-based
projects (with pytest).

.. autoclass:: circuitpython_mocks._mixins.Expecting
    :members:

.. autofunction:: circuitpython_mocks.monkey_patch_sys_paths

    .. md-tab-set::

        .. md-tab-item:: I2C

            .. literalinclude:: ../tests/test_i2c.py
                :language: python
                :end-before: def test_default():

            .. code-annotations::
                #. |pytest-used-import|

        .. md-tab-item:: SPI

            .. literalinclude:: ../tests/test_spi.py
                :language: python
                :end-before: def test_default():

            .. code-annotations::
                #. |pytest-used-import|

        .. md-tab-item:: UART

            .. literalinclude:: ../tests/test_uart.py
                :language: python
                :end-before: def test_default():

            .. code-annotations::
                #. |pytest-used-import|

        .. md-tab-item:: DigitalInOut

            .. literalinclude:: ../tests/test_dio.py
                :language: python

            .. code-annotations::
                #. |pytest-used-import|

Mocked API
************

.. toctree::
    :maxdepth: 2

    busio
    digitalio
    board
