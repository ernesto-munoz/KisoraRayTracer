from sample.raytracing.aabb import AABB
from sample.raytracing.hitable import Hitable

class HitableList(Hitable):

    _list_of_hitables = None

    def __init__(self, list_of_hitables=None):
        super().__init__()
        self._list_of_hitables = list_of_hitables

    def lenght(self):
        return len(self._list_of_hitables)

    def hit(self, ray, t_min, t_max):
        final_hit_record = None
        hit_anything = False
        closest_so_far = t_max
        for h in self._list_of_hitables:
            has_hit, hit_record = h.hit(ray=ray, t_min=t_min, t_max=closest_so_far)
            if has_hit is True:
                hit_anything = True
                closest_so_far = hit_record.t
                final_hit_record = hit_record

        return hit_anything, final_hit_record


    def bounding_box(self, t0: float, t1: float) -> AABB:
        if len(self._list_of_hitables) < 1:
            return None

        temp_box = self._list_of_hitables[0].bounding_box(t0, t1)

        if temp_box is None:
            return None
        else:
            box = temp_box

        for i in range(1, len(self._list_of_hitables)):
            temp_box = self._list_of_hitables[i].bounding_box(t0, t1)
            if temp_box is not None:
                box = AABB.surrounding_box(box0=box, box1=temp_box)
            else:
                return None

        return box

