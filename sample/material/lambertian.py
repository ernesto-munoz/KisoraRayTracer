from sample.material.constant_texture import ConstantTexture
from sample.material.material import Material
from sample.material.texture import Texture
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3


class Lambertian(Material):

    def __init__(self, albedo: Vector3=Vector3(1.0, 1.0, 1.0), texture: Texture=None):
        """ Lamberian Material
        :param albedo: albedo color of the material
        :type albedo: Vector3
        """
        super().__init__()
        self._albedo = albedo
        self._texture = ConstantTexture(Vector3(1.0, 1.0, 1.0)) if texture is None else texture

    def scatter(self, ray_incident:Ray, hit_record:HitRecord):
        target = hit_record.hit_point + hit_record.hit_point_normal + self.random_in_unit_sphere()
        scattered = Ray(hit_record.hit_point, target - hit_record.hit_point, ray_incident.time)
        attenuation = self._albedo * self._texture.value(hit_record.u, hit_record.v, hit_record.hit_point)
        return scattered, attenuation

    def emitted(self, u: float, v: float, p: Vector3) -> Vector3:
        return Vector3(0.0, 0.0, 0.0)