
Adafruit CircuitPython NeoPixel
===============================

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-neopixel/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/neopixel/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_Bundle/blob/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

Higher level NeoPixel driver that presents the strip as a sequence. This is a
supercharged version of the original MicroPython driver. Its now more like a
normal Python sequence and features slice support, ``repr`` and ``len`` support.

Colors are stored as tuples by default. However, you can also use int hex syntax
to set values similar to colors on the web. For example, ``0x100000`` (``#100000``
on the web) is equivalent to ``(0x10, 0, 0)``.

.. note:: The int hex API represents the brightness of the white pixel when
  present by setting the RGB channels to identical values. For example, full
  white is 0xffffff but is actually (0, 0, 0, 0xff) in the tuple syntax. Setting
  a pixel value with an int will use the white pixel if the RGB channels are
  identical. For full, independent, control of each color component use the
  tuple syntax.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit CircuitPython Pixelbuf library <https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-neopixel/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-neopixel

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-neopixel

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-neopixel

Usage Example
=============

This example demonstrates the library with the single built-in NeoPixel on the
`Feather M0 Express <https://www.adafruit.com/product/3403>`_ and
`Metro M0 Express <https://www.adafruit.com/product/3505>`_.

.. code-block:: python

    import board
    import neopixel

    pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pixels[0] = (10, 0, 0)

This example demonstrates the library with the ten built-in NeoPixels on the
`Circuit Playground Express <https://www.adafruit.com/product/3333>`_. It turns
off ``auto_write`` so that all pixels are updated at once when the ``show``
method is called.

.. code-block:: python

    import board
    import neopixel

    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
    pixels[0] = (10, 0, 0)
    pixels[9] = (0, 10, 0)
    pixels.show()

This example demonstrates using a single NeoPixel tied to a GPIO pin and with
a ``pixel_order`` to specify the color channel order. Note that ``bpp`` does not
need to be specified as it is computed from the supplied ``pixel_order``.

.. code-block:: python

    import board
    import neopixel

    pixel = neopixel.NeoPixel(board.D0, 1, pixel_order=neopixel.RGBW)
    pixel[0] = (30, 0, 20, 10)

Setup for sudo-less usage on Raspberry Pi boards
================================================
1. Enable both SPI and Serial port hardware (Serial interface). Do it by ``raspi-config`` tool or manually by adding

   ::

      dtparam=spi=on
      enable_uart=1

   to the ``/boot/config.txt``

2. Reboot the Pi to apply the changes - the hardware setup takes place during boot.
3. Connect LED's DIN to ``GPIO10`` (physical pin 19)

When initializing the ``NeoPixel`` object **always** do it with ``board.D10`` (GPIO10)

.. code-block:: python

    import board
    import neopixel

    DATA_PIN = board.D10
    pixel = neopixel.NeoPixel(DATA_PIN, ...)

Now you can execute the code using ``python`` without ``sudo``

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/neopixel/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
