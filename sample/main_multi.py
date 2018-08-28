import time
import random
random.seed(27)
import math
import threading
import concurrent.futures

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

def calculate_image_chunk(total_width, total_height, init_row, init_column, chunk_height, chunk_width, world, cam, num_samples):
    # print(f'IN:From ({init_row}, {init_column}) to ({init_row - chunk_height}, {init_column + chunk_width}) with H:{chunk_height} and W:{chunk_width}')
    print(f'Beginning thread: ({init_row}, {init_column})')
    start = time.time()

    result = list()
    for row in range(init_row, init_row - chunk_height, -1):
        for column in range(init_column, init_column + chunk_width):
            final_color = Vector3()
            for s in range(num_samples):
                u = float(column + random.random()) / float(total_width)
                v = float(row + random.random()) / float(total_height)

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
            # image.set_color(row=row, column=column, color=final_color)
            result.append((row, column, final_color))

    end = time.time()
    print(f'Ending thread: ({init_row}, {init_column}): {end - start}')
    return result

if __name__ == '__main__':
    print('Kisora RayTracer')

    start = time.time()
    max_workers = 5
    chunk_width, chunk_height = 50, 50

    # width, height, num_samples = 100, 50, 10
    width, height, num_samples = 256, 144, 20
    # width, height, num_samples = 300, 200, 40
    # width, height, num_samples = 854, 480, 50
    # width, height, num_samples = 1280, 720, 50

    image = PPMImage(width, height)

    print('Constructing BVH...')
    list_of_hitables = Utils.random_spheres_scene()
    world = BVHNode(list_of_hitables=list_of_hitables, n=len(list_of_hitables), time0=0.0, time1=1.0)
    # world.print_it()
    print('...end')

    lookfrom = Vector3(4.0, 1.5, 1.2)
    lookat = Vector3(0.0, 0.5, 0.0)
    cam = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                 vfov=40.0, aspect=float(width) / float(height), aperture=0.0, focus_dist=(lookfrom - lookat).length(),
                 t0=0.0, t1=1.0)

    total_pixels = width * height
    current_pixels_count = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers) as executor:
        futures = list()

        for row in range(height - 1, -1, -chunk_height):
            for column in range(0, width, chunk_width):
                h = row + 1 if row - chunk_height < 0 else chunk_height
                w = width - column if column + chunk_width > width else chunk_width

                futures.append(executor.submit(calculate_image_chunk, width, height, row, column, h, w, world, cam, num_samples))

        for x in concurrent.futures.as_completed(futures):
            list_of_tuples = x.result()
            for t in list_of_tuples:
                image.set_color(row=t[0], column=t[1], color=t[2])

    end = time.time()
    image.write(f'lots_of_balls_bvh_concurrent{max_workers}_s{int(end - start)}.ppm')
    print(end - start)