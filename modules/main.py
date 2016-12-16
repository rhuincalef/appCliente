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
		# Los capturadores comparten el mismo apiClient, que lleva la cantidad
		# comun de bytes enviados y bytes totales a enviar, de ambos capturadores.
		apiClientComun = ApiClientApp()
		self.capturador = Capturador(apiClientComun)
		self.capturadorInformados = CapturadorInformados(apiClientComun)
		self.bind(on_start=self.instanciada_app)
		self.screen_manager = None
		print "Inicializado MainApp!"


	#Metodo para el chequeo del estado de la aplicacion.
	def instanciada_app(self,app):
		if not conexionSensorEstablecida():
			mostrarDialogo(titulo='Error de conexion',
						content='El sensor no se encuentra conectado.\nConecte el sensor antes de realizar una nueva captura.')


	def getCapturador(self):
		return self.capturador

	def obtenerInformados(self,calle):
		return self.capturadorInformados.solicitarInformados(calle)


	#Lee el archivo .json a partir del stream
	def leerFallas(self,stream):
		self.capturador.leerFallas(stream)
		self.capturadorInformados.leerFallas(stream)


	#Guarda el archivo .json a partir del stream
	def guardarFallas(self,stream):
		self.capturador.guardarFallas(stream)
		self.capturadorInformados.guardarFallas(stream)




	# Retorna la coleccion de fallas informadas + confirmadas(registradas en la calle)
	# Usado para obtener una coleccion de ItemFalla para mostrar en el listview.
	def filtrarCapturas(self):
		self.capturador.filtrarCapturas()
		self.capturadorInformados.filtrarCapturas()
		colCapturas = []
		colCapturas = self.capturador.getColCapturasConfirmadas() + \
						self.capturadorInformados.getColCapturasConfirmadas()
		return colCapturas


	#Envia las capturas filtradas al servidor con POST
	def subir_capturas(self):
		print "Enviando fallas nuevas ..."	
		# cant_total_fallas_conf = len(self.capturador.getColCapturasConfirmadas() + \
		# 				self.capturadorInformados.getColCapturasConfirmadas())

		bytes_totales_a_enviar = 0
		bytes_totales_a_enviar = self.capturador.calcularTamanioCapturas()+\
							self.capturadorInformados.calcularTamanioCapturas()

		print "Los bytes_totales_a_enviar son : %s" % bytes_totales_a_enviar
		print ""
		lista_capturadores = [self.capturador,self.capturadorInformados]
		t = threading.Thread(target=self.iniciar_threads_capturas, 
								args=(bytes_totales_a_enviar,lista_capturadores,))

		#Se configura el envio de los archivos como un proceso demonio.
		t.setDaemon(True)
		t.start()
		# cant_actual_enviada = self.capturador.enviarCapturas(URL_UPLOAD_SERVER,
		# 										cant_total_fallas_conf,
		# 										cant_actual_enviada)
		# print "Enviando fallas Informadas ..."
		# cant_actual_enviada = self.capturadorInformados.enviarCapturas(URL_UPLOAD_SERVER,
		# 													cant_total_fallas_conf,
		# 													cant_actual_enviada)
		# print "-------------------------->Enviado %s %% de las capturas" % \
		# 											cant_actual_enviada
		# mostrarDialogo(titulo="Subida de capturas",
		# 	content="La carga de capturas en el servidor se ha realizado con exito!")

		

	# Metodo que paraleliza el envio al servidor de los objetos
	def iniciar_threads_capturas(self,bytes_totales_a_enviar,lista_capturadores):
		# Se actualiza el valor maximo de la progressbar con los bytes totales
		# de la peticion
		screen_upload = self.screen_manager.get_screen('enviocapturasserver')
		screen_upload.setMaxBarraProgreso(bytes_totales_a_enviar)
		print "En iniciar_threads_capturas..."
		print "Los bytes_totales_a_enviar recibidos son: %s" % bytes_totales_a_enviar
		print ""
		try:
			print "Por enviar capturas!"
			for capturador in lista_capturadores:
				capturador.enviarCapturas(URL_UPLOAD_SERVER)
			
			#Completa el remanente que falte de la barra de progreso
			screen_upload.completarBarraProg()
			mostrarDialogo(titulo="Subida de capturas",
			content="La carga de capturas en el servidor se ha realizado con exito!")
		
		except ExcepcionAjax, e:
			mostrarDialogo(titulo="Error en la subida de archivos",
				content=e.message)




	# Este metodo se emplea para actualizar el porcentaje enviado al servidor
	# en una ProgressBar.
	# def actualizar_barra_progreso(self,bytes_actuales_enviados):
 #      	#Obtener screenmanager y hacer que se actualice la barra de progreso.
	# 	screen_upload = self.screen_manager.get_screen('enviocapturasserver')
	# 	screen_upload.actualizar_barra_progreso(bytes_actuales_enviados)
	# 	print "------------------------->Enviado %s bytes al sevidor...\n" % \
	# 		screen_upload.getBytesActualesEnviados()


	# Actualiza los labels de cantidad de bytes subidos
	# en la pantalla enviocapturasservidor
	def actualizar_datos(self,bytes_read,encoder_len,finished):
		print "Actualizando data y barra_progreso ..."
		print ""
		screen_upload = self.screen_manager.get_screen('enviocapturasserver')
		screen_upload.actualizar_datos(bytes_read,encoder_len,finished)
		print "------------------------->Enviado %s bytes al sevidor...\n" % \
										screen_upload.getBytesActualesEnviados()

	

	#Captura de nuevos baches(no informados)
	def capturar(self,data,dir_trabajo,nombre_captura,id_falla):
		print "Asociando falla con id_falla %s" % id_falla
		print ""
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
		print "En build()"
		self.screen_manager = sm
		return sm
   
if __name__ == '__main__':
    MainApp().run()

















