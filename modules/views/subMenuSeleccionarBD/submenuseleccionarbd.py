# Screen principal del menu qeu selecciona el archivo de BD JSON para las 
# geoposiciones. Este screen se enlaza con "FileFilterWidget".
#

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from submenuscreen import *
#class SeleccionarBDScreen(Screen):
class SeleccionarBDScreen(SubMenuScreen):

    def __init__(self,tabbedPanel,**kwargs):
        super(SeleccionarBDScreen,self).__init__(tabbedPanel,**kwargs)


    #TODO: Este metodo tiene que deshabilitar el strip de este submenu, y deshabilitar
    # el resto de los elementos del menu.
    def comenzar_nueva_bd(self):
        print "Comenzando nueva BD, deshabilitando los elementos del menu!\n"
        #self.deshabilitarOpciones()
        #Si se comienza una nueva BDLocal, se crea un nuevo archivo con la fecha actual. 
        controlador = App.get_running_app()
        controlador.inicializarBDLocal()
        archivoBD = controlador.getBDLocalMuestras().getNombreBDLocal()
        controlador.mostrarDialogoMensaje(title = 'Carga de BD Muestras anterior',
                                            text = 'BD de Muestras locales %s \n cargada exitosamente!' % \
                                            archivoBD)
        self.habilitarOpciones()

    def buscar_bd_anterior(self):
        print "Buscando BD anterior, deshabilitando los elementos del menu!\n"
        #self.deshabilitarOpciones()
        self.manager.current = "fileFilter"




