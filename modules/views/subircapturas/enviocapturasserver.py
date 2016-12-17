# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from constantes import DIVISOR_EN_MB
import time
from time import time
import os

# Screen que contiene la pantalla de envio de datos al sevidor
class EnvioCapturasServerScreen(Screen):

	def __init__(self,**kwargs):
		super(EnvioCapturasServerScreen, self).__init__(**kwargs)
		self.t1 = time()
		self.t2 = 0
		self.barra_progreso.value = 0
		self.cant_bytes_actuales = 0
		# self.bytes_acumulados = 0

	def completarBarraProg(self):
		self.barra_progreso.value = self.barra_progreso.max

	#Al cargarse este screens se comienza la carga de los archivos.
	def on_enter(self):
		print "Cargada screen envio!"
		controlador = App.get_running_app()
		controlador.subir_capturas()

	def getBytesActualesEnviados(self):
		return self.barra_progreso.value


	def setMaxBarraProgreso(self,bytes_totales_a_enviar):
		self.barra_progreso.max = bytes_totales_a_enviar
		print "Cambiado el valor maximo de barra_progreso a: %s " %\
					self.barra_progreso.max


	#Actualiza los labels con la data actual.
	# NOTA IMPORTANTE: cant_bytes ES LA CANTIDAD DE BYTES QUE VA LEYENDO DEL
	# STREAM ACUMULADA, por lo que simplemente se tiene que pisar con
	# el valor de progress_bar y el valor del label
	def actualizar_datos(self,cant_bytes):
		self.cant_bytes_actuales = cant_bytes
		print "bytes_enviados: %s - bytes_totales: %s" % (self.cant_bytes_actuales,
														self.barra_progreso.max)
		self.bytes_subidos.text =  "%s MB/%s MB subidos al servidor... "%\
								( (self.cant_bytes_actuales/DIVISOR_EN_MB),
									(self.barra_progreso.max / DIVISOR_EN_MB))
		print "El texto en bytes_subidos es: %s\n" % self.bytes_subidos.text
		print ""
		self.barra_progreso.value = cant_bytes
		print "Actualizada progress_bar! con bytes_actuales_enviados: %s valor actual: %s" %\
			(self.cant_bytes_actuales,self.barra_progreso.value)
		print ""


	# Actualiza la barra de progreso con un porcentaje deducido del total
	# de las capturas a subir.
	# def actualizar_barra_progreso(self,bytes_actuales_enviados):
	# 	self.barra_progreso.value += int(bytes_actuales_enviados)
	# 	print "Actualizada progress_bar! con bytes_actuales_enviados: %s valor actual: %s" %\
	# 			(bytes_actuales_enviados,self.barra_progreso.value)
	# 	print ""

	# TODO: Terminar la cancelacion de los archivos que se subiran al server.
	def cancelar_subida(self):
		print "Cancelado subida al servidor!"
		print ""
		self.barra_progreso.max = self.barra_progreso.value = 0
		self.bytes_subidos.text = ""
		self.cant_bytes_actuales = 0
		self.manager.current = 'subircapturasservidor'






















