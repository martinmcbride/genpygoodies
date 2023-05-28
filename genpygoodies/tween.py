# Author:  Martin McBride
# Created: 2023-05-28
# Copyright (C) 2023, Martin McBride
# License: MIT
"""
The tween module provides some utility functions and classes for creating commonly used `Tween` objects using the
generativepy Tween class.
"""
from itertools import cycle

from generativepy.tween import Tween


def tween_alpha_on(time, *times, off=0, on=1, fade=0.5):
    """
    Fade an alpha value from off to on after a time period. Optionally fade off, on, off, on subsequent times.
    Each time must be greater than the previous time, and the minimum gap between times is the fade time.

    The default values are off=0 and on=1, so the Tween is suitable for use as an alpha value to make an object appear
    and disappear.

    **Parameters**

    * `time`: number - the time (in seconds) to turn the Tween on.
    * `times`: iterable(number) - optional extra times to alternately turn the tween off (then on, then off...)
    * `off`: number - off value (0 by default).
    * `on`: number - on value (1 by default).
    * `fade`: number - fade time (0.5 by default).

    **Returns**

    A configured `Tween` object.

    **Usage**
    This simple example creates a `Tween` that has value 0 for 2 seconds, then rises to 1 over 0.5 seconds, and stays at
    1 forever:

    ```
    tween = tween_alpha_on(2)
    ```

    This example creates a `Tween` that has value 0 for 2 seconds, then rises to 1 over 0.5 seconds. When the
    time reaches 5 seconds, it falls to 0 over 0.5 seconds:

    ```
    tween = tween_alpha_on(2, 5)
    ```

    This example creates a `Tween` that has value 0.2 for 3 seconds, then rises to 0.8 over 2 seconds, and stays at
    0.8 forever:

    ```
    tween = tween_alpha_on(3, off=0.2, on=0.8, fade=2)
    ```
    """
    tw = Tween(off).wait(time).to_d(on, fade)
    for t, v in zip(times, cycle((off, on))):
        tw.wait(t).to_d(v, fade)
    return tw


def tween_alpha_off(time, *times, off=0, on=1, fade=0.5):
    """
    Fade an alpha value from on to off after a time period. Optionally fade on, off, on, on subsequent times.

    This function is very similar to `tween_alpha_on` except that it starts on and turn off after a time delay.

    **Parameters**

    * `time`: number - the time (in seconds) to turn the Tween off.
    * `times`: iterable(number) - optional extra times to alternately turn the tween oon (then off, then onn...)
    * `off`: number - off value (0 by default).
    * `on`: number - on value (1 by default).
    * `fade`: number - fade time (0.5 by default).

    **Returns**

    A configured `Tween` object.
    """
    tw = Tween(on).wait(time).to_d(off, fade)
    for t, v in zip(times, cycle((on, off))):
        tw.wait(t).to_d(v, fade)
    return tw


