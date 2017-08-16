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

from kivy.adapters.dictadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListItemLabel, \
        CompositeListItem, ListView

from kivy.adapters import dictadapter
import threading

class SubirCapturasServidorScreen(Screen):
	
	def __init__(self,**kwargs):
		super(SubirCapturasServidorScreen, self).__init__(**kwargs)
		self.bind(on_enter = self.refrescar_vista)
		self.listado_capturas.adapter.bind(on_selection_change = self.cambio_seleccion)
		print "Bindeados elementos en subircapturasservidor!\n"

	#Se deseleccionan los elementos cunado adapter.selection<2 porque
	# sino se cambia el estado del primer elemento en la lista a
	# is_selected = True
	def cambio_seleccion(self,adapter):
		print "Cambio la seleccion!\n"
		#for elem in adapter.selection:
		#	print "Elemento seleccionado: %s,%s\n" % (type(elem),elem)
		if len(adapter.selection) < 2:
			print "DESELECCIONANDO FALLAS!!\N"
			for falla in self.listado_capturas.adapter.data:
				falla.desSeleccionar()
		print "El estado de las fallas es: \n"
		for falla in self.listado_capturas.adapter.data:
			print "%s\n" % falla
		print "\n*****************************************\n"
		print "Fin de cambio_seleccion"

	#Actualiza la lista de fallas confirmadas
	#def refrescar_vista(self,listview):
	#	print "Refrescando vista!!!! "
	#	controlador = App.get_running_app()
	#	fallas_dic = controlador.filtrarCapturas()
	#	if len(fallas_dic) > 0:
	#		print "Objeto: %s" % fallas_dic[0]
	#		print "Tipo de objeto: %s" % type(fallas_dic[0].getEstado())
	#		print ""
	#	self.listado_capturas.adapter.data = fallas_dic

	def refrescar_vista(self,listview):
		print "Refrescando vista!!!! "
		controlador = App.get_running_app()
		controlador.filtrarCapturas()
		

	def actualizarListaCaps(self,fallasFiltradas):
		self.listado_capturas.adapter.data = fallasFiltradas




	#Envia las capturas adaptadas para el envio al servidor,
	#
	def enviar_capturas(self):
		t = threading.Thread(name="thread-existenFallasSeleccionadas",
								target=self._existenFallasSeleccionadas)
		t.setDaemon(True)
		t.start()

		
	def _existenFallasSeleccionadas(self):
		existenFallas = False
		for falla in self.listado_capturas.adapter.data:
			if falla.is_selected:
				existenFallas = True
				break
		print "Resultado de controlador.existenFallasSeleccionadas()? %s\n" %\
				existenFallas
		if not existenFallas:
			controlador = App.get_running_app()
			controlador.mostrarDialogoMensaje( title="Seleccion de fallas",
												text = "Se debe seleccionar al menos una falla\n del listado para realizar un envio al servidor.")
		else:
			self.manager.current = 'enviocapturasserver'


	def volver(self):
		#Limpiar el ListView y volver
		print "Vaciadas capturas!"
		self.listado_capturas.adapter.data = []
		#self.manager.current = 'menu'
		self.manager.current = 'subMenuServidor'

	# This is quite an involved args_converter, so we should go through the
    # details. A CompositeListItem instance is made with the args
    # returned by this converter. The first three, text, size_hint_y,
    # height are arguments for CompositeListItem. The cls_dicts list
    # contains argument sets for each of the member widgets for this
    # composite: ListItemButton and ListItemLabel.
	def args_converter(self,row_index, an_obj):
		print "En subircapturasservidor.args_converter()...\n"
		print "row_index actual: %s\n" % row_index
		print "falla: %s\n" % an_obj
		attrEstado = an_obj.getEstado().getAttributos()
		print "Los attrEstado son: %s\n" % attrEstado
		print ">...............................................<\n\n"
		return {
		'size_hint_y': None,
		'height': 25,
		'cls_dicts': [{'cls': ListItemButton,
		               'kwargs': {'text': "{0}".format(attrEstado[0])
		                          #'deselected_color': [0.,0,1,1]
		                          }
		              }
		              ,{
		                   'cls': ListItemButton,
		                   'kwargs': {
		                       'text': "{0}".format(attrEstado[1]),
		                       #'deselected_color': [0.,0,1,1],
		                       'background_color': [0,1,0,1]
		                        }
		              },
		              {
		                   'cls': ListItemButton,
		                   'kwargs': { 'text': "{0}".format(attrEstado[2])
		                            }
		              }]
		    }

	
