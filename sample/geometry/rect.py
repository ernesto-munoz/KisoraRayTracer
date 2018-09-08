import math
import random

from sample.material.material import Material
from sample.raytracing.aabb import AABB
from sample.raytracing.hitable import Hitable
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3
from sample.raytracing.records import HitRecord


class XYRect(Hitable):

    def __init__(self, x0: float, x1: float, y0: float, y1: float, k: float, material: Material):
        """Plane defined in the Z Axis"""
        super().__init__()
        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1
        self._k = k
        self._material = material

    def hit(self, ray: Ray, t_min: float, t_max: float) -> (bool, HitRecord):
        """Checks if the ray 'ray' hits with the plane between t_min and t_max.
        Returns true if there is a collision, false otherwise.
        Return the hitRecord information if the collision is true.
        """
        if ray.direction.z() == 0.0:
            return False, None

        t = (self._k - ray.origin.z()) / ray.direction.z()
        if t < t_min or t > t_max:
            return False, None

        x = ray.origin.x() + t * ray.direction.x()
        y = ray.origin.y() + t * ray.direction.y()

        if x < self._x0 or x > self._x1 or y < self._y0 or y > self._y1:
            return False, None

        record = HitRecord()
        record.t = t
        record.hit_point = ray.point_at_parameter(record.t)
        record.hit_point_normal = Vector3(0, 0, 1)

        record.u = (x - self._x0) / (self._x1 - self._x0)
        record.v = (y - self._y0) / (self._y1 - self._y0)
        record.material = self._material

        return True, record

    def bounding_box(self, t0: float, t1: float) -> AABB:
        return AABB(min=Vector3(self._x0, self._y0, self._k - 0.0001), max=Vector3(self._x1, self._y1, self._k + 0.0001))

    def __str__(self):
        return f'Plane: {self.bounding_box(0, 0).__str__()}'


class XZRect(Hitable):

    def __init__(self, x0: float, x1: float, z0: float, z1: float, k: float, material: Material):
        """Plane defined in the Z Axis"""
        super().__init__()
        self._x0 = x0
        self._x1 = x1
        self._z0 = z0
        self._z1 = z1
        self._k = k
        self._material = material

    def hit(self, ray: Ray, t_min: float, t_max: float) -> (bool, HitRecord):
        """Checks if the ray 'ray' hits with the plane between t_min and t_max.
        Returns true if there is a collision, false otherwise.
        Return the hitRecord information if the collision is true.
        """
        if ray.direction.y() == 0.0:
            return False, None

        t = (self._k - ray.origin.y()) / ray.direction.y()
        if t < t_min or t > t_max:
            return False, None

        x = ray.origin.x() + t * ray.direction.x()
        z = ray.origin.z() + t * ray.direction.z()

        if x < self._x0 or x > self._x1 or z < self._z0 or z > self._z1:
            return False, None

        record = HitRecord()
        record.t = t
        record.hit_point = ray.point_at_parameter(record.t)
        record.hit_point_normal = Vector3(0, 1, 1)

        record.u = (x - self._x0) / (self._x1 - self._x0)
        record.v = (z - self._z0) / (self._z1 - self._z0)
        record.material = self._material

        return True, record

    def bounding_box(self, t0: float, t1: float) -> AABB:
        return AABB(min=Vector3(self._x0, self._z0, self._k - 0.0001), max=Vector3(self._x1, self._z1, self._k + 0.0001))

    def __str__(self):
        return f'Plane: {self.bounding_box(0, 0).__str__()}'


class YZRect(Hitable):

    def __init__(self, y0: float, y1: float, z0: float, z1: float, k: float, material: Material):
        """Plane defined in the Z Axis"""
        super().__init__()
        self._y0 = y0
        self._y1 = y1
        self._z0 = z0
        self._z1 = z1
        self._k = k
        self._material = material

    def hit(self, ray: Ray, t_min: float, t_max: float) -> (bool, HitRecord):
        """Checks if the ray 'ray' hits with the plane between t_min and t_max.
        Returns true if there is a collision, false otherwise.
        Return the hitRecord information if the collision is true.
        """
        if ray.direction.x() == 0.0:
            return False, None

        t = (self._k - ray.origin.x()) / ray.direction.x()
        if t < t_min or t > t_max:
            return False, None

        y = ray.origin.y() + t * ray.direction.y()
        z = ray.origin.z() + t * ray.direction.z()

        if y < self._y0 or y > self._y1 or z < self._z0 or z > self._z1:
            return False, None

        record = HitRecord()
        record.t = t
        record.hit_point = ray.point_at_parameter(record.t)
        record.hit_point_normal = Vector3(1, 0, 0)

        record.u = (y - self._y0) / (self._y1 - self._y0)
        record.v = (z - self._z0) / (self._z1 - self._z0)
        record.material = self._material

        return True, record

    def bounding_box(self, t0: float, t1: float) -> AABB:
        return AABB(min=Vector3(self._y0, self._z0, self._k - 0.0001), max=Vector3(self._y1, self._z1, self._k + 0.0001))

    def __str__(self):
        return f'Plane: {self.bounding_box(0, 0).__str__()}'
