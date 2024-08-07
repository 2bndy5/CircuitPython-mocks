"""A module that contains pytest fixtures.

.. _pytest_plugins: https://docs.pytest.org/en/latest/how-to/fixtures.html#using-fixtures-from-other-projects

These fixtures are made available by defining a `pytest_plugins`_ global attribute in
the test module (or in conftest.py module).

.. code-block:: python
    :caption: conftest.py

    pytest_plugins = ["circuitpython_mocks.fixtures"]
"""

from pathlib import Path
import pytest


@pytest.fixture()
def mock_blinka_imports(monkeypatch: pytest.MonkeyPatch):
    """A pytest fixture that monkey patches the Python runtime's import paths, such
    that this package's mock modules can be imported first (instead of using the
    adafruit-blinka package).

    .. md-tab-set::

        .. md-tab-item:: I2C

            .. literalinclude:: ../tests/test_i2c_fixture.py
                :language: python

        .. md-tab-item:: SPI

            .. literalinclude:: ../tests/test_spi_fixture.py
                :language: python

        .. md-tab-item:: UART

            .. literalinclude:: ../tests/test_uart_fixture.py
                :language: python

        .. md-tab-item:: DigitalInOut

            .. literalinclude:: ../tests/test_dio_fixture.py
                :language: python
    """
    root_pkg = Path(__file__).parent
    monkeypatch.syspath_prepend(str(root_pkg))
