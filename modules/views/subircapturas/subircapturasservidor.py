from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
import os
from constantes import *



class SubirCapturasServidorScreen(Screen):
	
	def __init__(self,**kwargs):
		super(SubirCapturasServidorScreen, self).__init__(**kwargs)
		self.file_chooser.path = os.getcwd()
		self.file_chooser.rootpath = ROOT_PCD_FOLDER


	def refrescar_directorio(self):
		self.ruta_fs.text = self.file_chooser.path 


	#TODO: Metodo para seleccionar todos los archivos en el dir. de trabajo actual.
	def seleccionar_todo(self):
		pass

	# TODO: Este metodo retorna una lista de archivos seleccionada para subir al servidor.
	# Esta lista es usado en el metodo enviarCapturas(apiClient) de Capturador.
	def enviar_capturas(self):
		rutas = []
		for archivo in filenames_selected:
			rutas.append(os.path.join(path,archivo))
		print rutas
		return rutas
		# os.path.join(path,filenames_selected[0])


	def volver(self):
		self.manager.current = 'menu'

	def select(self,path,filenames_selected):
		print "Seleccione algo!!"
		# print "filechooser.path -->"
		# print self.file_chooser.path
		# print "El archivo seleccionado es -->"
		# print "filenames -->"
		# print filenames_selected

		# print os.path.join(path,filenames_selected[0])
   