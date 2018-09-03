import math


class Vector3(object):
    _x = 0.0
    _y = 0.0
    _z = 0.0

    def __init__(self, x:float=0.0, y:float=0.0, z:float=0.0):
        self._x, self._y, self._z = x, y, z

    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z

    def r(self):
        return self._x

    def g(self):
        return self._y

    def b(self):
        return self._z

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self._x + other.x(), y=self._y + other.y(), z=self._z + other.z())
        else:
            return Vector3(x=self._x + other, y=self._y + other, z=self._z + other)

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self._x - other.x(), y=self._y - other.y(), z=self._z - other.z())
        else:
            return Vector3(x=self._x - other, y=self._y - other, z=self._z - other)

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self._x * other.x(), y=self._y * other.y(), z=self._z * other.z())
        else:
            return Vector3(x=self._x * other, y=self._y * other, z=self._z * other)

    def __rmul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self._x * other.x(), y=self._y * other.y(), z=self._z * other.z())
        else:
            return Vector3(x=self._x * other, y=self._y * other, z=self._z * other)

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self._x / other.x(), y=self._y / other.y(), z=self._z / other.z())
        else:
            return Vector3(x=self._x / other, y=self._y / other, z=self._z / other)

    def __iadd__(self, other):
        self._x += other.x()
        self._y += other.y()
        self._z += other.z()
        return self

    def __isub__(self, other):
        self._x -= other.x()
        self._y -= other.y()
        self._z -= other.z()
        return self

    def __imul__(self, other):
        if isinstance(other, Vector3):
            self._x *= other.x()
            self._y *= other.y()
            self._z *= other.z()
        else:
            self._x *= other
            self._y *= other
            self._z *= other
        return self

    def __itruediv__(self, other):
        if isinstance(other, Vector3):
            self._x /= other.x()
            self._y /= other.y()
            self._z /= other.z()
        else:
            self._x /= other
            self._y /= other
            self._z /= other
        return self

    def __neg__(self):
        return Vector3(x=-self._x, y=-self._y, z=-self._z)

    def __str__(self):
        return f'({self._x} {self._y} {self._z})'

    def length(self):
        return math.sqrt(self._x * self._x + self._y * self._y + self._z * self._z)

    def squared_length(self):
        return self._x * self._x + self._y * self._y + self._z * self._z

    def make_unit_vector(self):
        k = 1.0 / self.length()
        self._x *= k
        self._y *= k
        self._z *= k

    @staticmethod
    def dot(v1, v2):
        return v1.x() * v2.x() + v1.y() * v2.y() + v1.z() * v2.z()

    @staticmethod
    def cross(v1, v2):
        return Vector3(
            x=v1.y() * v2.z() - v1.z() * v2.y(),
            y=-(v1.x() * v2.z() - v1.z() * v2.x()),
            z=v1.x() * v2.y() - v1.y() * v2.x()
        )

    @staticmethod
    def normalize(v):
        if v.length() == 0:
            raise ValueError('Can\'t normalize a vector with length zero: {}'.format(v))
        return v / v.length()

    @staticmethod
    def reflect(v, n):
        return v - 2 * Vector3.dot(v, n) * n

    @staticmethod
    def refract(incident: 'Vector3', normal: 'Vector3', n1: 'float', n2: 'float'):
        """Calculate the refracted vector from the vector v in the surface with normal n
        """

        n = n1 / n2
        cosI = -Vector3.dot(normal,incident)
        sinT2 = n * n * (1.0 - cosI * cosI)
        if sinT2 > 1.0:
            return None

        cosT = math.sqrt(1.0 - sinT2)
        return n * incident + (n * cosI - cosT) * normal


