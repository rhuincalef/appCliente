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

from kivy.uix.label import Label
from capturador import CapturadorInformados

from kivy.uix.textinput import TextInput

class TextInputNumerica(TextInput):

  def insert_text(self, substring, from_undo=False):
    try:
      valid_number = int(substring)
      return super(TextInputNumerica, self).insert_text(valid_number,
                                                  from_undo=from_undo)
    except ValueError, e:
      print "Error numero no valido!"


class ObtenerInformadasScreen(Screen):
   
    def __init__(self, **kwargs):
      cap = CapturadorInformados()

      #TODO: Agregar a cap.solicitarInformados() la calle y la altura
      # para traer la falla desde el servidor.
      # self.fallas_dict = cap.solicitarInformados()
      super(Screen, self).__init__(**kwargs)

    def enviar_peticion(self,calle,altura):
      print "Enviada peticion al servidor"
      print "Calle ",calle
      print "Altura ",altura
      controlador = App.get_running_app()
      controlador.obtenerInformados(calle,altura)
      







