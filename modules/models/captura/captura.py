import pypcd
import numpy as np
from constantes import *

import os
from os import path
import subprocess
from subprocess import CalledProcessError
import threading
import sys

from constantes import EXTENSION_SUBIDA_SERVER_DEFAULT

import utils
from utils import *
from kivy.app import App

from persistent import Persistent

class Captura(Persistent):

	def __init__(self,nombre,dirLocal,formatoArchivo,extensionArchivo):
		self.nombreCaptura = nombre #Nombre sin extension.Ej:  "NUEVOSCONFIRMADOS"
		self.dirLocal = dirLocal #Directorio local donde se guardan los archivos de captura.
		self.formato = formatoArchivo
		self.extension = extensionArchivo
		self.nombreArchivoCaptura = None #Nombre del archivo de captura completo.Ej."NUEVOSCONFIRMADOS_1.pcd"
		self.estaSubidaAlServidor = False # determina si una captura se subio
										#completamente al servidor.
		self.consistente = True  # Determina si tanto la captura en memoria como en disco 
								 # existen al momento de subirse al servidor,
								 # si no es asi, no se la considera 
								 # para enviarse al servidor.

	def existeEnDisco(self):
		""" Este metodo verifica si el archivo existe en disco antes de realizar
			el envio al servidor. Retorna True si el archivo existe en disco y 
			False en caso contrario."""
		print "comprobando captura: %s\n" % self.getFullPathCaptura()
		return path.isfile(self.getFullPathCaptura())
 	 	
 	def esConsistente(self):
 		return self.consistente

	def marcarComoInconsistente(self):
		"""Marca la captura como inconsistente."""
		self.consistente = False

	def getNombreCapturaConvertida(self):
		"""Retorna el nombre del archivo + SUBFIJO + ID_INCREMENTAL + EXTENSION_SUBIDA_DEFAULT
		(puede ser .pcd o .csv)."""
		archivo_csv_salida = os.path.splitext(self.nombreArchivoCaptura)[0] 
		return archivo_csv_salida + EXTENSION_SUBIDA_SERVER_DEFAULT
	
	def getFullPathCapturaConv(self):
		"""Retorna la ruta completa al archivo asociado a la captura. """
		return self.dirLocal + path.sep + self.getNombreCapturaConvertida() 

	#Retorna la ruta completa al archivo .pcd asociado con la captura
	def getFullPathCaptura(self):
		return self.dirLocal + path.sep + self.nombreArchivoCaptura 

	def getNombreArchivo(self):
		return self.nombreCaptura

	#NOTA: Este es el archivo de captura final con el nombre+SUBFIJO+ID_INCREMENTAL.pcd
	def getNombreArchivoCaptura(self):
		return self.nombreArchivoCaptura

	def getDirLocal(self):
		return self.dirLocal

	def getFormato(self):
		return self.formato

	def getExtension(self):
		return self.extension

	def setNombreArchivoCaptura(self, archivo_salida):
		self.nombreArchivoCaptura = archivo_salida 

	def __repr__(self):
		return "Captura: nombreArchivoCaptura=%s , dirLocal = %s , nombreCaptura= %s;\n" %\
					(self.nombreArchivoCaptura,self.dirLocal,self.nombreCaptura)

	def __str__(self):
		""" Usado para el almacenamiento en formato json."""
		cadena = ""
		if self.nombreArchivoCaptura is not None:
			cadena = self.nombreArchivoCaptura
		return cadena

	# Usado por capturador.registrarCaptura(). Almacena el .pcd en disco.
	#def almacenarLocalmente(self,data1,capturador, modo = PCD_XYZ_FORMAT):
	def almacenarLocalmente(self,data1,capturador,modo):
		"""Almacena el archivo de nube de puntos en disco en formado pcd. """
		data = np.asarray(data1,dtype=np.float32)
		instanciar_pointcloud = pypcd.make_xyz_point_cloud
		if modo == TIPO_CAPTURA_DEFAULT:
			instanciar_pointcloud = pypcd.make_xyz_rgb_point_cloud

		pc = instanciar_pointcloud(data)
		# Se obtiene la cantidad de archivos con un nombre dentro
		# en un dir. de prueba dado
		try:
		  cant_archivos_actuales = capturador.getCantidadCapturas(self.nombreCaptura,
		                                                self.dirLocal,self.extension)
		  archivo_salida = self.nombreCaptura + SUBFIJO + str(cant_archivos_actuales) \
		                    + self.extension

		  path_out = self.dirLocal + path.sep + archivo_salida 
		  pc.save_pcd(path_out)
		  self.nombreArchivoCaptura = archivo_salida
		  return archivo_salida
		except OSError as e:
		  print "Error al listar archivos en directorio %s \n" % self.dirLocal
		  print "OSError: %s\n" % e 
		  sys.exit(1)


	# Captura.descartar()
	#def descartar(self,colCaps):
	def descartar(self, itemFalla):
		"""Descarta la captura de disco, borrando el .pcd y borrandose
		de la coleccion de capturas."""
		try:
			subprocess.check_call([REMOVE_COMMAND,self.getFullPathCaptura()])
			print "Borrada captura de disco! %s\n" % self.getFullPathCaptura()
			#subprocess.check_call([REMOVE_COMMAND,self.getFullPathCapturaConv()])
			#print "Borrada captura de disco! %s\n" % self.getFullPathCapturaConv()
		except Exception as e:
			err = "Error OS en borrar(%s)\n" % e
			print err
			controlador = App.get_running_app()
			controlador.mostrarDialogoMensaje(title='Error de conexion',
											text=err
											)
		finally:
			#print "Eliminando captura de memoria...\n"
			#colCaps.remove(self)
			c = itemFalla.getColCapturas()
			c.remove(self)
			itemFalla.setColCapturas(c)
			print "Mostrando la coleccion desde captura\n"
			self.mostrarCapturas(itemFalla.getColCapturas())

	def mostrarCapturas(self,colCaps):
		print "En mostrarCapturas()\n"
		for c in colCaps:
			print "captura asociada a la falla: %s \n" % c.getFullPathCaptura()
		print "Fin mostrarCapturas()\n"


