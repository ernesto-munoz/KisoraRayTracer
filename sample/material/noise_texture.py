import math

from sample.material.texture import Texture
from sample.raytracing.noise import Perlin
from sample.raytracing.vector3 import Vector3


class NoiseTexture(Texture):

    def __init__(self, scale: float=1.0):
        super().__init__()
        self._noise = Perlin()
        self._scale = scale

    def value(self, u: float, v: float, p: Vector3):
        # return Vector3(1, 1, 1) * 0.5 * (1 + self._noise.turb(p=self._scale * p))
        # return Vector3(1, 1, 1) * self._noise.turb(self._scale * p)
        return Vector3(1, 1, 1) * 0.5 * (1 + math.sin(self._scale * p.z() + 10 * self._noise.turb(p)))