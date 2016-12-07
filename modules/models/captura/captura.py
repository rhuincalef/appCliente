# +Captura
# 		-NombreCaptura
# 		-DirLocal
# 		-Formato
# 		+convertir() //Se utilizara json para el envio al servidor.

import pcl
from constantes import *

class Captura(object):
	def __init__(self,nombre,dirLocal,formatoArchivo,extensionArchivo):
		self.nombreCaptura = nombre
		self.dirLocal = dirLocal
		self.formato = formatoArchivo
		self.extension = extensionArchivo
		self.colCapturas = []
		self.nombreArchivoCaptura = None

	

	def getNombreArchivo(self):
		return self.nombreCaptura

	def getNombreArchivoCaptura(self):
		return self.nombreArchivoCaptura

	def getDirLocal(self):
		return self.dirLocal

	def getFormato(self):
		return self.formato

	def getExtension(self):
		return self.extension


	def __repr__(self):
		return "Captura:" + str(self.dirLocal)+str(self.dirLocal)

	#Conversion a json para enviar al servidor
	def convertir(self):
		pass
		# self.almacenarLocalmente()

	# Usado por convertir(). Almacena el .pcd en disco.
	def almacenarLocalmente(self,data,capturador):
		p = pcl.PointCloud(data)
		# Se obtiene la cantidad de archivos con un nombre dentro
		# en un dir. de prueba dado
		try:
		  cant_archivos_actuales = capturador.getCantidadCapturas(self.nombreCaptura,
		                                                self.dirLocal,self.extension)
		  archivo_salida = self.nombreCaptura + SUBFIJO + str(cant_archivos_actuales) \
		                    + self.extension
		  pcl.save(p, archivo_salida)
		  self.nombreArchivoCaptura = archivo_salida
		  return archivo_salida
		except OSError as e:
		  print "Error al listar archivos en directorio ",DIR_TRABAJO_PRUEBA
		  sys.exit(1)


	# Descarta las capturas que no se confirmaron.
	def descartar(self):
		pass




		