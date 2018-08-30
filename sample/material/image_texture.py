import math
import logging

from PIL import Image

from sample.material.texture import Texture
from sample.raytracing.vector3 import Vector3
from sample.utils.math_utils import MathUtils

# todo not workking
class ImageTexture(Texture):

    def __init__(self, texture_file_path:str):
        super().__init__()
        # TODO Currently, the pixel data is stored in a python array, change it to a numpy array
        # Read the texture_file_path with the Pillow module

        try:
            image = Image.open(texture_file_path)
            self._texture_data = list(image.getdata())
            self._width = image.size[0]
            self._height = image.size[1]
        except IOError as e:
            logging.error(f'Error when loaded a TextureImage: {e}')

    def value(self, u: float, v: float, p:Vector3) -> Vector3:
        i = u * self._width
        j = (1 - v) * self._height - 0.001
        i = MathUtils.clamp(i, 0, self._width - 1)
        j = MathUtils.clamp(j, 0, self._height - 1)
        r = int(self._texture_data[int(i + self._width * j)][0]) / 255.0
        g = int(self._texture_data[int(i + self._width * j)][1]) / 255.0
        b = int(self._texture_data[int(i + self._width * j)][2]) / 255.0


        return Vector3(r,g,b)
