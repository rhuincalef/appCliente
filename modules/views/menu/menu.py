# # -*- coding: utf-8 -*-
# import kivy
# kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

import loadsavedialog
from loadsavedialog import *
from kivy.uix.popup import Popup

from utils import mostrarDialogo
import os


class ArchivoExisteExcepcion(Exception):
    pass

class MenuScreen(Screen):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self._popup = None
        



    def salir(self):
    	App.get_running_app().stop()

    def menu_fallas(self):
        print "screen manager -->"
        print self.manager.screen_names
        self.manager.current = "menutiposfalla"
        print "cambie!"
        print self.manager.current


    def guardar_fallas_json(self):
        print "Cargado dialogo guardado de fallas"
        content = SaveDialog(save=self.guardar, cancel=self.dismiss_popup)
        if type(content) is None:
            print "Content es None!!!!!\n"
        else:
            print "Content NO es None!!!!!\n"
        # content = Label(text= "HOLA MUNDODOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDDDDD")
        self._popup = Popup(title="Guardar fallas capturadas", content=content)
        self._popup.open()
        

    def cargar_fallas_json(self):
        print "Cargado dialogo carga de fallas"        
        content = LoadDialog(load=self.cargar, cancel=self.dismiss_popup)
        self._popup = Popup(title="Cargar fallas capturadas", content=content)
        # self._popup = Popup(title="Cargar fallas capturadas", content=content,
        #                 size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        print "Cerrando dialog..."
        self._popup.dismiss()

    # Carga los capturadores con las fallas leidas de disco.
    def cargar(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as stream:
                # self.text_input.text = stream.read()
                controlador = App.get_running_app()
                controlador.leerFallas(stream)
        except IOError, e:
            mostrarDialogo(titulo="Error al leer el archivo de  fallas de disco",
                content=e.message)
        except Exception, e:
            mostrarDialogo(titulo="Error en el proceso de lectura de fallas",
                content=e.message)

        self.dismiss_popup()

    #Guarda serializa las capturas en un json y lo guarda a disco
    def guardar(self, path, filename):
        try:
            full_path = path + filename
            if os.path.isfile(full_path):
                raise ArchivoExisteExcepcion("El archivo que desea guardar ya existe!")

            with open(os.path.join(path, filename), 'w') as stream:
                # stream.write(self.text_input.text)
                controlador = App.get_running_app()
                controlador.guardarFallas(stream)
        except IOError, e:
            mostrarDialogo(titulo="Error al guardar el archivo de fallas en disco",
                content=e.message)

        except ArchivoExisteExcepcion, e:
            mostrarDialogo(titulo="Error archivo de capturas existente",
                content=e.message)
        except Exception, e:
            mostrarDialogo(titulo="Error en el proceso de guardado de fallas",
                content=e.message)

        self.dismiss_popup()


    # Opcion para subir las fallas capturadas(informadas y nuevas) al servidor
    def menu_subidas_servidor(self):
    	print "Menu subidas"
        self.manager.current = "subircapturasservidor"



# NOTA: La clase que hereda de App tiene que tener el mismo nombre que el layout del 
# archivo .kv.
# La clase que hereda de Screen tiene que tener al final la terminacion "Screen" y si
# existen .kv asociados, se deben agregar 
#
# class MenuApp(App):

#     def cargar_vistas(self,sm,listaVistas):
#         for kev,tupla in listaVistas.iteritems():
#             Builder.load_file(tupla["ruta_kv"])
#             MyClass = getattr(importlib.import_module(tupla["modulo"]), 
#                                 tupla["clase"])
#             instance = MyClass()
#             screen = MyClass(name=tupla["nombre_menu"])
#             sm.add_widget(screen)

#     def inicializar(self,sm):
#         conf = leer_configuracion('../config/confViews.cfg')
#         print "Configuracion leida..."
#         self.cargar_vistas(sm,conf)
        
#     def build(self):
#         sm = ScreenManager()
#         self.title = "Capturador de fallas"
#         self.inicializar(sm)
#         sm.current = 'menu'
#         return sm

   
# if __name__ == '__main__':
#     MenuApp().run()



