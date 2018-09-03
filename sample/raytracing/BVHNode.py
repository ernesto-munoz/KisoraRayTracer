import random
import logging

from sample.raytracing.vector3 import Vector3

from sample.raytracing.aabb import AABB
from sample.raytracing.hit_record import HitRecord
from sample.raytracing.hitable import Hitable
from sample.raytracing.ray import Ray


class BVHNode(Hitable):

    def __init__(self, list_of_hitables: list, n: int, time0: float, time1: float):
        super().__init__()

        # Choose a random Axis
        random_axis = random.choice(['x', 'y', 'z'])

        # Sort the list of hitables with in this random axis
        sorted_list_of_hitables = sorted(list_of_hitables, key=lambda x: getattr(x.bounding_box(t0=time0, t1=time1).min, random_axis)())

        # put half in each subtree
        if n == 1:
            self._left = self._right = sorted_list_of_hitables[0]
        elif n == 2:
            self._left = sorted_list_of_hitables[0]
            self._right = sorted_list_of_hitables[1]
        else:
            self._left = BVHNode(list_of_hitables=sorted_list_of_hitables[0:int(n/2)], n=int(n / 2), time0=time0, time1=time1)
            self._right = BVHNode(list_of_hitables=sorted_list_of_hitables[int(n/2):], n=n - int(n / 2), time0=time0, time1=time1)

        left_bb = self._left.bounding_box(t0=time0, t1=time1)
        right_bb = self._right.bounding_box(t0=time0, t1=time1)
        if left_bb is None or right_bb is None:
            logging.info('No bounding box in BVHNode constructor')

        self._box = AABB.surrounding_box(left_bb, right_bb)

    def print_it(self):
        print(f'BVHNode: {self._box}')
        if self._left is not None:
            if type(self._left) is not BVHNode:
                print(self._left)
            else:
                self._left.print_it()
        if self._right is not None:
            if type(self._right) is not BVHNode:
                print(self._right)
            else:
                self._right.print_it()

    def hit(self, ray:Ray, t_min: float, t_max: float) -> (bool, HitRecord):
        if self._box.hit(ray=ray, tmin=t_min, tmax=t_max):

            left_hit, left_hit_rec = self._left.hit(ray=ray, t_min=t_min, t_max=t_max)
            right_hit, right_hit_rec = self._right.hit(ray=ray, t_min=t_min, t_max=t_max)
            if left_hit is True and right_hit is True:
                if left_hit_rec.t < right_hit_rec.t:
                    return True, left_hit_rec
                else:
                    return True, right_hit_rec
            elif left_hit is True:
                return True, left_hit_rec
            elif right_hit is True:
                return True, right_hit_rec
            else:
                return False, None
        return False, None

    def bounding_box(self, t0: float, t1: float) -> AABB:
        return self._box
