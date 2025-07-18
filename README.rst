Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-is31fl3741/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/is31fl3741/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

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
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-is31fl3741

Usage Example
=============

Matrix:

.. code:: python

    import time
    import board
    import adafruit_is31fl3741

    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    is31 = adafruit_is31fl3741.IS31FL3741(i2c)

    is31.set_led_scaling(0xFF)  # turn on LEDs all the way
    is31.global_current = 0xFF  # set current to max
    is31.enable = True  # enable!

    # light up every LED, one at a time
    while True:
        for pixel in range(351):
            is31[pixel] = 255
            time.sleep(0.01)
            is31[pixel] = 0

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/is31fl3741/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_is31fl3741/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
