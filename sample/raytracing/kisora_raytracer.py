import math
import enum
import random
import logging
import concurrent.futures

from sample.decorators.decorators import timer
from sample.images.image_data import ImageData
from sample.raytracing.BVHNode import BVHNode
from sample.raytracing.ray import Ray
from sample.raytracing.vector3 import Vector3


class KisoraRayTracer:
    # TODO: Manage general data about the scene form a centric place. (width, height, samples, etc)
    # TODO: Associate a camera to a scene
    # TODO: Rewrite the parallelization code and time measurement code.
    # TODO: Create a benchmark scene to test the improvement of the following changes. (Cornel Box)
    # TODO: Use Numpy to manage lists of numbers
    # TODO: When Numpy is used: Implement translation, rotation and scale in geometry.
    # TODO: Use Pillow and numpy to manage the Image information and save it to disk.
    # TODO: (Maybe) Reestructure the Hitable(Renderable) herarchy tree.
    # TODO: Image Textures and Noise Textures
    # TODO: The diffuse light extreme value may be not working.
    # TODO: The Volume Rendering is making strange shapes, test it more.

    # Image resolutions
    P144 = (256, 144)
    P240 = (426, 240)
    qHD = (960, 540)
    HD = (1280, 720)
    FHD = (1920, 1080)
    QHD = (2560, 1440)
    UHD4k = (3840, 2160)
    FULL4K = (4096, 2304)

    def __init__(self):
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Welcome to Kisora Ray Tracer')
        logging.info('Initializing...')
        random.seed(27)

        # Render
        self.width, self.height = self.HD  # render resolution
        self.num_samples = 500  # samples per pixel

        # Concurrency
        self.max_workers_pool_process = 4  # max number of processes
        self.chunk_width, self.chunk_height = 50, 50  # render size for each process

        # Scene
        self._scene_objects_list = list()  # empty list of objects
        self._bvh_world = None  # no world
        self._camera = None  # no camera
        self._image_data = None # no image data

    # Properties
    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    # Scene
    @timer
    def set_objects_in_scene(self, list_of_hitables:list):
        logging.info(f'Constructing the BVH Structure for {len(list_of_hitables)} objects.')
        self._scene_objects_list = list_of_hitables
        self._bvh_world = BVHNode(list_of_hitables=self._scene_objects_list,
                              n=len(self._scene_objects_list), time0=0.0, time1=1.0)

    # Render
    def _initialize_render(self):
        """Make render initialization """
        self._image_data = ImageData(width=self.width, height=self.height)

        if self._camera is None:
            raise ValueError(f'No camera has been set.')

        logging.info(f'Rendering an image of {self.width} {self.height} with {self.num_samples} samples per pixel.')
        logging.info(f'NUmber of objects in the scene: {len(self._scene_objects_list)}')

    @timer
    def render(self):
        # Make the initilization of the render before the real render
        self._initialize_render()


        with concurrent.futures.ProcessPoolExecutor(self.max_workers_pool_process) as executor:
            futures = list()

            for row in range(self.height - 1, -1, -self.chunk_height):
                for column in range(0, self.width, self.chunk_width):
                    h = row + 1 if row - self.chunk_height < 0 else self.chunk_height
                    w = self.width - column if column + self.chunk_width > self.width else self.chunk_width

                    futures.append(executor.submit(self._render_patch, row, column, w, h))

            for x in concurrent.futures.as_completed(futures):
                list_of_tuples = x.result()
                for t in list_of_tuples:
                    self._image_data.set_color(row=t[0], column=t[1], color=t[2])

    @timer
    def _render_patch(self, begin_row, begin_column, patch_width, patch_height):
        """Render a patch of the image defined by {row} {column} with {width} and {heidht}"""
        logging.info(f'Beginning patch ({begin_row} {begin_column}) with width {patch_width} and height {patch_height}')
        #start = time.time()

        result = list()
        for row in range(begin_row, begin_row - patch_height, -1):
            for column in range(begin_column, begin_column + patch_width):
                final_color = Vector3()
                for s in range(self.num_samples):
                    u = float(column + random.random()) / float(self.width)
                    v = float(row + random.random()) / float(self.height)

                    r = self.camera.get_ray(u=u, v=v)
                    final_color = final_color + self.calculate_ray_color(ray=r, depth=0)

                final_color = final_color / self.num_samples

                # for the gamma correction
                final_color = Vector3(math.sqrt(final_color.r()),
                                      math.sqrt(final_color.g()),
                                      math.sqrt(final_color.b()))

                # print(final_color)
                ir = int(255.99 * final_color.r())
                ig = int(255.99 * final_color.g())
                ib = int(255.99 * final_color.b())
                final_color = Vector3(ir, ig, ib)
                result.append((row, column, final_color))

        #end = time.time()
        logging.info(f'Ending patch ({begin_row} {begin_column}) with width {patch_width} and height {patch_height}')
        return result

    def calculate_ray_color(self, ray:Ray, depth:float):
        has_hit, hit_record = self._bvh_world.hit(ray=ray, t_min=0.001, t_max=float('inf'))

        if has_hit is True:
            scattered, attenuation = hit_record.material.scatter(ray_incident=ray,
                                                                 hit_record=hit_record)

            emitted = hit_record.material.emitted(u=hit_record.u, v=hit_record.v, p=hit_record.hit_point)
            if depth < 50 and scattered is not None:
                return emitted + attenuation * self.calculate_ray_color(ray=scattered, depth=depth + 1)
            else:
                return emitted

        else:
            # Ambient Color
            # return Vector3(0.0, 0.0, 0.0)
            ray_direction = Vector3.normalize(ray.direction)
            t = 0.5 * (ray_direction.y() + 1.0)
            return (1.0 - t) * Vector3(0.3, 0.3, 0.3) + t * Vector3(0.5, 0.7, 1.0)

    # Utilities
    def save_image(self, filepath):
        self._image_data.write_as_ppm(filepath=filepath)