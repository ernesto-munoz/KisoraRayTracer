from sample.material.constant_texture import ConstantTexture
from sample.material.material import Material
from sample.material.texture import Texture
from sample.raytracing.records import HitRecord
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3


class DiffuseLight(Material):

    def __init__(self, albedo:Vector3, texture:Texture=None):
        """ Lamberian Material
        :param albedo: albedo color of the material
        :type albedo: Vector3
        """
        super().__init__()
        self._albedo = albedo
        self._texture = ConstantTexture(Vector3(1.0, 1.0, 1.0)) if texture is None else texture

    def scatter(self, ray_incident:Ray, hit_record:HitRecord):
        """A diffuse light doesn't scatter the light"""
        return None, None

    def emitted(self, u: float, v: float, p: Vector3) -> Vector3:
        return self._texture.value(u=u, v=v, p=p)