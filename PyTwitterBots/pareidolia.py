__author__ = 'supergork'

from PIL import Image
from PIL import ImageFilter

import random
import os.path
from face_detect import face_detect
import numpy
import copy

class Pareidolia():

    def __init__(self):
        self.size_x = 1024
        self.size_y = 512
        self.im = Image.new("RGB", (1024, 512), "white")
        self.region = (0, 0, 1024, 512) #x, y, w, h
        self.scale_factor = 1.1
        self.min_neighbors = 3

    def rand_gray(self):
        value = random.randint(0, 255)
        random.choice((0, 0, 0, 0, 255, 255))
        return (value, value, value)

    def rand_color(self):
        value = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return value

    def create_face_image(self):
        iterations = 0
        last_faces = 0
        while True:
            size = (self.region[2]*self.region[3])
            adjustments = size/10
            old_image = self.im.copy()
            for i in range(0, adjustments):
                pos = (random.randint(self.region[0], self.region[0] + self.region[2]/2 - 1), random.randint(self.region[1], self.region[1]+self.region[3]-1))
                possym = (self.region[0] + self.region[2] - (pos[0] - self.region[0]) - 1, pos[1])

                col = self.rand_gray()
                self.im.putpixel(pos, col)
                self.im.putpixel(possym, col)
            filter = random.choice((ImageFilter.GaussianBlur(radius=1), ImageFilter.CONTOUR, ImageFilter.FIND_EDGES, ImageFilter.DETAIL))
            self.im = self.im.filter(filter)
            imcv = numpy.asarray(self.im)[:,:,::-1].copy()
            faces = face_detect.find_faces(imcv, self.scale_factor, self.min_neighbors)
            if len(faces) >= 1:
                face_region = faces[0]
                print 'region = ' + str(self.region)
                crop_region = (face_region[0], face_region[1], face_region[0] + face_region[2], face_region[1] + face_region[3] )
                print 'crop_region = ' + str(crop_region)
                face = self.im.crop(crop_region)
                face.load()
                face.save(os.path.join('images', 'out' + str(iterations) + '.jpg'))

            iterations += 1
            if iterations % 1000 == 0:
                iterations = 0

            print "Iterations = " + str(iterations);


if __name__ == '__main__':
    p = Pareidolia()
    p.create_face_image()