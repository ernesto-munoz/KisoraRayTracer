import random

from abc import ABC, abstractmethod

# from sample.raytracing.hit_record import HitRecord
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3

class Material(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def scatter(self, ray_incident:Vector3, hit_record) -> (Ray, float):
        """Calculates the scatter and the attenuation in this material when a ray creates a hit_record on it.
        """
        pass

    @abstractmethod
    def emitted(self, u: float, v: float, p: Vector3) -> Vector3:
        return Vector3(0.0, 0.0, 0.0)

    def random_in_unit_sphere(self):
        p = Vector3(1.0, 1.0, 1.0)
        while p.length() >= 1.0:
            p = 2.0 * Vector3(random.random(), random.random(), random.random()) - Vector3(1, 1, 1)

        return p