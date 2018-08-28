from sample.material.material import Material
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.vector3 import Vector3
from sample.raytracing.ray import Ray


class Metal(Material):

    def __init__(self, albedo:Vector3, fuzz:float):
        """ Metal Material
        """
        super().__init__()
        self._albedo = albedo
        self._fuzz = fuzz


    def scatter(self, ray_incident:Ray, hit_record:HitRecord):
        reflected_ray = Vector3.reflect(Vector3.normalize(ray_incident.direction), hit_record.hit_point_normal)
        scattered = Ray(hit_record.hit_point, reflected_ray + self._fuzz * self.random_in_unit_sphere(), ray_incident.time)
        attenuation = self._albedo

        # This avoid a scatter ray totally perpendicular to the surface normal
        if Vector3.dot(scattered.direction, hit_record.hit_point_normal) > 0:
            return scattered, attenuation
        return None, None
