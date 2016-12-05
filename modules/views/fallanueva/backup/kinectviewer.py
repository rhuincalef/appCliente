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
#import cv2.cv as cv
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



from kivy.uix.screenmanager import Screen


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

# Variables globales respecto del almacenamiento de los
# archivos en disco.
# NOTA: Estas variables seran enviadas por la vista que
# genere una instancia de controller

nombre_archivo = "archivoSalida"
extension_archivo = ".pcd"
subfijo = "_"
dir_trabajo_prueba = "/home/rodrigo/TESINA-2016-KINECT/aplicacionCliente/modules/views/kinectView"
        

# Retorna el arreglo de la imagen en RGB
def get_video2():
    array,_ = freenect.sync_get_video()
    return array
        

#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    return array



# Retorna la cantidad de archivos que tienen un nombre dado
# en el directorio de trabajo especificado. Se detecta la
# extension desde la derecha del archivo.
def get_cantidad_archivos(archivo_a_buscar,dirTrabajo):
    cantActual = 0
    # time.sleep (2)
    patron = nombre_archivo + "[0-9]" + "\\" + extension_archivo
    print "El patron es: ", patron
    expr = re.compile(patron)
    
    #Obtiene una lista de nombres de archivos ordenada
    listado = sorted(os.listdir(dirTrabajo))

    print "listado -->"
    print listado
    print ""
    for file in listado:
        # if file.endswith(".pcd"):
        res = expr.search(file)
        print "examinando ",file
        if res != None:
            print "Archivo encontrado!"    
            #Si es un .pcd se
            index_extension = rfind(file,".pcd")
            cad_archivo = file[:index_extension]
            print "cad_archivo encontrado es: ",cad_archivo
            print "archivo_a_buscar encontrado es: ",archivo_a_buscar+ str(cantActual)
            if (archivo_a_buscar+ str(cantActual)) == cad_archivo:
                cantActual += 1
    print "Cantidad de archivos .pcd con el nombre ",archivo_a_buscar, "es : ",cantActual
    print ""
    #Se retorna el siguiente
    return cantActual



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
        

    def realizar_captura(self):
        print "capture!!"
        print "depths es -->"
        print self.kinect.get_depths()
        print "----------------------------------------------"
        print ""
        xyz, uv = depth2xyzuv(self.kinect.get_depths())
        data = xyz.astype(np.float32)
        self.capturar(data)


    # TODO: Llamar al capturador para almacenar los datos actuales
    # captados por el sensor.
    def capturar(self,data):
        print data
        p = pcl.PointCloud(data)
        # Se obtiene la cantidad de archivos con un nombre dentro
        # en un dir. de prueba dado
        try:
            cant_archivos_actuales = get_cantidad_archivos(nombre_archivo,
                                                            dir_trabajo_prueba)
            archivo_salida = nombre_archivo + str(cant_archivos_actuales) \
                                + extension_archivo
            pcl.save(p, archivo_salida)
            print "Archivo "+ archivo_salida +" guardado!"
            print ""
        except OSError as e:
            print "Error al listar archivos en directorio ",dir_trabajo_prueba
            sys.exit(1)
            

class KinectScreen(Screen):
    pass


# class ControllerApp(App):

#     def build(self):
#         self.title = "Captura de fallas"
#         return Controller(logo_path='mylogo.jpg', width_img = 640,
#                             height_img = 480) 
# if __name__ == '__main__':
#     ControllerApp().run()