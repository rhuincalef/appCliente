# -*- coding: utf-8 -*-

# Screen principal del menu qeu selecciona el archivo de BD JSON para las 
# geoposiciones. Este screen se enlaza con "FileFilterWidget".
#
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


#Imports y layouts para el popup de carga de elementos 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

#import loadsavedialog
#from loadsavedialog import *
from kivy.uix.popup import Popup

import os
from os import path
from os.path import expanduser
from file import XFileOpen, XFileSave

from submenuscreen import *
from capturador import ExcepcionRecorridoVacio
from constantes import EXTENSION_RECORRIDO_DEFAULT,ESTILO_BACKGROUND_MODAL_XBASE,COLOR_SEPARADOR_POPUPS

import re

class RecorridoScreen(SubMenuScreen):

    def __init__(self,tabbedPanel,**kwargs):
        super(RecorridoScreen,self).__init__(tabbedPanel,**kwargs)
        self._popup = None


    def guardar_recorrido(self):
        print "LLamando al screen de guardar recorrido...\n"
        #self.deshabilitarOpciones()
        self.guardarRecorrido()

    def cargar_recorrido(self):
        print "LLamando al screen de cargar recorrido...\n"
        #self.deshabilitarOpciones()
        self.cargarRecorrido()




    def guardarRecorrido(self):
        print "Cargado dialogo guardado de fallas...\n"
        controlador = App.get_running_app()
        if not controlador.existenFallasCargadas():
            controlador.mostrarDialogoMensaje( title= "Guardado de recorrido",
                                        text="No existen fallas cargadas en memoria!")
            return
        else:
            XFileSave(on_dismiss=self._fileSaveCallback,
                        title = "Guardar recorrido con fallas",
                        #path=expanduser(u'~'))
                        path=os.getcwd(),
                        background = ESTILO_BACKGROUND_MODAL_XBASE,
                        separator_color = COLOR_SEPARADOR_POPUPS
                        )
        


    def contieneExtensionPorDefecto(self,nameBD):
        patron = ".*\%s$" % EXTENSION_RECORRIDO_DEFAULT
        regex = re.compile(patron)
        if regex.match(nameBD) is not None:
            return True
        return False
    

    def _fileSaveCallback(self, instance):
        if instance.is_canceled():
            return

        #Retorna el path completo a la BD
        nameBD = instance.get_full_name()
        if not self.contieneExtensionPorDefecto(nameBD):
            nameBD = instance.get_full_name() + EXTENSION_RECORRIDO_DEFAULT
            
        print "nameBD final: %s\n" % nameBD
        if path.isfile(nameBD):
            controlador = App.get_running_app()
            print "tipo filename: %s; filename: %s\n" % (type(instance.filename),
                                                        instance.filename)
            msg = "¿Desea sobreescribir el archivo %s?" % str(instance.filename)
            controlador.mostrarDialogoConfirmacion( title = "Sobreescritura de fallas",
                                        content = msg,
                                        callback = self._callbackDialogoSobreescribir,
                                        args = [ nameBD ] )
        else:
            self._crearArchivoRecorrido(nameBD)            

    def _callbackDialogoSobreescribir(self,instance):
        print "LLamada _callbackDialogoSobreescribir() con %s\n" % instance.args[0]
        if not instance.is_confirmed():
            return
        self._crearArchivoRecorrido(instance.args[0])


    def _crearArchivoRecorrido(self,nameBD):
        controlador = App.get_running_app()
        print "nameBD ingresado es: %s\n" % nameBD
        controlador.persistirFallas(nameBD)
        print "Persistidas las fallas!\n"


    #Carga los objetos itemFalla en su respectivo capturador
    def cargarRecorrido(self):
        print "Cargado dialogo carga de fallas\n"        
        XFileOpen(on_dismiss=self._callbackCargarRecorrido,
                    title = "Cargar recorrido en memoria",
                    #path=expanduser(u'~'),
                    path=os.getcwd(),
                    multiselect=False,
                    background = ESTILO_BACKGROUND_MODAL_XBASE,
                    separator_color = COLOR_SEPARADOR_POPUPS
                    )


    def _callbackCargarRecorrido(self,instance):
        if instance.is_canceled():
            print "Cancelo la carga del recorrido en memoria!\n"
            return
        msg = title = ""
        controlador = App.get_running_app()
        try:
            archivo = instance.selection[0]
            print "Cargando recorrido en archivo: %s\n" % archivo 
            controlador.cargarRecorrido(archivo)
            title = "Carga de recorrido"
            msg = "Se cargo correctamente el archivo con las capturas"
        except ExcepcionRecorridoVacio as e:
            title = "Carga de recorrido"
            msg = "No existen fallas registradas en el archivo cargado"
        except Exception as e:
            title = "Error en carga de fallas"
            msg = "Error cargando BD con itemfallas.\n(%s)" % e
        finally:
            print "%s\n" % msg
            controlador.mostrarDialogoMensaje(title = title,
                                        text = msg)


    def dismiss_popup(self):
        print "Cerrando dialog..."
        self._popup.dismiss()

    # Carga los capturadores con las fallas leidas de disco.
    def cargar(self, path, filename):
        controlador = App.get_running_app()
        try:
            with open(os.path.join(path, filename[0])) as stream:
                # self.text_input.text = stream.read()
                controlador.leerFallas(stream)
        except IOError, e:
            controlador.mostrarDialogoMensaje(title="Error al leer el archivo de  fallas de disco",
                                    text=e.message)

        except Exception, e:
            controlador.mostrarDialogoMensaje(title="Error en el proceso de lectura de fallas",
                                    text=e.message)

        self.dismiss_popup()

    #Guarda serializa las capturas en un json y lo guarda a disco
    def guardar(self, path, filename):
        controlador = App.get_running_app()
        try:
            full_path = path + filename
            if os.path.isfile(full_path):
                raise ArchivoExisteExcepcion("El archivo que desea guardar ya existe!")

            with open(os.path.join(path, filename), 'w') as stream:
                # stream.write(self.text_input.text)
                controlador = App.get_running_app()
                controlador.guardarFallas(stream)
        except IOError, e:
            controlador.mostrarDialogoMensaje(title="Error al guardar el archivo de fallas en disco",
                                                text=e.message)

        except ArchivoExisteExcepcion, e:
            controlador.mostrarDialogoMensaje(title="Error archivo de capturas existente",
                                                text=e.message)

        except Exception, e:
            controlador.mostrarDialogoMensaje(title="Error en el proceso de guardado de fallas",
                                                text=e.message)

        self.dismiss_popup()


