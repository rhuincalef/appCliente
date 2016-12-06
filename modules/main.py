# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys,os



from constantes import *
# Agrega las vistas al path de Python
def agregar_vistas(listaVistas):
    for vista in listaVistas:
        path_local = vista
        sys.path.append(os.path.join( os.getcwd(), path_local  ))
        # sys.path.append(os.path.join(os.path.dirname('__file__'), path_local  ))

#Configuracion y carpetas de las vistas de la app.
agregar_vistas(LISTADO_MODULOS)


#Configuracion de los paths de las views en archivo .cfg
from utilscfg import *

from kinectviewer import KinectScreen
import importlib
from menu import *
from settingscreen import *
from kinectviewer import *
from subircapturasservidor import *
from apiclient1 import *
from capturador import *
from captura import *

import utils
from utils import *

class MainApp(App):
	def __init__(self,**kwargs):
		super(MainApp,self).__init__()
		self.capturador = Capturador()
		self.capturadorInformados = CapturadorInformados()
		self.bind(on_start=self.instanciada_app)


	#Metodo para el chequeo del estado de la aplicacion.
	def instanciada_app(self,app):
		if not conexionSensorEstablecida():
			mostrarDialogo(titulo='Error de conexion',
						content='El sensor no se encuentra conectado.\nConecte el sensor antes de realizar una nueva captura.')


	def getCapturador(self):
		return self.capturador

	def obtenerInformados(self,calle):
		return self.capturadorInformados.solicitarInformados(calle)

	#Captura de nuevos baches(no informados)
	def capturar(self,data,dir_trabajo,nombre_captura,id_falla):
		capturador_a_usar = self.capturador
		if id_falla != FALLA_NO_ESTABLECIDA:
			capturador_a_usar = self.capturadorInformados
		capturador_a_usar.asociarFalla(data, dir_trabajo, nombre_captura,id_falla)


	def getCapturadorInformados(self):
		return self.capturadorInformados


	def inicializar(self,sm):
		conf = leer_configuracion(PATH_ARCHIVO_CONFIGURACION)
		self.cargar_vistas(sm,conf)
    
	def cargar_vistas(self,sm,listaVistas):
		for kev,tupla in listaVistas.iteritems():
			Builder.load_file(tupla["ruta_kv"])
			MyClass = getattr(importlib.import_module(tupla["modulo"]), 
			tupla["clase"])
			instance = MyClass()
			screen = MyClass(name=tupla["nombre_menu"])
			sm.add_widget(screen)


	#Construir aca las instancias del modelo que son usadas por la App.
	# NOTA: Emplear el metodo App.get_running_app() para obtener la instancia
	# actual de MainAPP.
	def build(self):
		sm = ScreenManager()
		self.title = TITULO_APP
		self.inicializar(sm)
		sm.current = SCREEN_PRINCIPAL
		return sm
   
if __name__ == '__main__':
    MainApp().run()

















