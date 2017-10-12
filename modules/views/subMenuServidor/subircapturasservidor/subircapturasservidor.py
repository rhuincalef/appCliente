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

from screenredimensionable import ScreenRedimensionable

from customwidgets import MyListItemButton

#class SubirCapturasServidorScreen(Screen):
class SubirCapturasServidorScreen(ScreenRedimensionable):
	
	def __init__(self,**kwargs):
		super(SubirCapturasServidorScreen, self).__init__(**kwargs)
		self.bind(on_enter = self.refrescar_vista)
		self.listado_capturas.adapter.bind(on_selection_change = self.cambio_seleccion)
		print "Bindeados elementos en subircapturasservidor!\n"




	#Recorre todos los elementos del listview y los marca segun el parametro
	# "activos".
	def marcarCapturas(self,activo):
		print "\nEn marcarCapturas con activo: %s\n" % activo
		#print "\nself.ids.listado.adapter: %s\n\n" % self.ids.listado.adapter.__dict__
		colItemFalla = self.ids.listado.adapter.data
		print "self.ids.listado.adapter.data: %s\n" % self.ids.listado.adapter.data
		print "self.ids.listado.adapter.selection: %s\n" % self.ids.listado.adapter.selection
		
		for index in xrange(0,len(colItemFalla)):
			print "\n\n iteracion %s---->type(colItemFalla[index]): %s\n\n" % \
											(index,type(colItemFalla[index]))
			funcionItemFalla = None
			if activo:
				funcionItemFalla= colItemFalla[index].seleccionar
				print "Seleccionado elementos!\n"
			else:
				funcionItemFalla= colItemFalla[index].desSeleccionar
				print "DesSeleccionado elementos!\n"				
			funcionItemFalla()
		
			#Se seleccionan los botones de la GUI que representan a los elementos
			listadoCompositeListItem = self.ids.listado.children[0].children[0].children
			for elementoComp in listadoCompositeListItem:
				print "iterando botones...\n"
				for boton in elementoComp.children:
					funcionSeleccionarBoton = boton.deselect
					if activo:
						funcionSeleccionarBoton = boton.select
					funcionSeleccionarBoton()

		print "Colecciones actualizadas ...\n"
		print "self.ids.listado.adapter.data: %s\n" % self.ids.listado.adapter.data
		print "self.ids.listado.adapter.selection: %s\n" % self.ids.listado.adapter.selection
		print "\nFin de marcarCapturas()! %s\n"

	def check_box_activado(self):
		print "En check_box_activado con checkbox active: %s\n" % \
					self.ids.check_box_seleccionar_todo.active 
		self.marcarCapturas(activo = self.ids.check_box_seleccionar_todo.active)


	
	#Se desmarcan los elementos seleccionados antes al salir de la vista
	def desMarcarElementos(self):
		print "Desmarcando elementos ...\n" 
		self.marcarCapturas(activo=False)
		self.ids.check_box_seleccionar_todo.active = False
		print "Desmarcados todos los elementos!\n"



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
		existenFallas = existenCapsInconsistentes =  False
		for falla in self.listado_capturas.adapter.data:
			if falla.is_selected:
				existenFallas = True

			# Se verifica que todos los archivos .pcd asociados a las capturas
			# se encuentren aun en el disco al momento del envio, y se marcan
			# aquellos que contienen inconsistencias.
			falla.comprobarConsistencia()

		print "Resultado de controlador.existenFallasSeleccionadas()? %s\n" %\
				existenFallas
		controlador = App.get_running_app()
		if not existenFallas:
			controlador.mostrarDialogoMensaje( title="Selección de fallas",
												text = "Se debe seleccionar al menos una falla\n del listado para realizar un envio al servidor.")
		elif existenCapsInconsistentes:
			popup = controlador.mostrarDialogoMensaje(title="Envío de fallas al servidor",
											text = "Existen fallas que contienen capturas \n inconsistentes que se ignorarán.Se subirán\n solo aquellas que se encuentren inconsistentes.")
			popup.bind(on_dismiss = self._comenzarEnvioArchivos)
		else:
			self.manager.current = 'enviocapturasserver'

	def _comenzarEnvioArchivos(self,popup):
		self.manager.current = 'enviocapturasserver'


# BACKUP!
#	def _existenFallasSeleccionadas(self):
#		existenFallas = False
#		for falla in self.listado_capturas.adapter.data:
#			if falla.is_selected:
#				existenFallas = True
#				break
#		print "Resultado de controlador.existenFallasSeleccionadas()? %s\n" %\
#				existenFallas
#		if not existenFallas:
#			controlador = App.get_running_app()
##			controlador.mostrarDialogoMensaje( title="Seleccion de fallas",
#												text = "Se debe seleccionar al menos una falla\n del listado para realizar un envio al servidor.")
#		else:
#			self.manager.current = 'enviocapturasserver'


	def volver(self):
		#Limpiar el ListView y volver
		print "Vaciadas capturas!"
		self.desMarcarElementos()
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
		'cls_dicts': [{'cls': MyListItemButton,
		               'kwargs': {'text': "{0}".format(attrEstado[0]),
		                          'background_normal': ESTILO_BOTON_NO_SELECCIONADO_LIST_VIEW,
                                  'background_down': ESTILO_BOTON_SELECCIONADO_LIST_VIEW
		                          }
		              }
		              ,{
		                   'cls': MyListItemButton,
		                   'kwargs': {
		                       'text': "{0}".format(attrEstado[1]),
		                       'background_normal': ESTILO_BOTON_NO_SELECCIONADO_LIST_VIEW,
                               'background_down': ESTILO_BOTON_SELECCIONADO_LIST_VIEW
		                        }
		              },
		              {
		                   'cls': MyListItemButton,
		                   'kwargs': { 'text': "{0}".format(attrEstado[2]),
		                   				'background_normal': ESTILO_BOTON_NO_SELECCIONADO_LIST_VIEW,
                                  		'background_down': ESTILO_BOTON_SELECCIONADO_LIST_VIEW
		                            }
		              }]
		    }

	
