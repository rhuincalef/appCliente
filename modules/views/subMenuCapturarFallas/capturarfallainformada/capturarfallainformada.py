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
from constantes import FALLA_NO_ESTABLECIDA

class CapturarFallaInformadaScreen(Screen):
   
    def __init__(self, **kwargs):
      super(Screen, self).__init__(**kwargs)
      self.bind(on_enter=self.refrescar_vista)

    def obtener_fallas(self):
      controlador = App.get_running_app()
      # Diccionario de objetos ItemFalla(mostrados en el listview cuando se 
      # seleccionan los baches).
      fallas_dict = controlador.getCapturadorInformados().getColBachesInformados()
      if len(fallas_dict) > 0:
        print "Existen fallas seleccionadas"
        # Se carga el dialogopropsscreen con el id_falla de la falla seleccionada
        # en el listview.
        id_falla_seleccionada = -1 
        for falla in fallas_dict:
          if falla.estaSeleccionado():
            id_falla_seleccionada = falla.getEstado().getId()
            break

        print "Agregando falla informada para ser capturada: "
        print "Id: ",id_falla_seleccionada
        print ""
        #self.manager.get_screen('dialogopropscaptura').set_id_falla_informada(id_falla_seleccionada)
        #print "get_id_falla_informada() retorno: %s\n" %\
        #    self.manager.get_screen('dialogopropscaptura').get_id_falla_informada()
        controlador = App.get_running_app()
        controlador.agregarData("idFalla",id_falla_seleccionada)
        print "id_falla_seleccionada: %s\n" % controlador.getData("idFalla")
        
        self.manager.current = 'dialogopropscaptura'
        print "Cambie el screen!"
      else:
        print "No existen fallas seleccionadas para enviar"

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
                       'kwargs': {'text': "{0}".format(an_obj.getEstado().getId())
                                  #'deselected_color': [0.,0,1,1]
                                  }
                      }
                      ,{
                           'cls': ListItemButton,
                           'kwargs': {
                               'text': "{0}".format(an_obj.getEstado().getCalle()),
                               #'deselected_color': [0.,0,1,1],
                               'background_color': [0,1,0,1]
                                }
                      },
                      {
                           'cls': ListItemButton,
                           'kwargs': { 'text': "{0}".format(an_obj.getEstado().getAltura())
                                    }
                      }]
            }

    #Se regresa a menutiposfalla, y se reestablece el valor de
    #idFalla a su valor original
    def volver(self):
      controlador = App.get_running_app()
      controlador.agregarData("idFalla",FALLA_NO_ESTABLECIDA)
      #controlador.desSeleccionarFallas()
      controlador.desSeleccionarInformados()
      self.manager.current = 'menutiposfalla'