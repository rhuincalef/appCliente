from constantes import *
import sys,serial
from serial import SerialException
import time
import string

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


class GeofencingAPI(object):
	""" API para obtener la calle y altura de una falla confirmada,
		dada su latitud y longitud. """

	def __init__(self):
		self.gps = serial.Serial(DEVICE_GPS_DEFAULT, 9600, timeout=1)
		print "Instanciado GPS!"
		self.bd_json = BDLocal()
		print "Fin constructor GeofencingAPI!"

	def obtenerCalle(self,latitud,longitud):
		pass

	def obtenerAltura(self,latitud,longitud):
		pass

	# TODO: Obtiene la latidud y longitud del GPS.
	def getLatLong(self):
		return (LAT_PRUEBA,LONG_PRUEBA)

	#Obtiene la latidud y longitud para una captura y lo alamcena
	# en la BD local junto con el nombre de la captura.
	def obtenerLatitudLongitud(self,nombre_archivo="test_file_default.pcd"):
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
			#self.bd_json.agregar(latitude,longitude,nombre_archivo)		
		return (latitude,longitude)


	def almacenarCapturaLocal(self,lat,long,nombre_archivo):
		print "En alamcenarCapturaLocal() ..."
		self.bd_json.agregar(lat,long,nombre_archivo)


# Clase que almacena en una TinyBD la latidud, longitud,
# y el nombre del archivo de captura .pcd.
# https://tinydb.readthedocs.io/en/latest/getting-started.html#basic-usage
#
from tinydb import TinyDB, Query
class BDLocal(object):

	def __init__(self):
		self.bd_json = TinyDB(LOCAL_DB_JSON_NAME)
		print "Abriendo BD json local..."

	def agregar(self,latitud,longitud,nombrePcd):
		my_dic = {
				"latitud": latitud,
				"longitud": longitud,
				"nombrePcd": nombrePcd}
		self.bd_json.insert(my_dic)
		print "BD actualizada con elementos: "
		print self.bd_json.all()
		print "-----------------------------------------------------"



#if __name__ == '__main__':
#	g = GeofencingAPI()
#	lat,longitud = g.obtenerLatitudLongitud()
#	print "Latitud leida: %s ; Longitud leida: %s\n" % (lat,longitud)
#	print "----------------------------------------------------\n"

