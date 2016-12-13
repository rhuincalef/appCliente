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
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
import os
from constantes import *

from os.path import join, isdir

class SubirCapturasServidorScreen(Screen):
	
	def __init__(self,**kwargs):
		super(SubirCapturasServidorScreen, self).__init__(**kwargs)
		self.bind(on_enter=self.refrescar_vista)		


	#Actualiza la lista de fallas confirmadas
	def refrescar_vista(self,listview):
		print "Refrescando vista!!!! "
		controlador = App.get_running_app()
		fallas_dic = controlador.filtrarCapturas()
		if len(fallas_dic) > 0:
			print "Objeto: %s" % fallas_dic[0]
			print "Tipo de objeto: %s" % type(fallas_dic[0].getEstado())
			print ""
		self.listado_capturas.adapter.data = fallas_dic

	#Envia las capturas adaptadas para el envio al servidor
	def enviar_capturas(self):
		controlador = App.get_running_app()
		controlador.subir_capturas()

		
	def volver(self):
		#Limpiar el ListView y volver
		print "Vaciadas capturas!"
		self.listado_capturas.adapter.data = []
		self.manager.current = 'menu'

	# This is quite an involved args_converter, so we should go through the
    # details. A CompositeListItem instance is made with the args
    # returned by this converter. The first three, text, size_hint_y,
    # height are arguments for CompositeListItem. The cls_dicts list
    # contains argument sets for each of the member widgets for this
    # composite: ListItemButton and ListItemLabel.
	def args_converter(self,row_index, an_obj):
		print "row_index actual: ",row_index
		print ""
		print "tipo: %s" % type(an_obj)
		print ""
		return {
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
