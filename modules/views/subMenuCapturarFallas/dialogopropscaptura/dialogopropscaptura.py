# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')
from kivy.app import App
from kivy.uix.screenmanager import Screen
import os,sys
from constantes import *
from string import strip
import re
from kivy.properties import NumericProperty
from constantes import FALLA_NO_ESTABLECIDA
from os import path, makedirs

# Imports de xpopup
from tools import *
from xbase import XBase
from notification import XError
from form import *
from notification import XNotification, XConfirmation, XError

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from iconfonts import icon

import shutil
from constantes import TAMANIO_ICONOS_CTRL_BAR
from os import path

from screenredimensionable import ScreenRedimensionable
class DialogoPropsCapturaScreen(ScreenRedimensionable):

	def __init__(self,**kwargs):
		super(DialogoPropsCapturaScreen, self).__init__(**kwargs)
		self.dir_chooser.path = os.getcwd()
		self.dir_chooser.rootpath = ROOT_PCD_FOLDER
		# Se crean los botones y se agregan al widget

		self.crearDirBtn = Button(
			id="btn_crear_dir",
			text = "%s Crear carpeta"%(icon('fa-clone',TAMANIO_ICONOS_CTRL_BAR)),
			markup=True,
			#size_hint = (0.20,1),
			size_hint = (0.15,1),
			background_normal = ESTILO_BOTON_DEFAULT_OPCIONES_MENU,
			background_down = ESTILO_BOTON_DEFAULT_PRESIONADO
		)
		self.ctl_bar.add_widget(self.crearDirBtn)
		#self.crearDirBtn.disabled = True
		self.crearDirBtnUID = self.crearDirBtn.fbind('on_press', self.crearDir)
		if not self.crearDirBtnUID:
			print "ERROR BINDEANDO boton CrearDir!\n"

		self.botonBorrado = Button(
			id="boton1",
			#text = "%s Borrar carpeta"%(icon('fa-window-close',TAMANIO_ICONOS_CTRL_BAR)),
			text = "-",
			markup=True,
			#size_hint = (0.20,1),
			size_hint = (0.15,1),
			background_normal = ESTILO_BOTON_DEFAULT_OPCIONES_MENU,
			background_down = ESTILO_BOTON_DEFAULT_PRESIONADO
		)
		self.ctl_bar.add_widget(self.botonBorrado)
		self.borrarUID = None
		#self.borrarUID = self.botonBorrado.fbind('on_press', self.eliminarDirectorio)
		#self.botonBorrado.disabled = True
		#if not self.borrarUID:
		#	print "ERROR BINDEANDO boton BorrrarDir!\n"

		#Tercer boton para desvincular los otros dos. 
		#NOTA: La libreria no permite desasociar un boton
		self.botonBorrarCarpetas = Button(
			id="boton2",
			text = "Borrar carpetas",
			markup=True,
			#size_hint = (0.20,1),
			size_hint = (0.15,1),
			background_normal = ESTILO_BOTON_DEFAULT_OPCIONES_MENU,
			background_down = ESTILO_BOTON_DEFAULT_PRESIONADO
		)
		self.ctl_bar.add_widget(self.botonBorrarCarpetas)
		self.botonBorrarCarpetasUID = self.botonBorrarCarpetas.fbind('on_press', self.eliminarDirectorio)
		if not self.botonBorrarCarpetasUID:
			print "ERROR BINDEANDO boton Modo!\n"

		#print "self.borrarUID tiene: %s\n" % self.borrarUID
		self.borrarSeleccionUID = self.cancelarSeleccionUID = None
		#Flag empleado para detectar si esta activa la opcion de "borrado de carpetas"
		self.estaEnModoBorrado = False
		print "Bindeados botones creacion y borrado dialogopropscaptura!\n"


	def validar(self):
		pass

	#Activado cuando se pulsa enter el en Text-Input.
	def validar1(self,txt):
		print "VALIDANDO TEXTO de nombre de archivo!!\n"

	# NOTA: Por defecto el filechooser carga la seleccion con el directorio
	# de trabajo actual.
	def on_enter(self):
		print "Entre al filechooser"
		print "El directorio actual seleccionado es: ",self.dir_chooser.selection
		print ""
		print "PRE-ENTER!!"

	def esDirValido(self,dirChooser):
		#Si es el mismo dir que el dir de ejecucion de la app
		# se no se borra 
		if os.getcwd() == self.dir_chooser.selection[0]:
			print "Dir. invalido, es el mismo dir que el dir de ejecucion!\n"
			return False
		if len(dirChooser.selection) > 0:
			dirName = dirChooser.selection[0]	
		  	return self.dir_chooser.file_system.is_dir(dirName)
		return False

	def seleccionado(self, seleccion):
		print "La seleccion es: ",seleccion
		print ""
		# Si no es un dir actualiza self.dir_label.text, se remueve la entrada
		# en la coleccion selection y se agrega el directorio actual.
		if (len(seleccion) > 0) and not self.dir_chooser.file_system.is_dir(seleccion[0]):
			print "No es dir!"
			self.dir_label.text = "Archivo: " + seleccion[0]
			self.dir_chooser.selection.pop()
			self.dir_chooser.selection.append(self.dir_chooser.path)
			print "Actualizado! self.dir_chooser.selection: %s" % self.dir_chooser.selection
			print ""

	def cambio_dir(self):
		print "CAMBIO DE DIRECTORIO!"
		print "selection : %s" % self.dir_chooser.selection
		print "" 
		self.dir_chooser.selection = []
		self.dir_chooser.selection.append(self.dir_chooser.path)
		self.dir_label.text = self.dir_chooser.path
		print "Seleccion actual -->"
		print self.dir_chooser.selection

	# Retorna una cadena con los espacios en blanco en medio escapados,
	# y los espacios anteriores y posteriores a la misma trimeados 
	def _sanearCadena(self,cad):
		nueva = cad.strip()
		micad = nueva
		return micad

	#Se leen los datos ingresados por el usuario y se envian a la sigueinte
	#screen.
	def menu_falla_nueva(self):
		#nombre_captura = self.nombre_cap.text
		nombre_captura = self.ids.nombre_captura_txt.text
		es_nombre_valido = es_dir_valido = False
		#print "Archivo captura seleccionado: %s\n" % nombre_captura
		#print strip(nombre_captura)
		#NOTA: Solo se permiten nombres sin _ y un Numero y sin
		# extension .PCD
		PATRON_RE = "(.*\.pcd)|(.*_[0-9].*)"
		match = None
		match = re.search(PATRON_RE,nombre_captura)
		if (nombre_captura != None) and strip(nombre_captura) and \
			match is None:
			es_nombre_valido = True

		nombre_dir = self.dir_chooser.selection[0] 
		print "Dir. seleccionado: ", nombre_dir
		#Si no es cadena vacia y es un directorio valido
		if (nombre_dir!= None) and (strip(nombre_dir)) and \
									self.dir_chooser.file_system.is_dir(nombre_dir):
			es_dir_valido = True

		print "es_nombre_valido: ",str(es_nombre_valido)
		print "es_dir_valido: ",str(es_dir_valido)
		print ""
		# Si es un dirvalido se envian los datos a kinect_screen
		if es_nombre_valido and es_dir_valido:
			kinect_screen = self.manager.get_screen('capturaKinect')
			kinect_screen.setDatosCaptura(self._sanearCadena(nombre_captura).encode("utf-8"),
				self.dir_chooser.selection[0])
			print "Dir. de trabajo: %s\n" % self.dir_chooser.path
			print "Data SETEADA!!! con: nombre_cap = ",self._sanearCadena(nombre_captura).encode("utf-8"),"; dir_trabajo = ",self.dir_chooser.selection[0]
			self.manager.current = 'capturaKinect'


	def crearDir(self,componente):
		print "Creando directorio!!\n"
		XTextInput(title='Creacion de directorio', text='Ingrese el nombre del nuevo directorio',
					on_dismiss=self._createDir,
					background = ESTILO_BACKGROUND_MODAL_XBASE,
					separator_color = COLOR_SEPARADOR_POPUPS 
					)
	
	def _createDir(self, instance):
		if instance.is_canceled():
			return
		new_folder = self.dir_chooser.selection[0] + path.sep + instance.get_value()
		print "En self._create_dir(): %s\n" % new_folder
		if path.exists(new_folder):
			print "La carpeta existe!!!"
			#XError(text=_('La carpeta "%s" ya existe. Ingrese otro nombre de carpeta') % instance.get_value())
			XError(text=('La carpeta "%s" ya existe. Ingrese otro nombre de carpeta') % instance.get_value(),
				background = ESTILO_BACKGROUND_MODAL_XBASE,
				separator_color = COLOR_SEPARADOR_POPUPS)
			return
		makedirs(new_folder)
		#Se refresca el directorio de trabajo al crear un dir nuevo
		self.dir_chooser._update_files()
		return
		

	# Este metodo se llama desde la opcion "Borrar Carpetas" y permite 
	# acceder al borrado de carpetas individuales.
	def eliminarDirectorio(self, componente):
		print "En eliminarDirectorio handler...\n"
		if self.estaEnModoBorrado:
			print "Estoy en modo de borrado, reestablecendo GUI\n"
			self._reestablecerGUI()
			return
		
		print "Segui...\n"
		self.estaEnModoBorrado = True
		dirSeleccionado = self.dir_chooser.selection[0]
		#Se habilita la seleccion de directorios
		self.dir_chooser.dirselect = True
		#Se agrega dinamicamente dos botones para borrar y cancelar el borrado
		self.cargarOpcionesBorrado()

	#Agrega las opciones de "Borrar" y "Cancelar borrado" en donde estan 
	# las opciones de "Crear carpeta" y "Borrar carpeta".
	def cargarOpcionesBorrado(self):
		#Se cambia el texto de los botones y se bindean de nuevo con las nuevas acciones
		# relacionadas con el borrado de carpetas
		print "En cargarOpcionesBorrado()....\n"
		#observers = self.crearDirBtn.get_property_observers('on_press')
		#print "\nObservadores de self.crearDirBtn --->\n\n"
		#print '\n\nlist of observers before unbinding: {}\n'.format(observers)
		#print 'list of observers before unbinding: {}\n'.format(observers)
		
		#self.crearDirBtn.unbind_uid('on_press', self.crearDirBtnUID)
		#self.crearDirBtn.text = "%sBorrar!" % (icon('fa-check-square-o',TAMANIO_ICONOS_CTRL_BAR))
		#self.borrarSeleccionUID = self.crearDirBtn.fbind('on_press', self._borrarSeleccion)

		#print "\nObservadores de self.crearDirBtn luego de unbinding --->\n\n"
		#print '\n\nlist of observers after unbinding: {}\n'.format(self.crearDirBtn.get_property_observers('on_press'))
		#print 'list of observers after unbinding: {}\n\n'.format(self.crearDirBtn.get_property_observers('on_press'))
		#print "Desbindeado self.crearDirBtn...\n"


		observers = self.botonBorrado.get_property_observers('on_press')
		print "\nObservadores de self.botonBorrado antes de unbinding--->\n\n"
		print '\n\nlist of observers before unbinding: {}\n'.format(observers)
		print 'list of observers before unbinding: {}\n\n'.format(observers)
		
		#print "UID de borrarDir --> %s\n" % self.borrarUID
		#self.botonBorrado.unbind_uid('on_press', self.borrarUID)
		self.botonBorrado.text = "%sBorrar!" % (icon('fa-check-square-o',TAMANIO_ICONOS_CTRL_BAR))
		self.borrarSeleccionUID = self.botonBorrado.fbind('on_press', self._borrarSeleccion)

		self.botonBorrarCarpetas.text = "Cancelar"		

		self.crearDirBtn.disabled = True

		print "\nObservadores de self.botonBorrado luego de unbinding --->\n\n"
		print '\n\nlist of observers after unbinding: {}\n'.format(self.botonBorrado.get_property_observers('on_press'))
		print 'list of observers after unbinding: {}\n\n'.format(self.botonBorrado.get_property_observers('on_press'))

	#Borrado de los directorios que se seleccionaron 
	def _borrarSeleccion(self,componente):
		print "En _borrarSeleccion()...\n"
		if self.esDirValido(self.dir_chooser):
			dirABorrar = self.dir_chooser.selection[0]
			print "Borrando dir: %s\n" % dirABorrar
			shutil.rmtree(dirABorrar,onerror = self.deleteError)
			print "Borrado correctamente!\n"
			print "Update_files antes\n"
			self.dir_chooser._update_files()
			print "Update_files despues!!\n"

		
	#Cancelar la seleccion para borrar
	#def _cancelarSeleccion(self,boton):
	#	print "No se borra el dir...%s\n" % type(boton)
		#self._reestablecerGUI()

	#Agrega nuevamente las opciones anteriores para "Crear carpeta"
	#  y "Borrar carpeta".
	def _reestablecerGUI(self):
		print "Reestableciendo GUI! ...\n"
		#Se reestablece el boton de "Borrar carpetas" y el boton del medio
		self.botonBorrarCarpetas.text = "Borrar carpetas"
		self.estaEnModoBorrado = False

		self.botonBorrado.unbind_uid('on_press', self.borrarSeleccionUID)
		print "Desbindeado self.botonBorrado de borrado!\n"
		self.botonBorrado.text = "-"

		# Se modifica el modo de seleccion de directorios y se habilita
		# la creacion de directorios
		self.dir_chooser.dirselect = False
		self.crearDirBtn.disabled = False
		

	def _noBorrarDir(self):
		print "No se borra el dir"

	#Handler por default para errores de borrado.
	def deleteError(self):
		print "Error ocurrido al borrar! %s\n" % self.dir_chooser.path + path.sep + self.dir_chooser.selection[0] 
		XError(text= ("Error borrando el directorio\n %s" % shutil.Error))

	def default(self,evt):
		pass

	def volver(self):
		#Limpiar la seleccion y cambiar screen
		self.dir_chooser.selection = []
		self.dir_chooser.selection.append(self.dir_chooser.path)
		#Se limpia el textinput en el que el usuario pudo haber ingresado datos
		for w in self.ctl_bar.children:
			if isinstance(w,TextInput):
				w.text = ""

		#Si es una fallainformada se regresa al menu de 
		# seleccion de fallas informadas, sino al menu con las
		# propiedades de las fallas nuevas('propsFallaConfirmada'). 
		#menu_cambio = 'menutiposfalla'
		controlador = App.get_running_app()
		print "En dialogopropscaptura.getData(): %s\n" % controlador.getData("idFalla")
		menu_cambio = 'propsFallaConfirmada'
		if controlador.getData("idFalla") > 0:
			#menu_cambio = 'settingscreen'
			menu_cambio = 'capturarFallaInformada'

		print "controlador.getData('idFalla') > 0 ? %s\n" % (controlador.getData("idFalla") > 0)
		self.manager.current = menu_cambio

