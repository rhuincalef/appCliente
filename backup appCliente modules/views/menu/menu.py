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

import os
from os import path
from os.path import expanduser
from file import XFileOpen, XFileSave

from capturador import ExcepcionRecorridoVacio

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


    def guardarRecorrido(self):
        print "Cargado dialogo guardado de fallas...\n"
        controlador = App.get_running_app()
        if not controlador.existenFallasCargadas():
            controlador.mostrarDialogoMensaje( title= "Guardado de recorrido",
                                        text=  "No existen fallas cargadas en memoria!")
            return
        else:
            XFileSave(on_dismiss=self._fileSaveCallback,
                        title = "Guardar recorrido con fallas",
                        #path=expanduser(u'~'))
                        path=os.getcwd())
        
    def _fileSaveCallback(self, instance):
        if instance.is_canceled():
            return
        #Retorna el path completo a la BD
        nameBD = instance.get_full_name()
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
                    multiselect=False)


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


    # Opcion para subir las fallas capturadas(informadas y nuevas) al servidor
    def menu_subidas_servidor(self):
    	print "Menu subidas"
        self.manager.current = "subircapturasservidor"



# NOTA: La clase que hereda de App tiene que tener el mismo nombre que el layout del 
# archivo .kv.
# La clase que hereda de Screen tiene que tener al final la terminacion "Screen" y si
# existen .kv asociados, se deben agregar 




