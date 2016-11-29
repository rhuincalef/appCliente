# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


import sys,os
# Agrega las vistas al path de Python
def agregar_vistas(listaVistas):
    for vista in listaVistas:
        path_local = '../' + vista
        sys.path.append(os.path.join(os.path.dirname('__file__'), path_local  ))

agregar_vistas(['config',
                'tiposfalla',
                'fallanueva',
                'fallainformada'
                ])

from menutiposfalla import MenuTiposFallaScreen
from kinectviewer import KinectScreen
import importlib
from utilscfg import *



class MenuScreen(Screen):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    def salir(self):
    	App.get_running_app().stop()

    def menu_fallas(self):
        print "screen manager -->"
        print self.manager.screen_names
        self.manager.current = "menutiposfalla"
        print "cambie!"
        print self.manager.current


    # Opcion para subir las fallas capturadas(informadas y nuevas) al servidor
    def menu_subidas_servidor(self):
    	print "Menu subidas"



# NOTA: La clase que hereda de App tiene que tener el mismo nombre que el layout del 
# archivo .kv.
# La clase que hereda de Screen tiene que tener al final la terminacion "Screen".
#
class MenuApp(App):

    def cargar_vistas(self,sm,listaVistas):
        print "En cargar_vistas -->"
        print listaVistas
        print ""
        for kev,tupla in listaVistas.iteritems():
            Builder.load_file(tupla["ruta_kv"])
            print "tupla -->"
            print tupla
            print ""
            MyClass = getattr(importlib.import_module(tupla["modulo"]), 
                                tupla["clase"])
            print ""
            instance = MyClass()
            print "Instancia actual-->"
            print instance.__class__.__name__
            print "---------------------------------------------->"
            print ""
            screen = MyClass(name=tupla["nombre_menu"])
            print "Agregado modulo :"
            print tupla["nombre_menu"]
            sm.add_widget(screen)
            print sm.screen_names

        print "Screens totales -->"
        print sm.screen_names

    def inicializar(self,sm):
        conf = leer_configuracion('../config/confViews.cfg')
        print "Configuracion leida..."
        self.cargar_vistas(sm,conf)
        
    def build(self):
        sm = ScreenManager()
        self.title = "Capturador de fallas"
        self.inicializar(sm)
        sm.current = 'menu'
        return sm

   
if __name__ == '__main__':
    MenuApp().run()



