"""Resources related with fractals.

Refs:
 - https://realpython.com/mandelbrot-set-python/
"""

from dataclasses import dataclass
import math
from typing import Union

import numpy as np
import matplotlib.pyplot as plt


def mandelbrot_sequence(c):
    """Returns generator of the Mandelbrot sequence given C"""
    z = 0
    while True:
        yield z
        z = z**2 + c


def julia_sequence(c, z=0):
    """Returns generator of a Julia sequence given C and Z!=0

    Note: if Z=0 then Julia_seq==Mandelbrot_seq
    """
    while True:
        yield z
        z = z**2 + c


def mandelbrot_sequence_index(n, c):
    """Returns the n-th value of the Mandelbrot sequence given C"""
    if n == 0:
        return 0
    else:
        return mandelbrot_sequence_index(n - 1, c) ** 2 + c


def pixel_matrix(pixel_density, xmin=-2, xmax=0.5, ymin=-1.5, ymax=1.5):
    """Generate a matrix for plotting Mandelbrot/Julia sets.

    Args:
     - pixel_density: Number of pixels per unit
    """
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j


def is_mandelbrot_elem(c, num_iterations):
    """Returns if a value is stable (relatively small) and is element of Mandelbrot set"""
    z = 0
    for _ in range(num_iterations):
        z = z**2 + c
    return abs(z) <= 2


def mask_pixel_matrix(c, num_iterations):
    """Return pixel_matrix with bool elements indicating if pixel is Mandelbrot elem"""
    mask = is_mandelbrot_elem(c, num_iterations)
    return c[mask]


def plot_mandelbrot_ori(pixel_density=21):
    """Plot replica of first ever visualization of Mandelbrot set"""

    c = pixel_matrix(pixel_density=pixel_density)
    members = mask_pixel_matrix(c, num_iterations=20)

    plt.scatter(members.real, members.imag, color="black", marker=",", s=1)
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def plot_mandelbrot(pixel_density=512):
    """Plot Mandelbrot set"""
    c = pixel_matrix(pixel_density=pixel_density)

    plt.imshow(is_mandelbrot_elem(c, num_iterations=20), cmap="binary")
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


@dataclass
class MandelbrotSet:
    """Encapsulates the logic to compute if a value is element of Mandelbrot set.

    Optionally return a value between 0 and 1 if the approximation is not enough.
    """

    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex, smooth=False) -> Union[int, float]:
        z = 0
        for iteration in range(self.max_iterations):
            z = z**2 + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - math.log(math.log(abs(z))) / math.log(2)
                return iteration
        return self.max_iterations
