import math
import logging

from PIL import Image

from sample.material.texture import Texture
from sample.raytracing.vector3 import Vector3
from sample.utils.math_utils import MathUtils


class ImageTexture(Texture):

    def __init__(self, texture_file_path: str, uoffset: float=0.0, voffset: float=0.0):
        super().__init__()
        # TODO Currently, the pixel data is stored in a python array, change it to a numpy array
        # Read the texture_file_path with the Pillow module

        try:
            self._image = Image.open(texture_file_path)
            self._width = self._image.size[0]
            self._height = self._image.size[1]
            self.uoffset = uoffset
            self.voffset = voffset
        except IOError as e:
            logging.error(f'Error when loaded a TextureImage: {e}')

    def value(self, u: float, v: float, p: Vector3) -> Vector3:
        i = (self.uoffset - u) * (self._width - 1)
        j = (self.voffset + v) * (self._height - 1)
        i = i % self._width
        j = j % self._height
        # i = MathUtils.clamp(i, 0, self._width - 1)
        # j = MathUtils.clamp(j, 0, self._height - 1)

        pix = self._image.load()
        r = int(pix[i, j][0]) / 255.0
        g = int(pix[i, j][1]) / 255.0
        b = int(pix[i, j][2]) / 255.0

        return Vector3(r, g, b)
