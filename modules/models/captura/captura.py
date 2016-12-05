# +Captura
# 		-NombreCaptura
# 		-DirLocal
# 		-Formato
# 		+convertir() //Se utilizara json para el envio al servidor.

import pcl
from constantes import *

class Captura(object):
	def __init__(self,nombre,dirLocal,formatoArchivo):
		self.nombreCaptura = nombre
		self.dirLocal = dirLocal
		self.formato = formatoArchivo 

	def __repr__(self):
		return "Captura:" + str(self.dirLocal)+str(self.dirLocal)

	#Conversion a json para enviar al servidor
	def convertir(self):
		pass
		# self.almacenar()

	# Usado por convertir(). Almacena el .pcd en disco.
	def almacenar(self,capturador):
		p = pcl.PointCloud(data)
		# Se obtiene la cantidad de archivos con un nombre dentro
		# en un dir. de prueba dado
		try:
		  cant_archivos_actuales = capturador.getCantidadCapturas(NOMBRE_ARCHIVO,
		                                                DIR_TRABAJO_PRUEBA)
		  archivo_salida = NOMBRE_ARCHIVO + str(cant_archivos_actuales) \
		                    + EXTENSION_ARCHIVO
		  pcl.save(p, archivo_salida)
		  print "Archivo "+ archivo_salida +" guardado!"
		  print ""
		except OSError as e:
		  print "Error al listar archivos en directorio ",DIR_TRABAJO_PRUEBA
		  sys.exit(1)


	# Descarta las capturas que no se confirmaron.
	def descartar(self):
		pass




		
