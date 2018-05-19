import json
from constantes import PATH_ARCH_UBICACIONES_FALSAS

#PATH_ARCH_UBICACIONES_FALSAS = "latitudesFalsas.json"

class ExcepcionArchCoordInvalido(Exception):
	pass


class JSONizable(object):
	def toJson(self):
		return self.__dict__


class CoordenadaFalsa(JSONizable):
	""" Clase que representa una coordenada falsa con nombre de calle, latitud y longitud. """

	def __init__(self,latitud,longitud,nombreCalle):
		self.latitud = latitud
		self.longitud = longitud
		self.nombreCalle = nombreCalle

	def getLatitud(self):
		return self.latitud

	def getLongitud(self):
		return self.longitud

	def getNombreCalle(self):
		return self.nombreCalle

	def __str__(self):
		return "{ nombreCalle: %s, latitud: %s,  longitud %s }\n" % \
					(self.nombreCalle, self.latitud, self.longitud)

class FakeGPS(JSONizable):
	""" Clase que simula ser un gps proporciona una secuencia circular de varias coordenadas GPS,
		partiendo de un JSON. Esto permite que las ubicaciones no se superpongan en
		el mapa si no se dispone de un gps para probarlas.

		Las latitudes y longitudes se encuentran en constantes.py en PATH_ARCH_UBICACIONES_FALSAS(latitudesFalsas.json por defecto),
		y este puede ser modificado para agregar o eliminar el listado de latitudes 
		que la clase simula proporcionar."""

	def __init__(self):
		self.posCoordenadaActual = 0
		self.colCoordenadas = []
		self.f = open(PATH_ARCH_UBICACIONES_FALSAS,"r") 

	def setColCoordenadas(self,col):
		self.colCoordenadas = col

	def instanciarCoordenadaFalsa(self,dicElem):
		""" Este metodo instancia un objeto coordenada falsa dado un elemento del diccionario"""
		#print "dicElem actual: %s\n" % dicElem
		if dicElem.has_key('latitud'):
			objeto = CoordenadaFalsa(
									dicElem['latitud'],
									dicElem['longitud'],
									dicElem['nombreCalle']
					)
			self.colCoordenadas.append(objeto)
			return objeto
		elif dicElem.has_key('posCoordenadaActual'):
			self.posCoordenadaActual = dicElem['posCoordenadaActual']
			return self
		else:
			raise ExcepcionArchCoordInvalido("Archivo de coordenadas invalido")

	def inicializarGPS(self):
		""" Inicializa el objeto FakeGPS cargando el json desde disco"""
		#f = open(PATH_ARCH_UBICACIONES_FALSAS,"rw")
		#Se adjunta un metodo de parseo de json personalizado.
		# json.load() carga primero los nodos del json mas anidados,
		# y luego los nodos mas externos.
		try:
			dicObj = json.load(self.f,object_hook = self.instanciarCoordenadaFalsa)
		except Exception as e:
			print "Error desconocido en fakegps: %s\n" % e.message
		finally:
			try:
				print "Cerrando la aplicacion...\n"
				sys.exit(1)
			except Exception as e:
				pass



	def getCoordenada(self):
		""" Obtiene la coordenada actual en la coleccion y aumenta 
			el indice de coordenada actual, para que en la proxima invocacion 
			se solicite la siguiente coordenada """
		
		coord = self.colCoordenadas[self.posCoordenadaActual]
		if self.llegoAFinCoordenadas():
			print "se llego a fin!\n"
			self.posCoordenadaActual = 0
		else:
			self.posCoordenadaActual = self.posCoordenadaActual + 1
		print "self.posCoordenadaActual: %s\n" % self.posCoordenadaActual
		print "\nretornando la siguiente coordenada: %s\n" % coord
		return coord

					
	def llegoAFinCoordenadas(self):
		""" Indica si se debe comenzar el conteo desde el inicio de la coleccion de coordenadas"""
		print "\nself.posCoordenadaActual + 1: %s\n" % (self.posCoordenadaActual + 1)
		print "len(self.colCoordenadas): %s\n" % len(self.colCoordenadas)

		if self.posCoordenadaActual + 1 >= len(self.colCoordenadas):
			return True
		return False

	def toJson(self):
		return {
				"posCoordenadaActual": self.posCoordenadaActual,
				"colCoordenadas": [ elem.toJson() for elem in self.colCoordenadas]
		}

	def persistirUbicaciones(self):
		print "fakegps.toJson(): %s\n" % self.toJson()
		self.f = open(PATH_ARCH_UBICACIONES_FALSAS,"w")
		json.dump(self.toJson(),self.f,indent=4)
		print "dumpeado objeto a archivo!\n"
