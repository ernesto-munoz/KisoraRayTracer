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

    # @staticmethod
    # def bsic_scene():
    #     list_of_hitables = [
    #         Sphere(center=Vector3(0.0, -100.5, 0.0), radius=100,
    #                material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=colors_texture)),
    #         Sphere(center=Vector3(0, 0, 2), radius=0.5, material=Lambertian(albedo=Vector3(0.8, 0.8, 0.3)),
    #                center_destiny=Vector3(0, 0, 2.5), time0=0, time1=1),
    #         Sphere(center=Vector3(1.0, 0.0, 0.0), radius=0.5, material=Lambertian(albedo=Vector3(0.9, 0.3, 0.8))),
    #         Sphere(center=Vector3(0, 0, 0), radius=0.5, material=Lambertian(albedo=Vector3(0.1, 0.3, 0.8))),
    #         Sphere(center=Vector3(1, 0, 0), radius=0.5, material=Metal(albedo=Vector3(0.8, 0.6, 0.2), fuzz=0.3)),
    #         Sphere(center=Vector3(-1, 0, 0), radius=0.5, material=Metal(albedo=Vector3(0.2, 0.8, 0.3), fuzz=1.0)),
    #         Sphere(center=Vector3(0, 0, 1), radius=0.5, material=Dielectric(refraction_index=1.5))
    #     ]
    #     return list_of_hitables