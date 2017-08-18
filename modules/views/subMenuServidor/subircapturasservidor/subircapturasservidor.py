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


	#Recorre todos los elementos del listview y los marca segun el parametro
	# "activos".
	def marcarCapturas(self,activo):
		print "En marcarCapturas con activo: %s\n" % activo
		print "self.ids.listado.adapter.data: %s\n" % self.ids.listado.adapter.data
		colItemFalla = self.ids.listado.adapter.data
		for index in xrange(0,len(colItemFalla)):
			print "\n\n ---->type(colItemFalla[index]): %s\n\n" % type(colItemFalla[index])
			funcionItemFalla= colItemFalla[index].desSeleccionar
			if activo:
				print "Seleccionando elementos!\n"
				funcionItemFalla= colItemFalla[index].seleccionar
				
			print "self.ids.listado.adapter.selection: %s\n" % self.ids.listado.adapter.selection
			print "self.ids.listado.adapter.selection[0]: %s\n" % self.ids.listado.adapter.selection[index].__dict__
			print "self.ids.listado.adapter.selection[0].children: %s\n" % self.ids.listado.adapter.selection[index].children
			funcionItemFalla()
			for boton in self.ids.listado.adapter.selection[index].children:
				funcionSeleccionarBoton = boton.deselect
				if activo:
					funcionSeleccionarBoton = boton.select
				funcionSeleccionarBoton()


	#BACKUP!
	#def marcarCapturas(self,activo):
	#	print "En marcarCapturas con activo: %s\n" % activo
	#	print "self.ids.listado.adapter.data: %s\n" % self.ids.listado.adapter.data
	#	for itemfalla in self.ids.listado.adapter.data:
	#		print "\n\n ---->type(itemfalla): %s\n\n" % type(itemfalla)
	#		if activo:
	#			itemfalla.seleccionar()
	#			print "Seleccionado!\n"
	#			print "self.ids.listado.adapter.selection: %s\n" % self.ids.listado.adapter.selection
	#			print "self.ids.listado.adapter.selection[0]: %s\n" % self.ids.listado.adapter.selection[0].__dict__
	#			print "self.ids.listado.adapter.selection[0].children: %s\n" % self.ids.listado.adapter.selection[0].children
	#			for boton in self.ids.listado.adapter.selection[0].children:
	#				boton.select()
	##			break
	#		itemfalla.desSeleccionar()
	#		print "DesSeleccionado!\n"



	#def check_box_activado(self,estaActivo):
	def check_box_activado(self):
		print "En check_box_activado con checkbox active: %s\n" % \
					self.ids.check_box_seleccionar_todo.active 
		self.marcarCapturas(activo = self.ids.check_box_seleccionar_todo.active)


	#Se deseleccionan los elementos cunado adapter.selection<2 porque
	# sino se cambia el estado del primer elemento en la lista a
	# is_selected = True
	def cambio_seleccion(self,adapter):
		print "Cambio la seleccion!\n"
		print "El estado de las fallas es: \n"
		for falla in self.listado_capturas.adapter.data:
			print "%s\n" % falla
		print "\n*****************************************\n"
		print "Fin de cambio_seleccion"


	#BACKUP!
	#Se deseleccionan los elementos cunado adapter.selection<2 porque
	# sino se cambia el estado del primer elemento en la lista a
	# is_selected = True
	#def cambio_seleccion(self,adapter):
	#	print "Cambio la seleccion!\n"
	#	if len(adapter.selection) < 2:
	#		print "DESELECCIONANDO FALLAS!!\N"
	#		for falla in self.listado_capturas.adapter.data:
	#			falla.desSeleccionar()
	#	print "El estado de las fallas es: \n"
	#	for falla in self.listado_capturas.adapter.data:
	#		print "%s\n" % falla
	##	print "\n*****************************************\n"
	#	print "Fin de cambio_seleccion"



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
		self.manager.get_screen("subMenuServidor").habilitarOpciones()  
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

	
