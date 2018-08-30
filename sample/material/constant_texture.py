from sample.material.texture import Texture
from sample.raytracing.vector3 import Vector3


class ConstantTexture(Texture):

    def __init__(self, color:Vector3):
        super().__init__()
        self._color = color

    def value(self, u: float, v: float, p:Vector3) -> Vector3:
        return self._color