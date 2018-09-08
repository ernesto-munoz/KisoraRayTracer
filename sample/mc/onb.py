import math

from sample.raytracing.vector3 import Vector3


class ONB:

    _u: Vector3
    _v: Vector3
    _w: Vector3

    def __init__(self):
        super().__init__()
        self._u = Vector3()
        self._v = Vector3()
        self._w = Vector3()

    def u(self):
        return self._u

    def v(self):
        return self._v

    def w(self):
        return self._w

    def local(self, a, b=None, c=None):
        if isinstance(a, float):
            return a * self._u + b * self._v + c * self._w
        elif isinstance(a, Vector3):
            return a.x() * self._u + a.y() * self._v + a.z() * self._w
        else:
            raise ValueError('parameter is not a float or Vector3')

    def build_from_w(self, n: Vector3):
        self._w = Vector3.normalize(n)
        if math.fabs(self._w.x()) > 0.9:
            a = Vector3(0, 1, 0)
        else:
            a = Vector3(1, 0, 0)

        self._v = Vector3.normalize(Vector3.cross(self._w, a))
        self._u = Vector3.cross(self._w, self._v)
