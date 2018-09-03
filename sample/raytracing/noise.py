import math
import random

from sample.raytracing.vector3 import Vector3


class Perlin:

    def __init__(self):
        self._ranvector = self.perlin_generate()
        self._perm_x, self._perm_y, self._perm_z = self.perlin_generate_perm(), self.perlin_generate_perm(), self.perlin_generate_perm()

    def noise(self, p: Vector3):
        u = p.x() - math.floor(p.x())
        v = p.y() - math.floor(p.y())
        w = p.z() - math.floor(p.z())
        i = math.floor(p.x())
        j = math.floor(p.y())
        k = math.floor(p.z())

        # return self._ranvector[self._perm_x[i] ^ self._perm_y[j] ^ self._perm_z[k]]
        # c = [[[self._ranfloat[self._perm_x[(i + ii) & 255] ^ self._perm_y[(j + jj) & 255] ^ self._perm_z[(k + kk) & 255]] for kk in range(2)] for jj in range(2)] for ii in range(2)]
        c = list()
        for ii in range(2):
            for jj in range(2):
                for kk in range(2):
                    c.append(self._ranvector[self._perm_x[(i + ii) & 255] ^ self._perm_y[(j + jj) & 255] ^ self._perm_z[(k + kk) & 255]])

        return self.trilineart_interp(c, u, v, w)

    def turb(self, p: Vector3, depth: int=7):
        accum = 0
        temp_p = p
        weight = 1.0
        for i in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2

        return math.fabs(accum)

    def perlin_generate(self):
        p = list()
        for i in range(256):
            p.append(Vector3.normalize(Vector3(-1 + 2 * random.random(), -1 + 2 * random.random(), -1 + 2 * random.random())))
        return p

    def permute(self, l):
        for i in range(len(l) - 1, -1, -1):
            target = int(random.random() * (i + 1))
            l[i], l[target] = l[target], l[i]

    def perlin_generate_perm(self):
        p = list(range(256))
        self.permute(p)
        return p

    def trilineart_interp(self, c, u, v, w):
        uu = u * u * (3 - 2 * u)
        vv = v * v * (3 - 2 * v)
        ww = w * w * (3 - 2 * w)

        accum = 0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = Vector3(u - i, v - j, w - k)
                    accum += (i * uu + (1 - i) * (1 - uu)) * \
                             (j * vv + (1 - j) * (1 - vv)) * \
                             (k * ww + (1 - k) * (1 - ww)) * Vector3.dot(c[i * 2 + j * 2 + k], weight_v)
        return accum