from sample.raytracing.vector3 import Vector3


class Ray(object):

    def __init__(self, origin:Vector3=None, direction:Vector3=None, ti:float=0.0):
        self._origin = origin
        self._direction = direction
        self._time = ti

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def point_at_parameter(self, t):
        return self._origin + t * self._direction
