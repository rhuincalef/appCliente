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

agregar_vistas(['tiposfalla','fallanueva'])

from menutiposfalla import MenuTiposFallaScreen
from kinectviewer import KinectScreen
import importlib

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

    def menu_subidas_servidor(self):
    	print "Menu subidas"



# NOTA: La clase que hereda de App tiene que tener el mismo nombre que el layout del 
# archivo .kv.
# La clase que hereda de Screen tiene que tener al final la terminacion "Screen".
#
class MenuApp(App):

    def cargar_vistas(self,sm,listaVistas):
        for kev,tupla in listaVistas.iteritems():
            Builder.load_file(tupla["ruta_kv"])
            print "tupla -->"
            print tupla
            print ""
            MyClass = getattr(importlib.import_module(tupla["modulo"]), 
                                tupla["clase"])
            instance = MyClass()
            screen = MyClass(name=tupla["nombre_menu"])
            sm.add_widget(screen)

        # Builder.load_file("menuscreen.kv")
        # screen = MenuScreen(name='menu')
        # sm.add_widget(screen)
        # Builder.load_file("../TiposFalla/menutiposfallascreen.kv")
        # screen = MenuTiposFallaScreen(name='menutiposfalla')
        # sm.add_widget(screen)
        # Builder.load_file("../kinectView/kinectscreen.kv")
        # screen = KinectScreen(name='capturaKinect')
        # sm.add_widget(screen)

    def inicializar(self,sm):
        conf = {
                0:{
                    "nombre_menu": "menu" ,
                    "ruta_kv": "menuscreen.kv",
                    "modulo": "menu",
                    "clase": "MenuScreen"
                },
                1:{
                    "nombre_menu": "menutiposfalla" ,
                    "ruta_kv": "../tiposfalla/menutiposfallascreen.kv",
                    "modulo": "menutiposfalla",
                    "clase": "MenuTiposFallaScreen"

                },
                2:{
                    "nombre_menu": "capturaKinect" ,
                    "ruta_kv": "../fallanueva/kinectscreen.kv",
                    "modulo": "kinectviewer",
                    "clase": "KinectScreen"
                },
                3:{
                    "nombre_menu": "fallainformada" ,
                    "ruta_kv": "../fallainformada/kinectscreen.kv",
                    "modulo": "kinectviewer",
                    "clase": "KinectScreen"
                }
        }
        self.cargar_vistas(sm,conf)
        


    def build(self):
        sm = ScreenManager()
        self.title = "Capturador de fallas"
        self.inicializar(sm)
        sm.current = 'menu'
        return sm

   
if __name__ == '__main__':
    MenuApp().run()



