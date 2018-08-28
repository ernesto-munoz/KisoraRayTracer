from __future__ import annotations

from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3


class AABB(object):

    def __init__(self, min:Vector3, max:Vector3):
        super().__init__()
        self._min = min
        self._max = max

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    def hit(self, ray:Ray, tmin:float, tmax:float) -> bool:
        in_tmin = tmin
        in_tmax = tmax

        for axis in ['x', 'y', 'z']:
            invD = 1.0 / getattr(ray.direction, axis)()
            t0 = (getattr(self._min, axis)() - getattr(ray.origin, axis)()) * invD
            t1 = (getattr(self._max, axis)() - getattr(ray.origin, axis)()) * invD
            if invD < 0.0:
                t0, t1 = t1, t0

            in_tmin = t0 if t0 > in_tmin else in_tmin
            in_tmax = t1 if t1 < in_tmax else tmax

            if in_tmax <= in_tmin:
                return False

        return True

    def __str__(self):
        return f'AABB {self._min} {self._max}'

    @staticmethod
    def surrounding_box(box0, box1):  # try to use annotations
        smallest = Vector3(
            min(box0.min.x(), box1.min.x()),
            min(box0.min.y(), box1.min.y()),
            min(box0.min.z(), box1.min.z()),
        )

        biggest = Vector3(
            max(box0.max.x(), box1.max.x()),
            max(box0.max.y(), box1.max.y()),
            max(box0.max.z(), box1.max.z()),
        )

        return AABB(min=smallest,max=biggest)

