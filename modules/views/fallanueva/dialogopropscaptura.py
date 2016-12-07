# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')
from kivy.app import App
from kivy.uix.screenmanager import Screen
import os,sys
from constantes import *
from string import strip

from kivy.properties import NumericProperty
from constantes import FALLA_NO_ESTABLECIDA


# TODO: DESPUES DE HACER EL volver en kinectviewer.py actualizar el listado
# de archivos que muestra el filechooser!!.
# -Cuando se selecciona un archivo que se muestre en el label de navegacion
# el nombre del archivo seleccionado. 

class DialogoPropsCapturaScreen(Screen):

	idFalla = NumericProperty(FALLA_NO_ESTABLECIDA)

	def __init__(self,**kwargs):
		super(DialogoPropsCapturaScreen, self).__init__(**kwargs)
		self.dir_chooser.path = os.getcwd()
		self.dir_chooser.rootpath = ROOT_PCD_FOLDER

	def set_id_falla_informada(self,id_falla):
		self.idFalla = id_falla 

	def validar(self):
		pass

	# NOTA: Por defecto el filechooser carga la seleccion con el directorio
	# de trabajo actual.
	def on_enter(self):
		print "Entre al filechooser"
		print "El directorio actual seleccionado es: ",self.dir_chooser.selection
		print ""

	def seleccionado(self, seleccion):
		print "La seleccion es: ",seleccion
		print ""

	def cambio_dir(self):
		self.dir_chooser.selection = []
		self.dir_chooser.selection.append(self.dir_chooser.path)
		self.dir_label.text = self.dir_chooser.path
		print "Seleccion actual -->"
		print self.dir_chooser.selection


	#Se leen los datos ingresados por el usuario y se envian a la sigueinte
	#screen.
	def menu_falla_nueva(self):
		nombre_captura = self.nombre_cap.text
		es_nombre_valido = es_dir_valido = False
		print "Archivo captura seleccionado: ", nombre_captura
		print strip(nombre_captura)
		if strip(nombre_captura):
			es_nombre_valido = True 

		nombre_dir = self.dir_chooser.selection[0] 
		print "Dir. seleccionado: ", nombre_dir
		if (nombre_dir!= None) and (strip(nombre_dir)):
			es_dir_valido = True

		print "es_nombre_valido: ",str(es_nombre_valido)
		print "es_dir_valido: ",str(es_dir_valido)
		print ""

		if es_nombre_valido and es_dir_valido:
			kinect_screen = self.manager.get_screen('capturaKinect')
			kinect_screen.setDatosCaptura(self.nombre_cap.text,
				self.dir_chooser.selection[0],self.idFalla)
			print "Data SETEADA!!! con: nombre_cap = ",self.nombre_cap.text,"; dir_trabajo = ",self.dir_chooser.selection[0]
			self.manager.current = 'capturaKinect'

	def volver(self):
		#Limpiar la seleccion y cambiar screen
		self.dir_chooser.selection = []
		self.dir_chooser.selection.append(self.dir_chooser.path)
		self.nombre_cap.text = ""
		#Si es una fallainformada se regresa al menu de 
		# seleccion de fallas informadas, sino al principal. 
		menu_cambio = 'menutiposfalla'
		if self.idFalla != FALLA_NO_ESTABLECIDA:
			menu_cambio = 'settingscreen' 
		self.idFalla = FALLA_NO_ESTABLECIDA
		self.manager.current = menu_cambio





