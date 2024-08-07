CircuitPython-mocks documentation
=================================

This library contains mock data structures to be used when soft-testing CircuitPython-based
projects (with `pytest <https://docs.pytest.org/en/latest>`_).

Mocking expected behavior
-------------------------

.. autoclass:: circuitpython_mocks._mixins.Expecting
    :members: expectations, done

Pytest fixtures
---------------

.. automodule:: circuitpython_mocks.fixtures
    :members:

Mocked API
----------

.. toctree::
    :maxdepth: 2

    busio
    digitalio
    board
