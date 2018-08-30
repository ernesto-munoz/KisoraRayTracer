from sample.material.material import Material
from sample.material.texture import Texture
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3
from sample.utils.math_utils import MathUtils


class Isotropic(Material):

    def __init__(self, texture:Texture):
        super().__init__()
        self._texture = texture

    def scatter(self, ray_incident:Ray, hit_record:HitRecord) -> (Ray, Vector3):
        scattered = Ray(origin=hit_record.hit_point, direction=self.random_in_unit_sphere())
        attenuation = self._texture.value(hit_record.u, hit_record.v, hit_record.hit_point)
        return scattered, attenuation

    def emitted(self, u: float, v: float, p: Vector3) -> Vector3:
        return Vector3(0.0, 0.0, 0.0)