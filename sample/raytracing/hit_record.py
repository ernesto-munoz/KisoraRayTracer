from dataclasses import dataclass

from sample.raytracing.vector3 import Vector3

@dataclass
class HitRecord(object):
    t: float = 0.0
    hit_point: Vector3 = Vector3(0.0, 0.0, 0.0)
    hit_point_normal: Vector3 = Vector3(0.0, 0.0, 0.0)
