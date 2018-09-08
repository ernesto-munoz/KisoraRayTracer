import math

from sample.geometry.flip_normals import FlipNormals
from sample.geometry.rect import XYRect, XZRect, YZRect
from sample.material.material import Material
from sample.raytracing.aabb import AABB
from sample.raytracing.hitable import Hitable
from sample.raytracing.hitable_list import HitableList
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3
from sample.raytracing.records import HitRecord
from sample.utils.math_utils import MathUtils


class Box(Hitable):

    def __init__(self, p0: Vector3, p1: Vector3, material: Material):
        """Box with the two extremes defined by {p1} and {p2}"""
        super().__init__()
        self._pmin = p0
        self._pmax = p1
        self._material = material
        self._hitable_list = HitableList(list_of_hitables=[
            XYRect(self._pmin.x(), self._pmax.x(), self._pmin.y(), self._pmax.y(), self._pmax.z(), self._material),
            FlipNormals(XYRect(self._pmin.x(), self._pmax.x(), self._pmin.y(), self._pmax.y(), self._pmin.z(), self._material)),

            XZRect(self._pmin.x(), self._pmax.x(), self._pmin.z(), self._pmax.z(), self._pmax.y(), self._material),
            FlipNormals(XZRect(self._pmin.x(), self._pmax.x(), self._pmin.z(), self._pmax.z(), self._pmin.y(), self._material)),

            YZRect(self._pmin.y(), self._pmax.y(), self._pmin.z(), self._pmax.z(), self._pmax.x(), self._material),
            FlipNormals(YZRect(self._pmin.y(), self._pmax.y(), self._pmin.z(), self._pmax.z(), self._pmin.x(), self._material))
        ])

    def hit(self, ray: Ray, t_min: float, t_max: float) -> (bool, HitRecord):
        """Checks if the ray 'ray' hits with any of the walls between t_min and t_max."""
        return self._hitable_list.hit(ray=ray, t_min=t_min, t_max=t_max)

    def bounding_box(self, t0: float, t1: float) -> AABB:
        """Bounding box made with the bounding box of all the 'Rect' that delimit the box."""
        return self._hitable_list.bounding_box(t0=t0, t1=t1)
