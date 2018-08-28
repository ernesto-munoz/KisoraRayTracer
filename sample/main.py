import time
import random
random.seed(27)
import math

from sample.raytracing.BVHNode import BVHNode
from sample.raytracing.vector3 import Vector3
from sample.images.ppmimage import PPMImage
from sample.raytracing.hitable_list import HitableList
from sample.geometry.sphere import Sphere
from sample.raytracing.camera import Camera
from sample.material.lambertian import Lambertian
from sample.material.metal import Metal
from sample.material.dielectric import Dielectric
from sample.utils.utils import Utils


def random_in_unit_sphere():
    p = Vector3(1.0, 1.0, 1.0)
    while p.length() >= 1.0:
        p = 2.0 * Vector3(random.random(), random.random(), random.random()) - Vector3(1, 1, 1)

    return p

def color(ray, world, depth):

    has_hit, hit_record = world.hit(ray=ray, t_min=0.001, t_max=float('inf'))

    if has_hit is True:
        scattered, attenuation = hit_record.material.scatter(ray_incident=ray,
                                                             hit_record=hit_record)

        if depth < 50 and scattered is not None:
            return attenuation * color(ray=scattered, world=world, depth=depth+1)
        else:
            return Vector3(0.0, 0.0, 0.0)

    else:
        ray_direction = Vector3.normalize(ray.direction)
        t = 0.5 * (ray_direction.y() + 1.0)
        return (1.0 - t) * Vector3(1.0, 1.0, 1.0) + t * Vector3(0.5, 0.7, 1.0)


if __name__ == '__main__':
    print('Kisora RayTracer')

    start = time.time()
    # width, height, num_samples = 200, 100, 1
    width, height, num_samples = 256, 144, 20
    # width, height, num_samples = 300, 200, 40
    # width, height, num_samples = 854, 480, 50
    # width, height, num_samples = 1280, 720, 50

    image = PPMImage(width, height)

    # world = HitableList(list_of_hitables=random_spheres_scene())
    list_of_hitables = [
        Sphere(center=Vector3(0.0, -100.5, 0.0), radius=100, material=Lambertian(albedo=Vector3(0.8, 0.8, 0.0))),
        Sphere(center=Vector3(0, 0, 2), radius=0.5, material=Lambertian(albedo=Vector3(0.8, 0.8, 0.3)), center_destiny=Vector3(0, 0,2.5 ), time0=0, time1=1),
        Sphere(center=Vector3(1.0, 0.0, 0.0), radius=0.5, material=Lambertian(albedo=Vector3(0.9, 0.3, 0.8))),
        Sphere(center=Vector3(0, 0, 0), radius=0.5, material=Lambertian(albedo=Vector3(0.1, 0.3, 0.8))),
        Sphere(center=Vector3(1, 0, 0), radius=0.5, material=Metal(albedo=Vector3(0.8, 0.6, 0.2), fuzz=0.3)),
        Sphere(center=Vector3(-1, 0, 0), radius=0.5, material=Metal(albedo=Vector3(0.2, 0.8, 0.3), fuzz=1.0)),
        Sphere(center=Vector3(0, 0, 1), radius=0.5, material=Dielectric(refraction_index=1.5))
    ]

    # print('Constructing Hitable List...')
    # list_of_hitables = Utils.random_spheres_scene()
    # world = HitableList(list_of_hitables=list_of_hitables)
    # print('...end')

    print('Constructing BVHNode...')
    list_of_hitables = Utils.random_spheres_scene()
    world = BVHNode(list_of_hitables=list_of_hitables, n=len(list_of_hitables), time0=0.0, time1=1.0)
    # world.print_it()
    print('...end')

    lookfrom = Vector3(4.0, 1.5, 1.2)
    lookat = Vector3(0.0, 0.5, 0.0)
    cam = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                 vfov=40.0, aspect=float(width) / float(height), aperture=0.0, focus_dist=(lookfrom - lookat).length(), t0=0.0, t1=1.0)

    total_pixels = width * height
    current_pixels_count = 0

    for row in range(height - 1, -1, -1):

        for column in range(width):
            final_color = Vector3()
            for s in range(num_samples):
                u = float(column + random.random()) / float(width)
                v = float(row + random.random()) / float(height)

                r = cam.get_ray(u=u, v=v)
                final_color = final_color + color(ray=r, world=world, depth=0)

            final_color = final_color / num_samples

            # for the gamma correction
            final_color = Vector3(math.sqrt(final_color.r()),
                                  math.sqrt(final_color.g()),
                                  math.sqrt(final_color.b()))

            ir = int(255.99 * final_color.r())
            ig = int(255.99 * final_color.g())
            ib = int(255.99 * final_color.b())
            final_color = Vector3(ir, ig, ib)
            image.set_color(row=row, column=column, color=final_color)
            current_pixels_count += 1


        print(f"Completed percentage {(current_pixels_count/total_pixels) * 100:.2f}%: {current_pixels_count} of {total_pixels}")



    end = time.time()
    image.write(f'lots_of_balls_bvh_s{int(end-start)}.ppm')
    print(end - start)