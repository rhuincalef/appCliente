from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
import os
from constantes import *

from os.path import join, isdir

class SubirCapturasServidorScreen(Screen):
	
	def __init__(self,**kwargs):
		super(SubirCapturasServidorScreen, self).__init__(**kwargs)
		self.file_chooser.path = os.getcwd()
		self.file_chooser.rootpath = ROOT_PCD_FOLDER

	def refrescar_directorio(self):
		self.ruta_fs.text = self.file_chooser.path 

	#Metodo para seleccionar todos los archivos en el dir. de trabajo actual.
	def seleccionar_todo(self):
		for arch in self.file_chooser.files:
			if not self.file_chooser.file_system.is_dir(arch):
				print "archivo: ",arch," no es un dir."
				self.file_chooser.selection.append(arch)


	# TODO: Este metodo retorna una lista de archivos seleccionada para subir al servidor.
	# Esta lista es usado en el metodo enviarCapturas(apiClient) de Capturador.
	def enviar_capturas(self):
		rutas = []
		if len(self.file_chooser.selection)>0:
			for archivo in self.file_chooser.selection:
				rutas.append(archivo)
			print "Enviando capturas -->"
			print list(set(rutas))
			return list(set(rutas))

	def volver(self):
		self.manager.current = 'menu'

	# def select(self,path,filenames_selected):
	# 	print "El archivo seleccionado es -->"
	# 	print filenames_selected
	# print os.path.join(path,filenames_selected[0])
   