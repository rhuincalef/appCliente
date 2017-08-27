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
import numpy as np

from calibkinect import depth2xyzuv,xyz_complete_matrix
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


from dialogopropscaptura import DialogoPropsCapturaScreen

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

#Agregado para Imagen en Escala de grises
import frame_convert2
import StringIO
from kivy.core.image.img_pygame import ImageLoaderPygame
import pygame
from kivy.properties import ObjectProperty
from kivy.uix.image import Image


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

#Imagen desde memoria con Kivy -->
#https://mornie.org/blog/2013/11/06/how-load-image-memory-kivy/

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


def get_depth2():
    return freenect.sync_get_depth(index=0)


#Usado para la imgen en escala de grises
def get_depthV2():
    #return frame_convert2.pretty_depth(freenect.sync_get_depth()[0])
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def showHelp():
    print 'Ayuda: '
    print 'Presione ESC para salir.'
    print 'Presione h para ver ayuda.'
    print 'Presione SPACEBAR para capturar los datos del kinect.'


class KinectDepth(Thread):

    def __init__(self, *largs, **kwargs):
        super(KinectDepth, self).__init__(*largs, **kwargs)
        self.daemon = True
        #self.queue = deque()
        self.queueVideo = deque()
        self.queueGreyImg = deque()
        self.queueGreyImg2 = deque()
        self.quit = False
        self.index = 0
        self.depths = None
        self.depths2 = None
        #AGREGADO RODRIGO
        self.detenido = False
        self.recibiendoDatos = False # La primera vez que se crea alguna de las texturas 
                                    # este flag se pone en True.Sirve para determinar
                                    # si el sensor esta enviando datos o no.

    def marcarRecepcionDatos(self):
        if not self.recibiendoDatos:
            self.recibiendoDatos = True

    def detener(self):
        self.detenido = True
        
    def run(self):
        self.detenido = False
        qVideo = self.queueVideo
        qGreyImg = self.queueGreyImg
        qGreyImg2 = self.queueGreyImg2
        while not self.quit:
            try:
                #Si no estoy detenido comienzo la recoleccion de datos
                if self.detenido:
                    print "Se detuvo el KinectDepth thread!\n"
                    break

                self.depths = get_depth()
                self.depths2 = get_depth2()
                frames = get_video2()
                if frames is None or self.depths is None:
                    print "Esperando data...\n"
                    sleep(2)
                    continue

                qVideo.appendleft(frames)
                qGreyImg.appendleft(self.depths)
                qGreyImg2.appendleft(self.depths2)
                self.marcarRecepcionDatos()
                #print "Appendeando data a las colecciones!\n"

            except TypeError, e:
                print "Excepcion typeError en thread KinectDepth!!!\n"
                print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                print "%s" % e
                print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                print "Error: Problema de conexion con el sensor. Esta conectado?"
                sys.exit(1)
            except Exception, e:
                print "Excepcion desconocida en thread KinectDepth!!!\n"
                print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                print "%s" % e
                print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"



                 
    def popVideo(self):
        return self.queueVideo.pop()


    def popGreyImg(self):
        return self.queueGreyImg.pop()


    def popGreyImg2(self):
        return self.queueGreyImg2.pop()

    def vaciar(self):
        self.queueVideo = deque()
        self.queueGreyImg = deque()
        self.queueGreyImg2 = deque()
        print "Se vaciaron todas las colas!!!\n"

    def get_depths(self):
        return self.depths

    def hayFrames(self):
        print "len(self.queueVideo) = %s\n" % len(self.queueVideo)
        return len(self.queueVideo)>0





import pypcd
import struct
class KinectViewer(Image):

    depth_range = NumericProperty(7.7)

    def __init__(self,**kwargs):
        self.kinect = None
        self.controlador = App.get_running_app()
        
        # parent init
        super(KinectViewer, self).__init__(**kwargs)  
        #Clock.schedule_interval(self.actualizar_imagen, 1.0/30.0)
        print "El tamanio de la ventana es: %s,%s \n" % (Window.size[0],Window.size[1])
    

    def iniciarSensado(self,depthThread):
        from kivy.core.window import Window
        self.kinect = depthThread
        Clock.schedule_interval(self.actualizar_imagen, 1.0/30.0)
        print "Planificado el inicioSensado RGB! \n"

    #AGREGADO RODRIGO
    #KinectViewer.detenerSensado()
    def detenerSensado(self):
        Clock.unschedule(self.actualizar_imagen)
        print "Desplanificada RGB IMG!\n"


    def actualizar_imagen(self, dt):
        #print "\n--------------------------------------------\n\n"
        #print "En KinectViewer.actualizar_imagen() !\n"
        try:
            value = self.kinect.popVideo()
        except Exception as e:
            return

        texture1 = Texture.create(size=(640, 480),
                                    colorfmt='rgb')
        texture1.flip_vertical()
        texture1.blit_buffer(value.tostring(), colorfmt='rgb')
        self.texture = texture1
        #print "Creada textura: %s\n" % self.texture
        #print "\n--------------------------------------------\n\n"
    

    # Prepara los datos del sensor, empaquetando el rgb del video al formato de PCL
    # con las coordenadas,obtenidas de la profundidad .
    # 
    def getDatosSensor(self,formato=PCD_XYZ_RGB_FORMAT):
        print "En getDatosSensor()...\n"
        if formato == PCD_XYZ_RGB_FORMAT:
            rgbConCod = list()
            self.kinect.hayFrames()
            rgbSinCod = get_video2()
            print "rgbSinCod.shape: (%s,%s)\n" % (rgbSinCod.shape[0],rgbSinCod.shape[1]) 
            print "rgbSinCod.size: %s\n" % rgbSinCod.size
            for x in xrange(0,len(rgbSinCod)):
                filaRgbEmpaquetado = pypcd.encode_rgb_for_pcl(rgbSinCod[x])
                rgbConCod.append(filaRgbEmpaquetado)
            npRgbConCod = np.asarray(rgbConCod,dtype=np.float32)

            depth = self.kinect.get_depths()
            #Se extraen todas las coordenadsa con todas las coordenadas en eje Z
            xyzCoords = xyz_complete_matrix(depth)
            npXyzCoords = np.asarray(xyzCoords,dtype=np.float32)

            #Se une el rgb empaquetado con cada coordenada x,y,z
            dataNube = np.empty((480*640,4),dtype=np.float32)
            rgbAplanado = npRgbConCod.flatten()
            for index in xrange(0,len(rgbAplanado)-1):
                dataNube[index,:] = np.append(npXyzCoords[index],rgbAplanado[index])

            print "LLENADA dataNube! tipo: %s \n" % dataNube.dtype

            #Se elmina el elemento Z (indice 2) que es menor a cero(Incluido en la funcion
            #original depth2xyzuv que hace el filtrado de los elementos que estan detras de la camara). 
            dataNube2 = np.asarray([x for x in dataNube if x[2]<0 ],dtype=np.float32)
            return dataNube2
        else:
            xyz, uv = depth2xyzuv(self.kinect.get_depths())
            data = xyz.astype(np.float32)
            return data

        
import numpy as np
import io
from io import BytesIO
from PIL import Image as PILImage
from numpy import random
from kivy.graphics.texture import Texture




from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import InvertEffect,HorizontalBlurEffect

from kivy.properties import NumericProperty, StringProperty
from kivy.graphics import RenderContext, Color, Rectangle

from kivy.uix.boxlayout import BoxLayout
from time import sleep

from kivy.core.window import Window



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

hsv_func = '''
vec3 HSVtoRGB(vec3 color) {
    float f,p,q,t, hueRound;
    int hueIndex;
    float hue, saturation, v;
    vec3 result;

    /* just for clarity */
    hue = color.r;
    saturation = color.g;
    v = color.b;

    hueRound = floor(hue * 6.0);
    hueIndex = mod(int(hueRound), 6.);
    f = (hue * 6.0) - hueRound;
    p = v * (1.0 - saturation);
    q = v * (1.0 - f*saturation);
    t = v * (1.0 - (1.0 - f)*saturation);

    switch(hueIndex) {
        case 0:
            result = vec3(v,t,p);
        break;
        case 1:
            result = vec3(q,v,p);
        break;
        case 2:
            result = vec3(p,v,t);
        break;
        case 3:
            result = vec3(p,q,v);
        break;
        case 4:
            result = vec3(t,p,v);
        break;
        case 5:
            result = vec3(v,p,q);
        break;
    }
    return result;
}
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

points_kinect = fragment_header + hsv_func + '''
void main (void) {
    // threshold used to reduce the depth (better result)
    const int th = 5;

    // size of a square
    int square = floor(depth_range);

    // number of square on the display
    vec2 count = size / square;

    // current position of the square
    vec2 pos = floor(tex_coord0.xy * count) / count;

    // texture step to pass to another square
    vec2 step = 1 / count;

    // texture step to pass to another pixel
    vec2 pxstep = 1 / size;

    // center of the square
    vec2 center = pos + step / 2.;

    // calculate average of every pixels in the square
    float s = 0, x, y;
    for (x = 0; x < square; x++) {
        for (y = 0; y < square; y++) {
            s += texture2D(texture0, pos + pxstep * vec2(x,y)).r;
        }
    }
    float v = s / (square * square);

    // threshold the value
    float dr = th / 10.;
    v = min(v, dr) / dr;

    // calculate the distance between the center of the square and current
    // pixel; display the pixel only if the distance is inside the circle
    float vdist = length(abs(tex_coord0 - center) * size / square);
    float value = 1 - v;
    if ( vdist < value ) {
        vec3 col = HSVtoRGB(vec3(value, 1., 1.));
        gl_FragColor = vec4(col, 1);
    }
}
'''
hsv_kinect = fragment_header + hsv_func + '''
void main (void) {
    float value = texture2D(texture0, tex_coord0).r;
    value = mod(value * depth_range, 1.);
    vec3 col = HSVtoRGB(vec3(value, 1., 1.));
    gl_FragColor = vec4(col, 1.);
}
'''

class KinectViewerGreyScale(Image):

    depth_range = NumericProperty(7.7)

    #shader = StringProperty("rgb")
    shader = StringProperty("points")

    index = NumericProperty(0)

    def __init__(self, **kwargs):
        print "Creando kinectViewer greyscale...\n"
        self.kinect = None
        self.imagen_kv = None
        self.controlador = App.get_running_app()
        
        # parent init
        super(KinectViewerGreyScale, self).__init__(**kwargs)  
        print "Llamada a la superclase de kinectViewer greyscale OK!...\n"

        self.canvas = None
        self.canvas = RenderContext()
        #self.canvas.shader.fs = hsv_kinect
        self.canvas.shader.fs = rgb_kinect
        # allocate texture for pushing depth
        self.texture = Texture.create(
            size=(640, 480), colorfmt='luminance', bufferfmt='ushort')
        self.texture.flip_vertical()
        print "Creada kinectViewer greyscale!\n"



    def on_index(self, instance, value):
        self.kinect.index = value

    def on_shader(self, instance, value):
        if value == 'rgb':
            self.canvas.shader.fs = rgb_kinect
        elif value == 'hsv':
            self.canvas.shader.fs = hsv_kinect
        elif value == 'points':
            self.canvas.shader.fs = points_kinect


    def iniciarSensado(self,depthThread):
        from kivy.core.window import Window
        self.kinect = depthThread
        Clock.schedule_interval(self.actualizar_imagen, 0)


    #AGREGADO RODRIGO
    #KinectViewerGreyScale.detenerSensado()
    def detenerSensado(self):
        Clock.unschedule(self.actualizar_imagen)
        print "Desplanificada GREY IMG!\n"

    def actualizar_imagen(self, dt):
        try:
            value = self.kinect.popGreyImg()
        except:
            return
        # update projection mat and uvsize
        self.canvas['projection_mat'] = Window.render_context['projection_mat']
        self.canvas['depth_range'] = self.depth_range
        self.canvas['size'] = list(map(float, self.size))
        try:
            value = self.kinect.popGreyImg2()
        except:
            return

        f = value[0].astype('ushort') * 32
        self.texture.blit_buffer(
            f.tostring(), colorfmt='luminance', bufferfmt='ushort')
        self.canvas.ask_update()
        

from kivy.logger import LoggerHistory

import signal, os
import time


from screenredimensionable import ScreenRedimensionable

class KinectScreen(ScreenRedimensionable):
    
    nombre_captura = StringProperty()

    def __init__(self,**kwargs):
        print "En KinectScreen!!"
        self.depthThread = KinectDepth()
        self.depthThread.start()
        print "Inicializado el depthThread!\n"
        super(KinectScreen, self).__init__(**kwargs)
        self.inicializar_imagenes_kinect(self.depthThread)
        self._keyboard = Window.request_keyboard(None,self)
        print "Obtenido teclado...\n"
        self.dir_trabajo = "."
        

    #AGREGADO RODRIGO
    # Obtiene una referencia al thread que interactua con el sensor para obtener
    # los datos.
    #def getThreadCapturaSensor(self):
    #    return self.depthThread

    #AGREGADO RODRIGO
    def recibiendoDatosKinect(self):
        return self.depthThread.recibiendoDatos    


    def on_pre_enter(self):
        controlador = App.get_running_app()
        listo = controlador.conexionSensorEstablecida()
        print "Sensor LISTO? : %s...\n" % listo
        if listo:
            print "Bindeado SPACEBAR!!\n"
            self._keyboard.bind(on_key_down=self.tecla_presionada)
            self._iniciarMonitorDatosKinect()
        else:
            controlador = App.get_running_app()
            popup = controlador.mostrarDialogoMensaje(title='Error de conexion',
                                                text='No se pueden realizar capturas hasta que\n el sensor se encuentre conectado.\nConecte el sensor y reinicie la aplicacion.')
            popup.bind(on_dismiss=self.cancelarCaptura)


    # Establece una alarma para monitorear si se estan alamcenando frames
    # en el thread que mantiene el sensor en ejecucion.Si no es asi,
    # se muestra un dialog informando al usuario que debe reiniciar la app.
    def _iniciarMonitorDatosKinect(self):
        signal.signal(signal.SIGALRM,self._handlerTimeout)
        signal.alarm(TIMEOUT_KINECT_SEG)
        

    def _handlerTimeout(self,signum, frame):
        #raise ExcepcionTimeout("Error al abrir el dispositivo.\n Dispositivo ocupado\n")
        print 'Llamando al manejador!\n'
        if not self.depthThread.recibiendoDatos:
            signal.alarm(0) # Disable the alarm
            controlador = App.get_running_app()
            msg = "No se estan detectando datos enviados del sensor.\n Reinicie la aplicacion con el sensor conectado e intentelo de nuevo.\n"
            popup = controlador.mostrarDialogoMensaje(title='Error de streaming',
                                    text=msg)
            popup.bind(on_dismiss=self._terminarCaptura)
     
    def _terminarCaptura(self,instance):
        self.volver()

    def cancelarCaptura(self,instance):
        print "Deteniendo la app...\n"
        controlador = App.get_running_app()
        controlador.stop()
        self.volver()

    
    def on_leave(self):
        print "DesBindeada SPACEBAR!!\n"
        self._keyboard.unbind(on_key_down=self.tecla_presionada)

    

    #Metodo que inicializa las imagenes para visualizar en Kinect.
    def inicializar_imagenes_kinect(self,depthThread):
        print "En inicializar_imagenes_kinect() ...\n"
        self.kinect_rgb.iniciarSensado(depthThread)
        self.kinect_grey.iniciarSensado(depthThread)


    def detener_imagenes_kinect(self):
        print "Deteniendo imagenes_kinect!!\n"
        self.kinect_rgb.detenerSensado()
        self.kinect_grey.detenerSensado()



    def tecla_presionada(self,keyboard,keycode,text,modifiers):
        print "keycode[0] : %s" % keycode[0]
        print "keycode[1] : %s" % keycode[1]
        if keycode[0] == 32:
            print "Presione SPACE!!!!\n"
            self.capturar()
            return True
        return False

    #def setDatosCaptura(self,nombre_captura,dir_trabajo,id_falla):
    def setDatosCaptura(self,nombre_captura,dir_trabajo):
        self.nombre_captura = nombre_captura 
        self.dir_trabajo = dir_trabajo


    def capturar(self):
        controlador = App.get_running_app()
        print "En Kinectviewer.capturar()...con idFalla %s\n" % controlador.getData("idFalla") 
        if not controlador.conexionSensorEstablecida():
            controlador.mostrarDialogoMensaje(text= "Debe conectar el sensor antes de\nintentar realizar una captura.",
                                        title = "Error de conexion con el sensor")
            return
        
        data = self.kinect_rgb.getDatosSensor()

        controlador = App.get_running_app()
        print "El dir_trabajo para guardar la falla es: %s" % self.dir_trabajo
        controlador.capturar(data,self.dir_trabajo,self.nombre_captura,
                               controlador.getData("idFalla") )
        
    #Actualiza el screen que tiene el listado de capturas
    def actualizar_vista_archivos(self,nombre_screen):
        #Se instancia de vuelta el dialogopropscaptura
        my_screen = None
        for s in self.manager.screens:
            if s.name == nombre_screen:
                my_screen= s
                print "Screen encontrada y removida!"
                break
        self.manager.remove_widget(my_screen)
        screen = DialogoPropsCapturaScreen(name="dialogopropscaptura")
        self.manager.add_widget(screen)
        print "SCreen agregada al mananger"

    def volver(self):
        self.actualizar_vista_archivos('dialogopropscaptura')
        print "Las screens actuales de screenmanager luego de switch_to son: "
        print self.manager.screen_names
        self.manager.current = 'dialogopropscaptura'

