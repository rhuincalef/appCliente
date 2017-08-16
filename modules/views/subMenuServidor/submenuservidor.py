# Screen principal del menu qeu selecciona el archivo de BD JSON para las 
# geoposiciones. Este screen se enlaza con "FileFilterWidget".
#
from kivy.uix.screenmanager import ScreenManager, Screen
from submenuscreen import *

class ServidorScreen(SubMenuScreen):

    def __init__(self,tabbedPanel,**kwargs):
        super(ServidorScreen,self).__init__(tabbedPanel,**kwargs)

    def subir_fallas(self):
        print "LLamando al screen de SUBIR FALLAS...\n"
        self.deshabilitarOpciones()
        self.manager.current = "subircapturasservidor"
