
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-neopixel/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

Higher level NeoPixel driver that presents the strip as a sequence. This is a
supercharged version of the original MicroPython driver. Its now more like a
normal Python sequence and features slice support, ``repr`` and ``len`` support.

Colors are now stored as ints by default rather than tuples. However, you can
still use the tuple syntax to set values. For example, ``0x100000`` is equivalent
to ``(0x10, 0, 0)``.

.. note:: This API represents the brightness of the white pixel when present by
  setting the RGB channels to identical values. For example, full white is
  0xffffff but is actually (0, 0, 0, 0xff) in the tuple syntax. Setting a pixel
  value with an int will use the white pixel if the RGB channels are identical.
  For full, independent, control of each color component use the tuple syntax
  and ignore the readback value.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

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
`Circuit Playground Express <https://www.adafruit.com/product/3333>`_. It turns off
``auto_write`` so that all pixels are updated at once.

.. code-block:: python

    import board
    import neopixel

    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
    pixels[0] = (10, 0, 0)
    pixels[9] = (0, 10, 0)
    pixels.show()

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
   :maxdepth: 2

   api
