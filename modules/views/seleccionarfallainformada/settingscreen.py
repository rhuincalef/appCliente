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
   
# class ItemFalla(SelectableDataItem):
#   def __init__(self,id_falla,calle,altura, is_selected=False, **kwargs):
#      super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
#      self.id = id_falla
#      self.calle = calle
#      self.altura = altura
#      self.is_selected = False

#   def __cmp__(self,other):
#     if self.id > other.id:
#       return 0
#     elif self.id == other.id:
#       return 0
#     else:
#       return -1



# class CapturadorInformados:

#   def __init__(self):
#     self.colBachesInformados = []
#     self.url_servidor = ""

#   def solicitar_informados(self):
#     dic_json= {
#         "1":{ "id": 1,
#             "calle": "Belgrano",
#             "altura": 200},
#         "2":{ "id": 2,
#             "calle": "Irigoyen",
#             "altura": 200},
#         "3":{ "id": 3,
#             "calle": "Ameguino",
#             "altura": 200},
#         "4":{ "id": 4,
#             "calle": "Pellegrini",
#             "altura": 200},
#         "5":{ "id": 5,
#             "calle": "9 de Julio",
#             "altura": 200},
#         "6":{ "id": 6,
#             "calle": "Aedo",
#             "altura": 200},
#         "7":{ "id": 7,
#             "calle": "Callao",
#             "altura": 200}
#     } 
#     for key,tupla in dic_json.iteritems():
#       falla = ItemFalla(tupla["id"],tupla["calle"],tupla["altura"])
#       self.colBachesInformados.append(falla)
#     self.colBachesInformados = sorted(self.colBachesInformados)
#     return self.colBachesInformados


class SettingScreen(Screen):
   
    def __init__(self, **kwargs):
      cap = CapturadorInformados()
      self.fallas_dict = cap.solicitarInformados()
      # self.fallas_dict = cap.solicitar_informados()
      super(Screen, self).__init__(**kwargs)

      # self.listado1.adapter.bind(on_selection_change=self.on_change)
      # Se inicializan todas las fallas
      self.inicializar_fallas()


    def inicializar_fallas(self):
      for obj in self.fallas_dict:
        obj.is_selected = False
      print "Fallas inicializadas ..."


    # def on_change(self,adapter,**kwargs):
    #   print "SELECCION REALIZADA!!!!!!!!!!!!!"
    #   print "self.fallas_dict -->"
    #   print type(self.fallas_dict)
    #   for obj in self.fallas_dict:
    #     if obj.is_selected == True:
    #       print "falla:",obj.id
    #     print "obj.id = ",obj.id," - is_selected?: ",obj.is_selected
    #     print ""


    def obtener_fallas(self):
      print "self.fallas_dict -->"
      print self.fallas_dict
      print ""
      seleccionados = []
      for obj in self.fallas_dict:
        if obj.is_selected == True:
          print "falla:",obj.id
          seleccionados.append(obj)
      if len(seleccionados) == 0:
        print "Sin fallas seleccionadas"
      return seleccionados


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
