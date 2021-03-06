from kivy.app import App
import argparse

from constantes import *
import sys,serial
from serial import SerialException
import time
import string

import gps

#MODIFICADO ACA!!!
#from utils import mostrarDialogo

# Tutoriales compartir GPS con USB
# http://www.jillybunch.com/sharegps/user.html
# http://www.jillybunch.com/sharegps/nmea-bluetooth-linux.html

#http://www.jillybunch.com/sharegps/nmea-usb-linux.html

# sudo python geo.py /dev/rfcomm1 ./gps.kml 


#REMOVER LAS CONSTANTES DE ACA PARA PROBAR EL PROGRAMA COMPLETO!!
#LOCAL_DB_JSON_NAME = './DB_MUESTRAS_LOCALES.json'
#Tiempo maximo de espera en segundos para obtener una latitud y longitud
#MAX_TIMEOUT_SEGS = 10
#INVALID_LAT_LONG = -1
#DEVICE_GPS_DEFAULT = "/dev/rfcomm1"


class GeofencingAPI1(object):
	"""API para obtener la calle y altura de una falla confirmada,
		dada su latitud y longitud. """

	def __init__(self):
		self.gps = None
		try:
			self.gps = serial.Serial(DEVICE_GPS_DEFAULT, 9600, timeout=1)
			print "Instanciado GPS!\n"
		except SerialException as e:
			controlador = App.get_running_app()
			controlador.mostrarDialogoMensaje(title='Error de GPS',
										text="Dispositivo GPS no detectado!"
										)
			print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			print "+++++++++++++++++++++++++++ Error dispositivo GPS no detectado! ++++++++++++++++++++++++++"
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		self.bd_json = BDLocal()
		print "Fin constructor GeofencingAPI!"

	def obtenerCalle(self,latitud,longitud):
		pass

	def obtenerAltura(self,latitud,longitud):
		pass

	def getLatLong(self):
		"""Obtiene la latidud y longitud ficticias de un objeto FakeGPS que simula
			obtener distintas ubicaciones falsas."""
		#Se obtiene la siguiente coordenada del objeto FakeGPS y se sobreescribe el json
		# con las ubicaciones para mantener la coordenada actual entre varias ejecuciones de 
		# appCliente. 	
		coord = self.fakeGPS.getCoordenada()
		self.fakeGPS.persistirUbicaciones()
		print "retornando coordenada calle: %s\n" % coord.getNombreCalle() 
		return coord.getLatitud(),coord.getLongitud()


	def obtenerLatitudLongitud(self,nombre_archivo="test_file_default.pcd"):
		"""Obtiene la latitud y longitud para una captura y lo alamcena
			en la BD local junto con el nombre de la captura."""
		t1 = time.time()
		latitude = longitude = INVALID_LAT_LONG
		estanObtenidas = False
		print "En obtenerLatitudLongitud() con nombre_archivo: %s" % nombre_archivo
		print ""
		#Se prueba obtener la lat. y long por una cant. de segundos.
		try:
			while 1:
				latitude = longitude = INVALID_LAT_LONG
				line = self.gps.readline()
				datablock = line.split(',')
				if line[0:6] == '$GPRMC':
					print "datablock tiene:\n %s\n" % datablock
					latitude = string.atof(datablock[3])
					longitude = string.atof(datablock[5])
					if latitude != None and longitude != None:
						print "Latitud y longitud obtenidas!!!"
						estanObtenidas = True
						break
					t2 = time.time()
					tiempo_transcurrido = t2-t1
					print "Tiempo transcurrido: %s seg." % tiempo_transcurrido
					print ""
					if tiempo_transcurrido >= MAX_TIMEOUT_SEGS:
						print "Espera sin conseguir lat y longitud: %s" % (t2-t1)
						break
					t1 = t2
		except SerialException as se:
			print "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			print "++++++++++++ Error ubicacion en GPS no disponible(Dispositivo GPS no conectado). ++++++++++++"
			print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

		except Exception as se:
			print "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			print "++++++++++++ Error ubicacion en GPS no disponible(Excepcion interna). ++++++++++++"
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		finally:
			if not estanObtenidas:
				print "No se pudieron obtener las coordenadas!\n"
		return (latitude,longitude)


from tinydb import TinyDB, Query
from fakegps import *

class GeofencingAPI(object):
	""" API para obtener la calle y altura de una falla confirmada,
		dada su latitud y longitud. """

	def __init__(self):
		controlador = App.get_running_app()
		self.fakeGPS = FakeGPS()
		self.fakeGPS.inicializarGPS()
		# Si no es el gps real no se accede al dispositivo y se inicializa
		# solo la BD de coordenadas
		if (controlador is not None) and ( not (controlador.args.gps == OPCIONES_GPS[0]) ):
			self.session = gps.gps()
			self.session.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)

	def obtenerLatitudLongitud(self,nombre_archivo="test_file_default.pcd"):
		"""Obtiene la latidud y longitud reales desde el dispositivo GPS."""
		t1 = time.time()
		latitude = longitude = INVALID_LAT_LONG
		estanObtenidas = False
		tiempo_transcurrido = 0
		print "En obtenerLatitudLongitud() con nombre_archivo: %s" % nombre_archivo
		print ""
		#Se prueba obtener la lat. y long por una cant. de segundos.
		while 1:
			latitude = longitude = INVALID_LAT_LONG
			report = self.session.next()
			print report
			if report['class'] == 'TPV':
				#if not 'lat' in gpsd_report.keys():
				#        continue
				latitude =  report['lat']
				longitude = report['lon']
				t2 = time.time()
				tiempo_transcurrido += t2-t1
				print "Tiempo transcurrido: %s seg." % tiempo_transcurrido
				print ""
				if tiempo_transcurrido >= MAX_TIMEOUT_SEGS:
					print "Espera sin conseguir lat y longitud: %s" % (t2-t1)
					break
				t1 = t2
		return (latitude,longitude)

	def getLatLong(self):
		"""Obtiene la latidud y longitud ficticias de un objeto FakeGPS que simula
			obtener distintas ubicaciones falsas."""
		#Se obtiene la siguiente coordenada del objeto FakeGPS y se sobreescribe el json
		# con las ubicaciones para mantener la coordenada actual entre varias ejecuciones de 
		# appCliente. 	
		coord = self.fakeGPS.getCoordenada()
		self.fakeGPS.persistirUbicaciones()
		print "retornando coordenada calle: %s\n" % coord.getNombreCalle() 
		return coord.getLatitud(),coord.getLongitud()


class BDLocal(object):
	"""Base de datos de debugging para asociar los archivos .pcd, latitud y longitud y
		fecha de captura de las mismas."""

	def __init__(self,fullPathBD=None):
		controlador = App.get_running_app()
		self.rutaBDLocal = self.bd_json = None
		if fullPathBD is not None:
			self.bd_json = TinyDB(fullPathBD)
			self.rutaBDLocal = fullPathBD
		print "BDLocal en json tiene: %s\n" % self.bd_json


	def inicializar(self,fullPathBD = None ):
		"""Inicializa una BD Local con una fecha dada. Si no se especifica nada
			se considera por defecto la fecha actual. """
		if fullPathBD is not None:
			self.bd_json = TinyDB(fullPathBD)
			self.rutaBDLocal = fullPathBD
			print "Inicializada con path del usuario: %s...\n" % fullPathBD
			return

		fechaBDActual = time.strftime("%d-%m-%Y")
		bdPath = LOCAL_DB_JSON_NAME + fechaBDActual +\
						EXTENSION_LOCAL_BD_JSON_NAME
		self.bd_json = TinyDB(bdPath)
		self.rutaBDLocal = bdPath
		print "Inicializada por Defecto BD Local de muestras...\n"

	def estaInicializada(self):
		"""Retorna True si la BD se encuentra inicializada con una instancia a TinyDB."""
		return self.bd_json is not None

	def getNombreBDLocal(self):
		"""Retorna el nombre de archivo de la BD Muestras Locales."""
		nombreArch = ""
		if self.estaInicializada():
			print "En getNombreBDLocal() con self.rutaBDLocal: %s\n" % self.rutaBDLocal
			nombreArch = path.basename(self.rutaBDLocal)
		return nombreArch

	def agregar(self,latitud,longitud,nombrePcd):
		my_dic = {
				"latitud": latitud,
				"longitud": longitud,
				"nombrePcd": nombrePcd}
		self.bd_json.insert(my_dic)
		print "BD actualizada con elementos: "
		print self.bd_json.all()
		print "-----------------------------------------------------"
