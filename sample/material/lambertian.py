from sample.material.material import Material
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.ray import Ray


class Lambertian(Material):

    def __init__(self, albedo):
        """ Lamberian Material
        :param albedo: albedo color of the material
        :type albedo: Vector3
        """
        super().__init__()
        self._albedo = albedo


    def scatter(self, ray_incident:Ray, hit_record:HitRecord):
        target = hit_record.hit_point + hit_record.hit_point_normal + self.random_in_unit_sphere()
        scattered = Ray(hit_record.hit_point, target - hit_record.hit_point, ray_incident.time)
        attenuation = self._albedo
        return scattered, attenuation