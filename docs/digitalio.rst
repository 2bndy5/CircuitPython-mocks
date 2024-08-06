``digitalio``
=================

.. automodule:: circuitpython_mocks.digitalio

    .. autoclass:: circuitpython_mocks.digitalio.DigitalInOut
        :members: value, deinit, direction, drive_mode, pull, switch_to_input, switch_to_output

    .. py:class:: circuitpython_mocks.digitalio.Direction

        A mock enumeration of :external:py:class:`digitalio.Direction`.

        .. py:attribute:: INPUT
            :type: Direction
        .. py:attribute:: OUTPUT
            :type: Direction

    .. py:class:: circuitpython_mocks.digitalio.DriveMode

        A mock enumeration of :external:py:class:`digitalio.DriveMode`.

        .. py:attribute:: PUSH_PULL
            :type: DriveMode
        .. py:attribute:: OPEN_DRAIN
            :type: DriveMode

    .. py:class:: circuitpython_mocks.digitalio.Pull

        A mock enumeration of :external:py:class:`digitalio.Pull`.

        .. py:attribute:: UP
            :type: Pull
        .. py:attribute:: DOWN
            :type: Pull


``digitalio.operations``
------------------------

.. automodule:: circuitpython_mocks.digitalio.operations

    .. autoclass:: circuitpython_mocks.digitalio.operations.SetState
    .. autoclass:: circuitpython_mocks.digitalio.operations.GetState
