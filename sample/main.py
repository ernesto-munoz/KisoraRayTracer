from sample.raytracing.camera import Camera
from sample.raytracing.kisora_raytracer import KisoraRayTracer
from sample.raytracing.vector3 import Vector3
from sample.utils.test_scenes import TestScenes

if __name__ == '__main__':
    r = KisoraRayTracer()
    r.width, r.height = KisoraRayTracer.RES_qHD
    r.num_samples = 30
    r.max_workers_pool_process = 4
    r.chunk_width, r.chunk_height = 200, 200

    list_of_hitables, camera = TestScenes.one_sphere_world()
    r.camera = camera

    r.set_objects_in_scene(list_of_hitables=list_of_hitables)
    r.render()
    r.save_image('image_world', 'png')
    # r.save_image('image00', 'jpeg')
    # r.save_image('image00', 'ppm')
    r.show_image()
