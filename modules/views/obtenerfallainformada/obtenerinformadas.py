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

# class TextInputNumerica(TextInput):

#   def insert_text(self, substring, from_undo=False):
#     try:
#       valid_number = int(substring)
#       return super(TextInputNumerica, self).insert_text(valid_number,
#                                                   from_undo=from_undo)
#     except ValueError, e:
#       print "Error numero no valido!"


class ObtenerInformadasScreen(Screen):
   
    def __init__(self, **kwargs):
      # cap = CapturadorInformados()      
      #TODO: Agregar a cap.solicitarInformados() la calle y la altura
      # para traer la falla desde el servidor.
      # self.fallas_dict = cap.solicitarInformados()
      super(Screen, self).__init__(**kwargs)
      self.calle = None


    def enviar_peticion(self,calle):
      print "Enviada peticion al servidor"
      print "Calle ",calle
      self.calle = calle
      popup = Popup(title='Peticion al servidor',
              content=Label(text='Cargando fallas...'),
              size_hint=(None, None), 
              size=(400, 400),
              auto_dismiss=False)
      popup.bind(on_open=self.popup_abierto)
      popup.bind(on_open=self.pop_up_cerrado)
      popup.open()
      print "Termine!"


    #Llamado al abrir el pop_up en enviar_peticion().
    def popup_abierto(self,popup):
      calle = self.calle_input_txt.text
      controlador = App.get_running_app()
      controlador.obtenerInformados(self.calle)
      #TODO: Borrar este delay de prueba
      time.sleep(3)
      popup.dismiss()


    def pop_up_cerrado(self,popup):
      print "Cerrado popup!"
      self.volver()

    def volver(self):
      self.calle_input_txt.text = ""
      self.manager.current = 'menutiposfalla'





