Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-is31fl3741/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/is31fl3741/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741/actions/
    :alt: Build Status

CircuitPython driver for the IS31FL3741 RGB Matrix IC.

This driver supports the following hardware:


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-is31fl3741/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-is31fl3741

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-is31fl3741

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-is31fl3741

Usage Example
=============

Matrix:

.. code:: python

    from adafruit_is31fl3741.matrix import Matrix
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = Matrix(i2c)
        display.fill(127)


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/is31fl3741/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_is31fl3741/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
