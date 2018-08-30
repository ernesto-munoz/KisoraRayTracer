from sample.raytracing.aabb import AABB
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.hitable import Hitable
from sample.raytracing.ray import Ray


class FlipNormals(Hitable):

    def __init__(self, hitable:Hitable):
        super().__init__()
        self._hitable = hitable

    def hit(self, ray: Ray, t_min: float, t_max: float) -> (bool, HitRecord):
        has_hit, hit_record = self._hitable.hit(ray=ray, t_min=t_min, t_max=t_max)

        if has_hit is True:
            hit_record.hit_point_normal = -hit_record.hit_point_normal
            return True, hit_record
        else:
            return False, None

    def bounding_box(self, t0: float, t1: float) -> AABB:
        return self._hitable.bounding_box(t0=t0, t1=t1)