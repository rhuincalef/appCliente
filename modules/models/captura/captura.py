# +Captura
# 		-NombreCaptura
# 		-DirLocal
# 		-Formato
# 		+convertir() //Se utilizara json para el envio al servidor.


#import pcl
import pypcd
import numpy as np
from constantes import *
#from utils import generarDataCsv,REMOVE_COMMAND
#from utils import REMOVE_COMMAND
import os
from os import path
import subprocess
from subprocess import CalledProcessError
import threading
import sys

from constantes import EXTENSION_SUBIDA_SERVER_DEFAULT
from constantes import CSV_TMP_DIR

import utils
from utils import *

from persistent import Persistent
#class Captura(object):
class Captura(Persistent):
	def __init__(self,nombre,dirLocal,formatoArchivo,extensionArchivo):
		self.nombreCaptura = nombre
		self.dirLocal = dirLocal
		self.formato = formatoArchivo
		self.extension = extensionArchivo
		self.nombreArchivoCaptura = None
		self.estaSubidaAlServidor = False # determina si una captura se subio
										#completamente al servidor.


	#Retorna el nombre del archivo+SUBFIJO+ID_INCREMENTAL+".csv"
	def getNombreCapturaConvertida(self):
		archivo_csv_salida = os.path.splitext(self.nombreArchivoCaptura)[0] 
		return archivo_csv_salida + EXTENSION_SUBIDA_SERVER_DEFAULT


	#Retorna la ruta completa al archivo .csv convertido asociado a la captura
	def getFullPathCapturaConv(self):
		return self.dirLocal + path.sep + CSV_TMP_DIR + self.getNombreCapturaConvertida() 


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


	def __repr__(self):
		return "Captura: nombreArchivoCaptura=%s , dirLocal = %s , nombreCaptura= %s;\n" %\
					(self.nombreArchivoCaptura,self.dirLocal,self.nombreCaptura)

	#Usado para el almacenamiento en formato json
	def __str__(self):
		cadena = ""
		if self.nombreArchivoCaptura is not None:
			cadena = self.nombreArchivoCaptura
		return cadena

	#Conversion a de los archivos .pcd a csv para enviar dentro del json de la falla
	def convertir(self):
		#os.path.splitext() divide el nombre de un archivo de la extension del mismo.
		archivo_csv_salida = os.path.splitext(self.nombreArchivoCaptura)[0] 
		nombreArchCsvNube = utils.generarDataCsv(self.nombreArchivoCaptura,
									self.dirLocal,archivo_csv_salida)
		return nombreArchCsvNube


	# Usado por capturador.registrarCaptura(). Almacena el .pcd en disco.
	#def almacenarLocalmente(self,data1,capturador, modo = PCD_XYZ_FORMAT):
	def almacenarLocalmente(self,data1,capturador,modo):
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
		  #print "El path_out generado para captura es: %s\n" % path_out
		  pc.save_pcd(path_out)
		  #print "Salvada captura XYZ! en: %s\n" % path_out
		  self.nombreArchivoCaptura = archivo_salida
		  return archivo_salida
		except OSError as e:
		  print "Error al listar archivos en directorio %s \n" % self.dirLocal
		  print "OSError: %s\n" % e 
		  sys.exit(1)


	# Descarta la captura de disco,borrando el .pcd y .csv y, borrandose
	# de la coleccion de capturas
	# captura.descartar()
	def descartar(self,colCaps):
		try:
			subprocess.check_call([REMOVE_COMMAND,self.getFullPathCaptura()])
			subprocess.check_call([REMOVE_COMMAND,self.getFullPathCapturaConv()])
			print "Borrada captura de disco! %s\n" % self.getFullPathCaptura()
			print "Borrada captura de disco! %s\n" % self.getFullPathCapturaConv()
		except Exception as e:
			err = "Error OS en borrar(%s)\n" % e
			print err
			controlador = App.get_running_app()
			controlador.mostrarDialogoMensaje(title='Error de conexion',
											text=err
											)
		finally:
			print "Eliminando captura de memoria...\n"
			colCaps.remove(self)
			print "Mostrando la coleccion desde captura\n"
			self.mostrarCapturas(colCaps)

	def mostrarCapturas(self,colCaps):
		print "En mostrarCapturas()\n"
		for c in colCaps:
			print "captura asociada a la falla: %s \n" % c.getFullPathCaptura()
		print "Fin mostrarCapturas()\n"


