import random
import math

from sample.geometry.flip_normals import FlipNormals
from sample.geometry.rect import XYRect, XZRect, YZRect
from sample.material.isotropic import Isotropic
from sample.material.material import Material
from sample.material.texture import Texture
from sample.raytracing.aabb import AABB
from sample.raytracing.hitable import Hitable
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3
from sample.raytracing.hit_record import HitRecord


class ConstantVolume(Hitable):

    def __init__(self, boundary:Hitable, density:float, texture:Texture):
        """Volume defined from another Hitable"""
        super().__init__()

        self._boundary = boundary
        self._density = density
        self._texture = texture
        # create the phase function with the Isotropic material and the texture
        self._phase_function = Isotropic(texture=texture)


    def hit(self, ray:Ray, t_min:float, t_max:float) -> (bool, HitRecord):
        """Checks if the ray 'ray' hits with any of the walls between t_min and t_max."""
        db = False
        has_hit, rec1 = self._boundary.hit(ray=ray, t_min=-float('inf'), t_max=float('inf'))
        if has_hit is True:
            has_hit_again, rec2 = self._boundary.hit(ray=ray, t_min= rec1.t + 0.0001, t_max=float('inf'))
            if has_hit_again is True:


                if rec1.t < t_min:
                    rec1.t = t_min
                if rec2.t > t_max:
                    rec2.t = t_max

                if db:
                    print(f't0 t1 {rec1.t} {rec2.t}')
                if rec1.t >= rec2.t:
                    return False, None
                if rec1.t < 0:
                    rec1.t = 0

                distance_inside_boundary = ray.direction.length() * (rec2.t - rec1.t)
                hit_distance = -(1 / self._density) * math.log10(random.random())  # base 10 ?

                if db:
                    print(f'DATA: {hit_distance} {distance_inside_boundary} {hit_distance < distance_inside_boundary}')

                if hit_distance < distance_inside_boundary:
                    if db:
                        print(f'hit distance = {hit_distance}')
                    hit_record = HitRecord()
                    hit_record.t = rec1.t + hit_distance / ray.direction.length()
                    if db:
                        print(f'rec.t = {hit_record.t}')
                    hit_record.hit_point = ray.point_at_parameter(hit_record.t)
                    if db:
                        print(f'rec.hit_point = {hit_record.hit_point}')
                    hit_record.hit_point_normal = Vector3(1, 0, 0)
                    hit_record.material = self._phase_function

                    return True, hit_record

        return False, None


    def bounding_box(self, t0: float, t1: float) -> AABB:
        return self._boundary.bounding_box(t0=t0, t1=t1)