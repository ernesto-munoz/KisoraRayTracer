import math

from sample.material.texture import Texture
from sample.raytracing.vector3 import Vector3


class CheckerTexture(Texture):

    def __init__(self, texture0:Texture, texture1:Texture):
        super().__init__()
        self._texture0 = texture0
        self._texture1 = texture1

    def value(self, u: float, v: float, p:Vector3) -> Vector3:
        sines = math.sin(10 * p.x()) * math.sin(10*p.y()) * math.sin(10*p.z())
        if sines < 0:
            return self._texture0.value(u, v, p)
        else:
            return self._texture1.value(u, v, p)