# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton, ListItemLabel, ListView
from kivy.uix.listview import CompositeListItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics import *

from  kivy.uix.popup import Popup
from kivy.uix.label import Label
from capturador import CapturadorInformados

from kivy.uix.textinput import TextInput
import time

import threading

from constantes import PATH_ICONO_LUPA
import re

from apiclient1 import ExcepcionAjax,ExcepcionSinInformados
from customwidgets import AutoCompleteTextInput

from screenredimensionable import ScreenRedimensionable
class ObtenerInformadasScreen(ScreenRedimensionable):
   
    def __init__(self, **kwargs):
      super(Screen, self).__init__(**kwargs)
      self.calle = None
      self.ids.container_autocomplete.add_widget(AutoCompleteTextInput())

    # Valida que el string tenga solo caracteres alfanumericos y 
    # underscore.
    def esValida(self,calle):
      if re.search('^(\w+)$',calle) is None:
        return False
      return True

    def enviar_peticion(self):
      self.calle = self.ids.container_autocomplete.children[0].getOpcionSeleccionada()
      print "Enviando peticion al servidor calle: %s\n" % self.calle
      controlador = App.get_running_app()
      popup = controlador.mostrarDialogoEspera(
                              title="Peticion al servidor",
                              content="Cargando fallas...",
                              gif = PATH_ICONO_LUPA
        )
      popup.bind(on_dismiss = self.pop_up_cerrado)
      #Se configura el envio de los archivos como un proceso demonio.
      t = threading.Thread(name = "thread-obtenerInformadas",
                  target = self.threadObtenerInformadas, 
                  args = (popup,) 
                )
      t.setDaemon(True)
      t.start()

    def pop_up_cerrado(self,popup):
      print "Cerrado popup!"
      time.sleep(1)
      self.volver()

    #Llamado al abrir el pop_up en enviar_peticion().
    def threadObtenerInformadas(self,popup):
      calle = self.ids.container_autocomplete.children[0].getOpcionSeleccionada()
      controlador = App.get_running_app()
      try:
        controlador.obtenerInformados(calle)
      except ExcepcionAjax, e:
        controlador = App.get_running_app()
        controlador.mostrarDialogoMensaje(title="Error en solicitud al servidor",
                                            text= e.message)
      except ExcepcionSinInformados as e:
        msgVacio = controlador.mostrarDialogoMensaje(title = "Resultado de peticion vacio",
                                                        text = e.message)
      finally:
        popup.dismiss()
      
    def volver(self):
      self.ids.container_autocomplete.children[0].limpiar()
      self.manager.get_screen("subMenuCapturarFalla").habilitarOpciones()  
      self.manager.current = 'subMenuCapturarFalla'
