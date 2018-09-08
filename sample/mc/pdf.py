import math
import random

from abc import ABC, abstractmethod

# from sample.raytracing.hitable_list import HitableList
from sample.raytracing.vector3 import Vector3
from sample.utils.math_utils import MathUtils
from sample.mc.onb import ONB


class PDF(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def value(self, direction: Vector3) -> float:
        pass

    @abstractmethod
    def generate(self) -> Vector3:
        pass


class CosinePDF(PDF):

    _uvw: ONB

    def __init__(self, w: Vector3):
        super().__init__()
        self._uvw = ONB()
        self._uvw.build_from_w(w)

    def value(self, direction: Vector3) -> float:
        cosine = Vector3.dot(Vector3.normalize(direction), self._uvw.w())
        if cosine > 0:
            return cosine / math.pi
        else:
            return 0

    def generate(self) -> Vector3:
        return self._uvw.local(MathUtils.random_cosine_direct())


class HitablePDF(PDF):

    def __init__(self, p, origin: Vector3):
        super().__init__()
        self._hitables = p
        self._origin = origin

    def value(self, direction: Vector3) -> float:
        return self._hitables.pdf_value(self._origin, direction)

    def generate(self) -> Vector3:
        return self._hitables.random(self._origin)


class MixturePDF(PDF):

    _pdf0: PDF
    _pdf1: PDF

    def __init__(self, p0: PDF, p1: PDF):
        super().__init__()
        self._pdf0 = p0
        self._pdf1 = p1

    def value(self, direction: Vector3) -> float:
        return 0.5 * self._pdf0.value(direction=direction) + 0.5 * self._pdf1.value(direction=direction)

    def generate(self) -> Vector3:
        if random.random() < 0.5:
            return self._pdf0.generate()
        else:
            return self._pdf1.generate()
