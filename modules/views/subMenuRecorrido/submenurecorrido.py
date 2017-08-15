# Screen principal del menu qeu selecciona el archivo de BD JSON para las 
# geoposiciones. Este screen se enlaza con "FileFilterWidget".
#
from kivy.uix.screenmanager import ScreenManager, Screen
from submenuscreen import *
#class RecorridoScreen(Screen):
class RecorridoScreen(SubMenuScreen):

    def __init__(self,tabbedPanel,**kwargs):
        super(RecorridoScreen,self).__init__(tabbedPanel,**kwargs)


    #TODO: Este metodo tiene que deshabilitar el strip de este submenu, y deshabilitar
    # el resto de los elementos del menu.
    def guardar_recorrido(self):
        print "LLamando al screen de guardar recorrido...\n"
        self.deshabilitarOpciones()
        #TODO: AGREGAR CODIGO ACA!


    #TODO: Este metodo tiene que deshabilitar el strip de este submenu, y deshabilitar
    # el resto de los elementos del menu.
    def cargar_recorrido(self):
        print "LLamando al screen de cargar recorrido...\n"
        self.deshabilitarOpciones()
        #TODO: AGREGAR CODIGO ACA!


