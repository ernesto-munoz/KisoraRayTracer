import math

from sample.material.material import Material
from sample.raytracing.aabb import AABB
from sample.raytracing.hitable import Hitable
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3
from sample.raytracing.hit_record import HitRecord
from sample.utils.math_utils import MathUtils


class Sphere(Hitable):

    def __init__(self, center:Vector3, radius:float, material:Material, center_destiny:Vector3=None, time0:float=0.0, time1:float=1.0):
        """Sphere with center, radius and a material

        :param center: center of the sphere
        :type center: Vector3
        :param radius: radios of the sphere
        :type radius: float
        :param material: material of the sphere
        :type material: Material
        """
        super().__init__()
        self._center = center
        self._radius = radius
        self._material = material
        self._center_destiny = center_destiny if center_destiny is not None else center
        self._time0 = time0
        self._time1 = time1

    def get_center(self, t:float):
        return self._center + ((t - self._time0) / (self._time1 - self._time0)) * (self._center_destiny - self._center)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self.radius = value

    def get_sphere_uv(self, p:Vector3) -> (float, float):
        """Get the uv coordinates of a point in the sphere"""
        d = Vector3.normalize(p - self._center)

        phi = math.atan2(d.z(), d.x()) / (2 * math.pi)
        u = phi + 0.5

        v = 0.5 - (math.asin(d.y()) / math.pi)
        return u, v

    def hit(self, ray:Ray, t_min:float, t_max:float) -> (bool, HitRecord):
        """Checks if the ray 'ray' hits with the sphere between t_min and t_max.
        Returns true if there is a collision, false otherwise.
        Return the hitRecord information if the collision is true.
        """
        current_center = self.get_center(t=ray.time)

        oc = ray.origin - current_center

        a = Vector3.dot(ray.direction, ray.direction)
        b = Vector3.dot(oc, ray.direction)
        c = Vector3.dot(oc, oc) - self._radius * self._radius
        discriminant = b * b - a * c

        if discriminant > 0:
            temp = (-b - math.sqrt(b * b - a * c)) / a
            if t_max > temp > t_min:
                record = HitRecord()
                record.t = temp
                record.hit_point = ray.point_at_parameter(record.t)
                record.hit_point_normal = (record.hit_point - current_center) / self._radius
                record.u, record.v = self.get_sphere_uv(p=record.hit_point)
                record.material = self._material
                return True, record
            temp = (-b + math.sqrt(b * b - a * c)) / a
            if t_max > temp > t_min:
                record = HitRecord()
                record.t = temp
                record.hit_point = ray.point_at_parameter(record.t)
                record.hit_point_normal = (record.hit_point - current_center) / self._radius
                record.u, record.v = self.get_sphere_uv(p=record.hit_point)
                record.material = self._material
                return True, record

        return False, None

    def bounding_box_on_time(self, time:float) -> AABB:
        box = AABB(self.get_center(time) - Vector3(self._radius, self._radius, self._radius),
                   self.get_center(time) + Vector3(self._radius, self._radius, self._radius)
                   )
        return box

    def __str__(self):
        return f'Sphere Radius:{self._radius} Center0:{self.get_center(0)} Center1:{self.get_center(1)}'

    def bounding_box(self, t0: float, t1: float) -> AABB:
        box0 = self.bounding_box_on_time(time=t0)
        box1 = self.bounding_box_on_time(time=t1)
        return AABB.surrounding_box(box0=box0, box1=box1)
