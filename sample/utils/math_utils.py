import math
import random
from sample.raytracing.vector3 import Vector3


class MathUtils:

    @staticmethod
    def clamp(value, small, big):
        return max(small, min(value, big))

    @staticmethod
    def random_in_unit_sphere():
        p = Vector3(1.0, 1.0, 1.0)
        while p.length() >= 1.0:
            p = 2.0 * Vector3(random.random(), random.random(), random.random()) - Vector3(1, 1, 1)

        return p

    @staticmethod
    def random_cosine_direct():
        r1, r2 = random.random(), random.random()
        z = math.sqrt(1 - r2)
        phi = 2 * math.pi * r1
        x = math.cos(phi) * 2 * math.sqrt(r2)
        y = math.sin(phi) * 2 * math.sqrt(r2)
        return Vector3(x, y, z)
