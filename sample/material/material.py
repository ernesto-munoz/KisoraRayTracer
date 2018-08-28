import random

from abc import ABC, abstractmethod
from sample.raytracing.vector3 import Vector3

class Material(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def scatter(self, ray_incident, hit_record):
        """Calculates the scatter and the attenuation in this material when a ray creates a hit_record on it.

        :param ray_incident: Ray incident in to the material
        :type ray_incident: Ray
        :param hit_record: hit record of the hit
        :type hit_record: HitRecord
        :return attenuation: attenuation
        :rtype attenuation: Vector3
        :return scattered: scatter
        :rtype scattered: Vector3
        """
        pass

    def random_in_unit_sphere(self):
        p = Vector3(1.0, 1.0, 1.0)
        while p.length() >= 1.0:
            p = 2.0 * Vector3(random.random(), random.random(), random.random()) - Vector3(1, 1, 1)

        return p