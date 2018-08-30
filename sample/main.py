from sample.raytracing.camera import Camera
from sample.raytracing.kisora_raytracer import KisoraRayTracer
from sample.raytracing.vector3 import Vector3
from sample.utils.test_scenes import TestScenes

if __name__ == '__main__':
    r = KisoraRayTracer()
    r.width, r.height = KisoraRayTracer.P144
    r.num_samples = 5

    lookfrom = Vector3(278, 278, -800)
    lookat = Vector3(278, 278, 0.0)
    r.camera = Camera(lookfrom=lookfrom, lookat=lookat, vectorup=Vector3(0.0, 1.0, 0.0),
                 vfov=40.0, aspect=float(r.width) / float(r.height), aperture=0.0,
                 focus_dist=(lookfrom - lookat).length(),
                 t0=0.0, t1=1.0)

    r.set_objects_in_scene(list_of_hitables=TestScenes.cornell_box())
    r.render()
    r.save_image('image00.ppm')
