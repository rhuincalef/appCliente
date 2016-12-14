# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from constantes import DIVISOR_EN_MB
import time
from time import time

# Screen que contiene la pantalla de envio de datos al sevidor
class EnvioCapturasServerScreen(Screen):

	def __init__(self,**kwargs):
		super(EnvioCapturasServerScreen, self).__init__(**kwargs)
		self.t1 = time()
		self.t2 = 0



	#Al cargarse este screens se comienza la carga de los archivos.
	def on_enter(self):
		print "Cargada screen envio!"
		controlador = App.get_running_app()
		controlador.subir_capturas()


	#Actualiza los labels con la data actual.
	def actualizar_datos(self,cant_bytes,total_bytes):		
		print "Actualizando labels de datos..."
		print "%s - %s"
		self.t2 = time()
		if self.t2 - self.t1 >= 1:
			self.t1 = self.t2
			print "El texto en bytes_subidos es: %s\n" % self.bytes_subidos.text
			self.bytes_subidos.text =  "%s MB/%s MB subidos al servidor... "%\
										( (cant_bytes/DIVISOR_EN_MB),
											(total_bytes / DIVISOR_EN_MB))


		# self.archivo_actual.text = str(self.archivo_actual.text) + ".csv"
		

	# Actualiza la barra de progreso con un porcentaje deducido del total
	# de las capturas a subir.
	def actualizar_barra_progreso(self,cant_fallas_enviadas,total_fallas_confirmadas):
		print "Actualizada progress_bar!"
		print ""
		self.barra_progreso.value = cant_fallas_enviadas/float(total_fallas_confirmadas)


	# TODO: Terminar la cancelacion de los archivos que se subiran al server.
	def cancelar_subida(self):
		print "Cancelado subida al servidor!"
		print ""
		self.manager.current = 'subircapturasservidor'






















