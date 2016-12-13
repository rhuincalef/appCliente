# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


# Screen que contiene la pantalla de envio de datos al sevidor
class EnvioCapturasServerScreen(Screen):

	def __init__(self,**kwargs):
		super(EnvioCapturasServerScreen, self).__init__(**kwargs)


	#Actualiza los labels con la data actual.
	def actualizar_datos(self,cant_bytes,total_bytes,archivo_actual):		
		self.bytes_subidos.text =  "%s MB/%s MB subidos al servidor... "%\
									( (cant_bytes/DIVISOR_EN_MB),
										(total_bytes / DIVISOR_EN_MB))
		self.archivo_actual.text = str(archivo_actual) + ".csv"
		

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






















