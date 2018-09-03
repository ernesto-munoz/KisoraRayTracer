from PIL import Image

from sample.raytracing.vector3 import Vector3


class ImageData(object):
    """Image Data holder"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._pil_image = Image.new('RGB', (width, height), "black")  # create a new black image

    def set_color(self, row: int, column: int, color: Vector3):
        data = self._pil_image.load()  # create the pixel map
        data[column, self.height - row - 1] = (int(color.r()), int(color.g()), int(color.b()))

    def write_image(self, filename, extension):
        self._pil_image.save(filename, extension)

    def show_image(self):
        self._pil_image.show()