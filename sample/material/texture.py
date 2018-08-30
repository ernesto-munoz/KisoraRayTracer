from abc import ABC, abstractmethod

from sample.raytracing.vector3 import Vector3


class Texture(ABC):

    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def value(self, u:float, v:float, p:Vector3):
        """Value of the texture in the coordinates u v.
        """
        pass
