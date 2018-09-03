import math
import random

from sample.raytracing.vector3 import Vector3
from sample.raytracing.ray import Ray


class Camera(object):

    def __init__(self, lookfrom:'Vector3', lookat:'Vector3', vectorup:'Vector3', vfov:'float', aspect:'float', aperture:'float', focus_dist:'float', t0:float, t1:float):
        theta =  vfov * math.pi / 180  # vfov to radians
        half_height = math.tan(theta / 2) # h = tan(theta / 2)
        half_width = half_height * aspect

        self._lens_radius = aperture / 2

        self._time0 = t0
        self._time1 = t1

        self._camera_origin = lookfrom
        w = Vector3.normalize(lookfrom - lookat)
        u = Vector3.normalize(Vector3.cross(vectorup, w))
        v = Vector3.cross(w, u)

        self._lower_left_corner = self._camera_origin - half_width * focus_dist * u - half_height * focus_dist * v - focus_dist*w
        self._horizontal = 2 * half_width * focus_dist * u
        self._vertical = 2 * half_height * focus_dist * v

    def get_ray(self, u, v):
        rd = self._lens_radius * self.random_in_unit_disk()
        offset = u * rd.x() + v * rd.y()
        time = self._time0 + random.random() * (self._time1 - self._time0)
        return Ray(
            origin=self._camera_origin + offset,
            direction=(self._lower_left_corner + u * self._horizontal + v * self._vertical) - self._camera_origin - offset,
            ti=time
        )

    def random_in_unit_disk(self):
        p = Vector3(1.0, 1.0, 0.0)
        while p.length() >= 1.0:
            p = 2.0 * Vector3(random.random(), random.random(), 0) - Vector3(1, 1, 0)

        return p