from abc import ABC, abstractmethod

from sample.raytracing.aabb import AABB
from sample.raytracing.ray import Ray


class Hitable(ABC):

    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def hit(self, ray:Ray, t_min:float, t_max:float):
        pass

    @abstractmethod
    def bounding_box(self, t0:float, t1:float) -> AABB:
        pass

