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


from screenredimensionable import ScreenRedimensionable

#class CapturarFallaInformadaScreen(Screen):
class CapturarFallaInformadaScreen(ScreenRedimensionable):
   
    def __init__(self, **kwargs):
      super(Screen, self).__init__(**kwargs)
      self.bind(on_enter = self.refrescar_vista)

    #def cambioSeleccion(self,adapter):
    #  print "\ncambio la seleccion! len(adapter.selection) = %s\n\n" % len(adapter.selection)
    #  itemButton = adapter.selection[0]
    #  print "seleccion actual: %s\n" % len(adapter.selection)  

    #def on_enter(self):
    #  controlador = App.get_running_app()
    #  controlador.desSeleccionarInformados()

  

    def buscarFallaSeleccionada(self,fallas_dict):
      # Se carga el dialogopropsscreen con el id_falla de la falla seleccionada
      # en el listview.
      id_falla_seleccionada = -1 
      for falla in fallas_dict:
        print "recorriendo falla informada %s falla.estaSeleccionado: %s\n" % \
                          (falla.getEstado().getId(),falla.estaSeleccionado())
        if falla.estaSeleccionado():
          id_falla_seleccionada = falla.getEstado().getId()
          break
      return id_falla_seleccionada 


    def obtener_fallas(self):
      controlador = App.get_running_app()

      # Diccionario de objetos ItemFalla(mostrados en el listview cuando se 
      # seleccionan los baches).
      id_falla_seleccionada = -1
      fallas_dict = controlador.getCapturadorInformados().getColBachesInformados()

      if len(fallas_dict) == 0:
        #print "Coleccion vacia de fallas!\n"
        controlador.mostrarDialogoMensaje(title="Captura de falla informada", 
                                            text="No existen fallas informadas asociadas a la calle")
        return

      id_falla_seleccionada = self.buscarFallaSeleccionada(fallas_dict)
      if id_falla_seleccionada != -1:
        print "Existen fallas seleccionadas"
        print "Agregando falla informada para ser capturada: "
        print "Id: ",id_falla_seleccionada
        print ""
        #NOTA: Se coloca el idFalla en el dic. del controlador para que la vista
        # dialogoPropsCaptura sepa donde volver cuando regresa.
        controlador = App.get_running_app()
        controlador.agregarData("idFalla",id_falla_seleccionada)
        print "id_falla_seleccionada: %s\n" % controlador.getData("idFalla")
        self.manager.current = 'dialogopropscaptura'
      else:
        #print "No existen fallas seleccionadas para enviar!\n"
        controlador.mostrarDialogoMensaje(title="Captura de falla informada", 
                                            text="Debe seleccionar una falla informada para capturar")

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
      self.manager.get_screen("subMenuCapturarFalla").habilitarOpciones()
      self.manager.current = 'subMenuCapturarFalla'
