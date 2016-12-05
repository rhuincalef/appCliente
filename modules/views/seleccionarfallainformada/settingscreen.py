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

class SettingScreen(Screen):
   
    def __init__(self, **kwargs):
      super(Screen, self).__init__(**kwargs)
      self.bind(on_enter=self.refrescar_vista)

    def obtener_fallas(self):
      controlador = App.get_running_app()
      # Diccionario de objetos ItemFalla(mostrados en el listview cuando se 
      # seleccionan los baches).
      fallas_dic = controlador.getCapturadorInformados().getColBachesInformados()
      print "fallas_dict -->"
      print fallas_dict
      print ""
      seleccionados = []
      for obj in fallas_dict:
        if obj.is_selected == True:
          print "falla:",obj.id
          seleccionados.append(obj)
      if len(seleccionados) == 0:
        print "Sin fallas seleccionadas"
      return seleccionados

    # Cuando se carga el screen se actualiza el listao de fallas seleccionadas
    def refrescar_vista(self,settignscreen):
      print "Actualizando listado de fallas..."
      print "tipo: ", str(type(settignscreen))
      controlador = App.get_running_app()
      fallas_dic = controlador.getCapturadorInformados().getColBachesInformados()
      self.listado1.adapter.data = fallas_dic
      print "Actualizado listado!"


   # This is quite an involved args_converter, so we should go through the
    # details. A CompositeListItem instance is made with the args
    # returned by this converter. The first three, text, size_hint_y,
    # height are arguments for CompositeListItem. The cls_dicts list
    # contains argument sets for each of the member widgets for this
    # composite: ListItemButton and ListItemLabel.
    def args_converter(self,row_index, an_obj):
      print "row_index actual: ",row_index
      print ""
      return {
        # 'text': an_obj.id,
        'size_hint_y': None,
        'height': 25,
        'cls_dicts': [{'cls': ListItemButton,
                       'kwargs': {'text': "{0}".format(an_obj.id)
                                  #'deselected_color': [0.,0,1,1]
                                  }
                      }
                      ,{
                           'cls': ListItemButton,
                           'kwargs': {
                               'text': "{0}".format(an_obj.calle),
                               #'deselected_color': [0.,0,1,1],
                               'background_color': [0,1,0,1]
                                }
                      },
                      {
                           'cls': ListItemButton,
                           'kwargs': { 'text': "{0}".format(an_obj.altura)
                                    }
                      }]
            }
