import random

from sample.geometry.sphere import Sphere
from sample.material.dielectric import Dielectric
from sample.material.lambertian import Lambertian
from sample.material.metal import Metal
from sample.raytracing.vector3 import Vector3


class Utils:

    @staticmethod
    def random_spheres_scene():
        world = list()
        world.append(
            Sphere(Vector3(0, -1000, 0), 1000, Lambertian(Vector3(0.5, 0.5)))
        )
        for a in range(-11, 11):
            for b in range(-11, 11):
                center = Vector3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())
                if (center - Vector3(1, 0.2, 0)).length() > 0.9:
                    choose_mat = random.random()
                    if choose_mat < 0.8:
                        world.append(
                            Sphere(center, 0.2, Lambertian(
                                Vector3(random.random() * random.random(), random.random() * random.random(),
                                        random.random() * random.random())))
                        )
                    elif choose_mat < 0.95:
                        world.append(
                            Sphere(center, 0.2, Metal(Vector3(0.5 * (1 + random.random()), 0.5 * (1 + random.random()),
                                                              0.5 * (1 + random.random())), 0.5 * random.random())
                                   )
                        )
                    else:
                        world.append(
                            Sphere(center, 0.2, Dielectric(1.5))
                        )
        world.append(
            Sphere(Vector3(0, 1, 0), 1.0, Dielectric(1.5))
        )
        world.append(
            Sphere(Vector3(-4, 1, 0), 1.0, Lambertian(Vector3(0.4, 0.2, 0.1)))
        )
        world.append(
            Sphere(Vector3(4, 1, 0), 1.0, Metal(Vector3(0.7, 0.6, 0.5), 0.0))
        )
        return world