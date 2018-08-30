import os
import random

from sample.geometry.box import Box
from sample.geometry.flip_normals import FlipNormals
from sample.geometry.sphere import Sphere
from sample.geometry.rect import XYRect, XZRect, YZRect
from sample.geometry.volumes import ConstantVolume
from sample.material.checker_texture import CheckerTexture
from sample.material.constant_texture import ConstantTexture
from sample.material.dielectric import Dielectric
from sample.material.diffuse_light import DiffuseLight
from sample.material.image_texture import ImageTexture
from sample.material.lambertian import Lambertian
from sample.material.metal import Metal
from sample.raytracing.vector3 import Vector3


class TestScenes:

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

    @staticmethod
    def first_light_scene():
        list_of_hitables = [
            Sphere(center=Vector3(0.0, -1000, 0.0), radius=1000, material=Lambertian(albedo=Vector3(0.9, 0.67, 0.25))),
            Sphere(center=Vector3(0.0, 2, 0.0), radius=2, material=Lambertian(albedo=Vector3(0.7, 0.8, 0.1))),
            Sphere(center=Vector3(0.0, 7, 0.0), radius=2, material=DiffuseLight(albedo=Vector3(1.0, 1.0, 1.0), texture=ConstantTexture(color=Vector3(4,4,4)))),
            XYRect(3, 5, 1, 3, -2, DiffuseLight(albedo=Vector3(1.0, 1.0, 1.0), texture=ConstantTexture(color=Vector3(1, 1, 1))))
        ]

        return list_of_hitables

    @staticmethod
    def one_sphere():
        checker_texture = CheckerTexture(texture0=ConstantTexture(Vector3(0.2, 0.3, 0.1)), texture1=ConstantTexture(Vector3(0.9, 0.9, 0.9)))

        script_dir = os.path.dirname(__file__)
        texture_filepath = os.path.join(script_dir, r'../resources/textures/tiled-background-with-stripes-and-splatter_256x256.jpg')
        colors_texture = ImageTexture(texture_file_path=texture_filepath)

        list_of_hitables = [
            Sphere(center=Vector3(0.0, -100.5, 0.0), radius=100,
                   material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=checker_texture)),
            Sphere(center=Vector3(0, 1, 0), radius=1.0, material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=colors_texture)),
        ]
        return list_of_hitables

    @staticmethod
    def cornell_box():

        red_mat = Lambertian(albedo=Vector3(0.65, 0.05, 0.05))
        white_mat = Lambertian(albedo=Vector3(0.73, 0.73, 0.73))
        green_mat = Lambertian(albedo=Vector3(0.12, 0.45, 0.15))
        light = DiffuseLight(albedo=Vector3(1.0, 1.0, 1.0), texture=ConstantTexture(color=Vector3(1, 1, 1)))

        box01 = Box(p0=Vector3(130, 0, 65), p1=Vector3(295, 165, 230), material=white_mat)
        box02 = Box(p0=Vector3(265, 0, 295), p1=Vector3(430, 330, 460), material=white_mat)

        list_of_hitables = [
            FlipNormals(YZRect(0, 555, 0, 555, 555, green_mat)),
            YZRect(0, 555, 0, 555, 0, red_mat),
            XZRect(113, 443, 127, 432, 554, light),
            FlipNormals(XZRect(0, 555, 0, 555, 555, white_mat)),
            XZRect(0, 555, 0, 555, 0, white_mat),
            FlipNormals(XYRect(0, 555, 0, 555, 555, white_mat)),
            ConstantVolume(boundary=box01, density=0.01, texture=ConstantTexture(Vector3(0.95, 0.95, 0.95))),
            ConstantVolume(boundary=box02, density=0.01, texture=ConstantTexture(Vector3(0.05, 0.05, 0.05)))
        ]

        return list_of_hitables
