from sample.raytracing.vector3 import Vector3


class ImageData(object):
    """Image Data holder"""
    width = None
    height = None
    color_matrix = None

    def __init__(self, width, height, color_matrix=None):
        self.width = width
        self.height = height
        if color_matrix is None:
            self.color_matrix = list()
            for row in range(self.height):
                self.color_matrix.append([Vector3(0.0, 0.0, 0.0)] * self.width)
        else:
            self.color_matrix = color_matrix

    def set_color_matrix(self, width, height, color_matrix):
        self.width = width
        self.height = height
        self.color_matrix = color_matrix

    def set_color(self, row, column, color):
        self.color_matrix[row][column] = color

    def write_as_ppm(self, filepath):
        with open(filepath, 'w') as f:
            f.write('P3\n{} {}\n255\n'.format(self.width, self.height))
            for row in range(self.height - 1, -1, -1):
                for column in range(self.width):
                    color = self.color_matrix[row][column]
                    f.write('{} {} {}\n'.format(int(color.r()), int(color.g()), int(color.b())))