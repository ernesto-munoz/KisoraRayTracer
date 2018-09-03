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
from sample.material.noise_texture import NoiseTexture
from sample.raytracing.camera import Camera
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
    def one_sphere_world():
        lookfrom = Vector3(12, 5, 3)
        lookat = Vector3(0, 2, -1)
        camera = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                        vfov=20.0, aspect=16 / 9, aperture=0.0,
                        focus_dist=10.0, t0=0.0, t1=1.0)

        checker_texture = CheckerTexture(texture0=ConstantTexture(Vector3(0.2, 0.3, 0.1)), texture1=ConstantTexture(Vector3(0.9, 0.9, 0.9)))

        script_dir = os.path.dirname(__file__)
        texture_filepath = os.path.join(script_dir, r'../resources/textures/google-maps.jpg')
        world_texture = ImageTexture(texture_file_path=texture_filepath, uoffset=0.1)
        texture_filepath = os.path.join(script_dir, r'../resources/textures/tiled-background-with-stripes-and-splatter_256x256.jpg')
        colors_texture = ImageTexture(texture_file_path=texture_filepath)

        list_of_hitables = [
            # Sphere(center=Vector3(0.0, -1000, 0.0), radius=1000,
            #        material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=colors_texture)),
            XZRect(-20, 20, -20, 20, 0, material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=colors_texture)),
            Sphere(center=Vector3(0, 2, 0), radius=2.0, material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=world_texture)),
            Sphere(center=Vector3(0, 1.0, -3), radius=1.0,material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=checker_texture))
        ]
        return list_of_hitables, camera

    @staticmethod
    def one_sphere_noise() -> (list, Camera):
        lookfrom = Vector3(13, 2, 3)
        lookat = Vector3(0, 0, 0)
        camera = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                        vfov=20.0, aspect=16 / 9, aperture=0.0,
                        focus_dist=10.0, t0=0.0, t1=1.0)

        pertext = NoiseTexture(scale=1.0)

        list_of_hitables = [
            Sphere(Vector3(0, -1000, 0), 1000, Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=pertext)),
            Sphere(Vector3(0, 2, 0), 2, Lambertian(albedo=Vector3(1.0, 1.0, 1.0), texture=pertext))
        ]

        return list_of_hitables, camera

    @staticmethod
    def cornell_box():

        red_mat = Lambertian(albedo=Vector3(0.65, 0.05, 0.05))
        white_mat = Lambertian(albedo=Vector3(0.73, 0.73, 0.73))
        green_mat = Lambertian(albedo=Vector3(0.12, 0.45, 0.15))
        light = DiffuseLight(albedo=Vector3(1.0, 1.0, 1.0), texture=ConstantTexture(color=Vector3(4, 4, 4)))

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

        lookfrom = Vector3(278, 278, -800)
        lookat = Vector3(278, 278, 0.0)
        camera = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                        vfov=40.0, aspect=16/9, aperture=0.0,
                        focus_dist=(lookfrom - lookat).length(),
                        t0=0.0, t1=1.0)

        return list_of_hitables, camera

    @staticmethod
    def the_next_week_final():
        white_mat = Lambertian(albedo=Vector3(0.73, 0.73, 0.73))
        ground_mat = Lambertian(albedo=Vector3(0.48, 0.83, 0.53))
        light = DiffuseLight(albedo=Vector3(1.0, 1.0, 1.0), texture=ConstantTexture(color=Vector3(1,1,1)))

        lookfrom = Vector3(0, 150, -500)
        lookat = Vector3(200, 150, 0)
        camera = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                        vfov=60.0, aspect=16 / 9, aperture=0.0,
                        focus_dist=(lookfrom - lookat).length(),
                        t0=0.0, t1=1.0)

        list_of_hitables = list()

        for i in range(20):
            for j in range(20):
                w = 100
                x0 = -1000 + i * w
                z0 = -1000 + j * w
                y0 = 0
                x1 = x0 + w
                y1 = 100 * (random.random() + 0.01)
                z1 = z0 + w
                print(Vector3(x0, y0, z0))
                print(Vector3(x1, y1, z1))
                list_of_hitables.append(
                    Box(Vector3(x0, y0, z0), Vector3(x1, y1, z1), ground_mat)
                )

        list_of_hitables.append(
            YZRect(123, 423, 147, 412, 554, light)
        )

        list_of_hitables.append(
            Sphere(center=Vector3(400, 400, 200), radius=50,
                   material=Lambertian(albedo=Vector3(1.0, 1.0, 1.0),
                                       texture=ConstantTexture(color=Vector3(0.7, 0.3, 0.1))
                                       ),
                   center_destiny=Vector3(430, 400, 200), time0=0, time1=1)
        )
        list_of_hitables.append(
            Sphere(center=Vector3(260, 150, 45), radius=50,
                   material=Dielectric(refraction_index=1.5))
        )
        list_of_hitables.append(
            Sphere(center=Vector3(0, 150, 145), radius=50,
                   material=Metal(albedo=Vector3(0.8, 0.8, 0.9), fuzz=10.0))
        )
        boundary01 = Sphere(center=Vector3(360, 150, 145), radius=70, material=Dielectric(refraction_index=1.5))
        list_of_hitables.append(
            ConstantVolume(boundary=boundary01, density=0.2, texture=ConstantTexture(Vector3(0.2, 0.4, 0.9)))
        )
        boundary02 = Sphere(center=Vector3(0, 0, 0), radius=5000, material=Dielectric(refraction_index=1.5))
        list_of_hitables.append(
            ConstantVolume(boundary=boundary02, density=0.0001, texture=ConstantTexture(Vector3(1.0, 1.0, 1.0)))
        )

        return list_of_hitables, camera























