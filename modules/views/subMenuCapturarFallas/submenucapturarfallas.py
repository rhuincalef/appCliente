# Screen principal del menu qeu selecciona el archivo de BD JSON para las 
# geoposiciones. Este screen se enlaza con "FileFilterWidget".
#
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from submenuscreen import *

class CapturarFallasScreen(SubMenuScreen):

    def __init__(self,tabbedPanel,**kwargs):
        super(CapturarFallasScreen,self).__init__(tabbedPanel,**kwargs)

    def capturar_falla_nueva(self):
        controlador = App.get_running_app()
        # Se compueba que exista una BD local seleccionada antes de redirigir a los
        # submenus de captura.
        if not controlador.getBDLocalMuestras().estaInicializada():
            controlador.mostrarDialogoMensaje(title="Captura de falla informada", 
                                text="Debe seleccionar una BD Local para registrar las fallas.\n Ir a submenu 'Seleccion de fallas' y\n seleccionar un archivo de BD para registrar las capturas.")
            return

        print "LLamando al screen de captura de fallas...\n"
        self.deshabilitarOpciones()
        self.manager.current = 'propsFallaConfirmada'
        
    def obtener_fallas_informadas(self):
        print "LLamando al screen de obtener fallas inforamadas...\n"
        self.deshabilitarOpciones()
        self.manager.current = 'obtenerinformadas'

    def capturar_falla_informada(self):
        controlador = App.get_running_app()
        # Se compueba que exista una BD local seleccionada antes de redirigir a los
        # submenus de captura.
        if not controlador.getBDLocalMuestras().estaInicializada():
            controlador.mostrarDialogoMensaje(title="Captura de falla informada", 
                                text="Debe seleccionar una BD Local para registrar las fallas.\n Ir a submenu 'Seleccion de fallas' y\n seleccionar un archivo de BD para registrar las capturas.")
            return

        print "LLamando al screen de capturar falla informada...\n"
        self.deshabilitarOpciones()
        self.manager.current = 'capturarFallaInformada'
        