# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')


from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty

#IMports de Kinect
import freenect
from time import sleep
from threading import Thread
from collections import deque
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.graphics import RenderContext, Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


#import the necessary modules
import freenect
import cv2
import numpy as np

from calibkinect import depth2xyzuv
import pcl
import sys,getopt
import re

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label




# Imports necesarios para tratamiento de archivos.
import sys
import os
from string import rfind
import re
import time

from utils import *

from kivy.uix.screenmanager import Screen
from constantes import FALLA_NO_ESTABLECIDA
from kivy.properties import NumericProperty


fragment_header = '''
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

/* custom input */
uniform float depth_range;
uniform vec2 size;
'''

rgb_kinect = fragment_header + '''
void main (void) {
    float value = texture2D(texture0, tex_coord0).r;
    value = mod(value * depth_range, 1.);
    vec3 col = vec3(0., 0., 0.);
    if ( value <= 0.33 )
        col.r = clamp(value, 0., 0.33) * 3.;
    if ( value <= 0.66 )
        col.g = clamp(value - 0.33, 0., 0.33) * 3.;
    col.b = clamp(value - 0.66, 0., 0.33) * 3.;
    gl_FragColor = vec4(col, 1.);
}
'''


depths = None
frames = None
grayscale_frame = None


# Retorna el arreglo de la imagen en RGB
def get_video2():
    array,_ = freenect.sync_get_video()
    return array
        

#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    return array

def showHelp():
    print 'Ayuda: '
    print 'Presione ESC para salir.'
    print 'Presione h para ver ayuda.'
    print 'Presione SPACEBAR para capturar los datos del kinect.'


class KinectDepth(Thread):

    def __init__(self, *largs, **kwargs):
        super(KinectDepth, self).__init__(*largs, **kwargs)
        self.daemon = True
        self.queue = deque()
        self.quit = False
        self.index = 0
        self.depths = None

        
    def run(self):
        q = self.queue
        while not self.quit:
            try:
                self.depths = get_depth()
                frames = get_video2()
                if frames is None:
                    sleep(2)
                    continue
                q.appendleft(frames)
            except TypeError, e:
                print "Error: Problema de conexion con el sensor. Esta conectado?"
                sys.exit(1)


                 
    def pop(self):
        return self.queue.pop()

    def get_depths(self):
        return self.depths


class KinectViewer(Image):

    depth_range = NumericProperty(7.7)

    def __init__(self, **kwargs):
        # add kinect depth provider, and start the thread
        self.kinect = KinectDepth()
        self.kinect.start()
        self.imagen_kv = None

        self.controlador = App.get_running_app()
        
        # parent init
        super(KinectViewer, self).__init__(**kwargs)  
        Clock.schedule_interval(self.actualizar_imagen, 1.0/30.0)


    def establecer_imagen_kv(self,kv):
        self.imagen_kv = kv


    def actualizar_imagen(self, dt):

        try:
            value = self.kinect.pop()
        except:
            return
        
        texture1 = Texture.create(size=(640, 480),
                                    colorfmt='rgb')
        texture1.flip_vertical()
        texture1.blit_buffer(value.tostring(), colorfmt='rgb')
        self.texture = texture1
        

    def getDatosSensor(self):
        xyz, uv = depth2xyzuv(self.kinect.get_depths())
        data = xyz.astype(np.float32)
        return data

        

class KinectScreen(Screen):
    nombre_captura = StringProperty()
    dir_trabajo = StringProperty()
    idFalla = NumericProperty(FALLA_NO_ESTABLECIDA)
    
    def setDatosCaptura(self,nombre_captura,dir_trabajo,id_falla):
        self.nombre_captura = nombre_captura 
        self.dir_trabajo = dir_trabajo
        self.idFalla = id_falla 


    def capturar(self):
        if not conexionSensorEstablecida():
            mostrarDialogo(titulo="Error de conexion con el sensor",
                            content="Debe conectar el sensor antes de\nintentar realizar una captura.")
            return
        data = self.imagen_kv.getDatosSensor()
        controlador = App.get_running_app()
        controlador.capturar(data,self.dir_trabajo,self.nombre_captura,
                                self.idFalla)
