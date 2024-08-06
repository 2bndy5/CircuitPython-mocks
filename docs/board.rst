``board``
=================

.. automodule:: circuitpython_mocks.board
    :members:

This module includes the following dummy pins for soft-testing:

.. jinja:: board

    .. hlist::
        :columns: 5

        {% for pin in pins -%}
        - ``{{pin}}``
        {% endfor %}
