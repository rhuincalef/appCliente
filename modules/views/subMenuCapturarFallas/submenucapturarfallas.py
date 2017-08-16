# Screen principal del menu qeu selecciona el archivo de BD JSON para las 
# geoposiciones. Este screen se enlaza con "FileFilterWidget".
#
from kivy.uix.screenmanager import ScreenManager, Screen
from submenuscreen import *
#class CapturarFallasScreen(Screen):
class CapturarFallasScreen(SubMenuScreen):

    def __init__(self,tabbedPanel,**kwargs):
        super(CapturarFallasScreen,self).__init__(tabbedPanel,**kwargs)

    def capturar_falla_nueva(self):
        print "LLamando al screen de captura de fallas...\n"
        self.deshabilitarOpciones()
        #self.manager.current = "seleccionarTipoFalla"
        self.manager.current = 'propsFallaConfirmada'

    def obtener_fallas_informadas(self):
        print "LLamando al screen de obtener fallas inforamadas...\n"
        self.deshabilitarOpciones()
        #self.manager.current = "filtradoDirecciones"
        self.manager.current = 'obtenerinformadas'

    def capturar_falla_informada(self):
        print "LLamando al screen de capturar falla informada...\n"
        self.deshabilitarOpciones()
        self.manager.current = 'capturarFallaInformada'
