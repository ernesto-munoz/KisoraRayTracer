import math
import random

from sample.material.material import Material
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.vector3 import Vector3
from sample.raytracing.ray import Ray


class Dielectric(Material):

    def __init__(self, refraction_index):
        """Dielectric Material

        :param retraction_index: index of refraction of the material
        :type retraction_index: float
        """
        super().__init__()
        self._refraction_index = refraction_index

    def scatter(self, ray_incident:Ray, hit_record:HitRecord):

        reflected_vector = Vector3.reflect(Vector3.normalize(ray_incident.direction), hit_record.hit_point_normal)
        attenuation = Vector3(1.0, 1.0, 1.0)

        refracted_vector = Vector3.refract(incident=ray_incident.direction,
                                           normal=hit_record.hit_point_normal,
                                           n1=1.0,
                                           n2=self._refraction_index
                                           )
        reflect_probability = self.schlick(incident=ray_incident.direction,
                                           normal=hit_record.hit_point_normal,
                                           n1=1.0,
                                           n2=self._refraction_index)

        if random.random() < reflect_probability:
            scattered = Ray(hit_record.hit_point, reflected_vector, ray_incident.time)
        else:
            scattered = Ray(hit_record.hit_point, refracted_vector, ray_incident.time)

        return scattered, attenuation

    def schlick(self, incident:'Vector3', normal:'Vector3', n1:'float', n2:'float'):
        r0 = (n1 - n2) / (n1 + n2)
        r0 *= r0
        cosX = Vector3.dot(normal, incident)
        if n1 > n2:
            n = n1 / n2
            sinT2 = n * n * (1.0 - cosX * cosX)
            if sinT2 > 1.0:
                return 1.0
            cosX = math.sqrt(1.0 - sinT2)

        x = 1.0 - cosX
        return r0 + (1.0 - r0) * math.pow(x, 5)

    def emitted(self, u: float, v: float, p: Vector3) -> Vector3:
        return Vector3(0.0, 0.0, 0.0)