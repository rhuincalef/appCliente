#!/usr/bin/env python
# encoding: utf-8

# kivy_memory_image.py
# How to load an image from memory in Kivy
# http://mornie.org/blog/2013/11/06/how-load-image-memory-kivy/

#https://gist.github.com/eriol/d6ea5c5036373199b934
#http://stackoverflow.com/questions/10762454/load-image-from-memory-in-kivy



#CREANDO IMAGEN DESDE NUMPYARRAY -->
#http://stackoverflow.com/questions/6915106/saving-a-numpy-array-as-an-image-instructions

#import Image
#import numpy as np
#data = np.random.random((100,100))
#Rescale to 0-255 and convert to uint8
#rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)
#im = Image.fromarray(rescaled)
#im.save('test.png')



# Copyright (c) 2013, Daniele Tricoli 
# All rights reserved.
#
# License: BSD-3

import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np

from kivy.app import App
from kivy.core.image.img_pygame import ImageLoaderPygame
from kivy.properties import ObjectProperty
from kivy.uix.image import Image


def cardioid(start, stop, step):
    """A rotated cardioid."""
    theta = np.arange(start, stop, step)
    r = 1 - np.sin(theta)
    return theta, r


def polar_plot(theta, r, rmax):
    """Draw a polat plot.

    :returns: matplotlib.Figure
    """
    fig = Figure(facecolor='white')
    ax = fig.add_subplot(111, polar=True, frameon=False)
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.plot(theta, r, color='g', linewidth=2)
    ax.set_rmax(rmax)
    return fig


def fig2png(fig):
    """Convert a matplotlib.Figure to PNG image.

    :returns: PNG image bytes
    """
    data = StringIO.StringIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(data)
    return data.getvalue()


class MemoryImage(Image):
    """Display an image already loaded in memory."""
    memory_data = ObjectProperty(None)

    def __init__(self, memory_data, **kwargs):
        self.memory_data = memory_data
        super(MemoryImage, self).__init__(**kwargs)
        self.on_memory_data()


    def on_memory_data(self, *args):
        print "EJECUTADO on_memory_data()!!!..\n"
        """Load image from memory."""
        data = StringIO.StringIO()
        data.write(self.memory_data)
        print "type(data): %s\n" % type(data)
        print "type(data.getvalue()): %s\n" % type(data.getvalue())
        print "data.getvalue() tiene:\n %s\n +++++++++++++++++++++++++++++++++\n" % data.getvalue()
        with self.canvas:
            print "TIPO de ImageLoaderPygame %s" % type(data.getvalue())
            self.texture = ImageLoaderPygame(data.getvalue()).texture


class TestApp(App):

    def build(self):
        print "self.options: %s" % self.options['image'] 
        #return MemoryImage(self.options['image'])
        return MemoryImage(self.options['image'])

if __name__ == '__main__':
    theta, r = cardioid(0, 8.0, 0.01)
    image = fig2png(polar_plot(theta, r, 2.5))
    TestApp(image=image).run()
    #TestApp(image="mario.png").run()


#Guardar en un buffer un numpy array como imagen.
#http://stackoverflow.com/questions/646286/python-pil-how-to-write-png-image-to-string
#http://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image


#https://www.daniweb.com/programming/software-development/code/493004/display-an-image-from-the-web-pygame


from PIL import Image
import numpy as np
import io
from numpy import random

#w, h = 512, 512
#data = np.zeros((h, w, 3), dtype=np.uint8)
#data = np.ones((h, w, 3), dtype=np.uint8)

#w, h = 512, 512
#data = random.random((w,h))

data = 255 * np.random.random_sample((480,640))


#data[256, 256] = [255, 0, 0]
#numpy_bytes = data.tobytes()
img = Image.fromarray(data, 'RGB')
#Modo 'L' de escala de grises 
img.mode = 'L'


output = io.BytesIO()
output.write(img.tobytes())
format = 'PNG' # or 'JPEG' or whatever you want
#img.save(output, format)
img.save("mi-png", format)

#output = io.StringIO()
#output = io.BytesIO()
#output.write(img)
#img.save(output, format)
#output.seek(0)
#contents = output.getvalue()

#image_file = io.BytesIO(img.tobytes())
#image_file.seek(0)


#image_file = io.BytesIO(numpy_bytes)
#ImageLoaderPygame("ms",inline=True,rawdata=image_file)

textura = ImageLoaderPygame("mi-png").texture


#Codigo para generar la textura de Kivy v1 FUNCUIONANDO!!
#from kivy.core.window import Window
#import io
#from kivy.core.image import Image as CoreImage
#data = io.BytesIO(open("mi-png.png", "rb").read())
#im = CoreImage(data, ext="png")
#im.texture


#Codigo para generar la textura de Kivy v2 DESDE CACHE!
from kivy.core.window import Window
import io
from kivy.core.image import Image as CoreImage
import numpy as np
from numpy import random
from kivy.graphics.texture import Texture

data = 255 * np.random.random_sample((480,640))
numpy_bytes = data.tobytes()
stream = io.BytesIO()
stream.write(numpy_bytes)
stream.seek(0)

tex = Texture.create(size=(480,640), colorfmt='luminance')
tex.blit_buffer(stream.getvalue(), colorfmt='luminance', bufferfmt='ubyte')











