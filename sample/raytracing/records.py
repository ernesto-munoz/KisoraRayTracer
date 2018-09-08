from dataclasses import dataclass

from sample.material.material import Material
from sample.raytracing.vector3 import Vector3

@dataclass
class HitRecord(object):
    t: float = 0.0
    hit_point: Vector3 = Vector3(0.0, 0.0, 0.0)
    hit_point_normal: Vector3 = Vector3(0.0, 0.0, 0.0)
    u: float = 0.0
    v: float = 0.0
    material:Material = None
