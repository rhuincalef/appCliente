from constantes import *
import datetime
import time
from persistent import Persistent

class Estado(Persistent):
	"""Clase base que encapsula el comportamiento asociado con el estado de una falla.
		 Puede ser Informada o Confirmada."""
	
	def cambiar(self,fallaItem):
		fallaItem.setEstado(self)

	def registrar(self,item_falla,capturador,captura):
		raise Exception("Error este metodo debe implementarse en subclases")

	def mostrar_capturas_asociadas(self,falla):
		raise Exception("Error este metodo debe implementarse en subclases")

	def completarDataFalla(self,api_client):
		raise Exception("Error este metodo debe implementarse en subclases")		
	
	def getAttributos(self):
		"""Retorna un listado ordenado con los atributos del itemFalla."""
		raise Exception("Error este metodo se debe implementar en subclases")

	def getNombreAtributos(self):
		"""Retorna un listado con los nombres de los atributos del dominio
			que encapsula cada estado."""
		atributos = [i for i in dir(self) if not inspect.ismethod(i) and not(i.startswith('__') and i.endswith('__') )]
		return atributos

	def getDicFallaEncoded(self):
		"""Retorna el diccionario de la falla codificado en utf-8."""
		raise Exception("Error este metodo se debe implementar en subclases")

	def comparar(self,other):
		raise Exception("Error este metodo se debe implementar en subclases")
		

class Confirmada(Estado):
	""" Estado para las fallas que se capturaron sobre la calle"""
	
	def __init__(self,lat,lon):
		self.id = "No asignado"
		self.latitud = lat
		self.longitud = lon
		self.calleEstimada = self.rangoEstimado1 = self.rangoEstimado2 = None
		self.criticidad = self.tipoMaterial = self.tipoFalla = None
		
	def setCalleEstimada(self,c):
		self.calleEstimada = c
		
	def setRangosEstimados(self,rango1,rango2):
		self.rangoEstimado1 = rango1
		self.rangoEstimado2 = rango2

	def setTipoFalla(self,f):
		self.tipoFalla = f
		
	def setCriticidad(self,c):
		self.criticidad = c

	def setTipoMaterial(self,m):
		self.tipoMaterial = m

	def getId(self):
		return self.id

	def getLatitud(self):
		return self.latitud

	def getLongitud(self):
		return self.longitud

	def __repr__(self):
		return "Confirmada; latitud: %s - longitud: %s " % \
			(self.latitud,self.longitud)

	#NOTA: -Para las fallas nuevas, si estas no tienen al menos
	# una captura asociada se deben descartar de la colCapturas del 
	# capturador.
	# -Si es una falla informada, esta se conserva aun si no tiene
	# capturas asociadas.
	def registrar(self,item_falla,capturador,captura):
		"""Agrega una captura a un elemento ItemFalla y agrega la falla 
			la coleccion de fallas del capturador."""
		print "En capturador.registrar()...\n"
		col_caps_item_falla = item_falla.getColCapturas()
		col_caps_item_falla.append(captura)
		print "Appeandeada la captura!\n"
		#NOTA: Agrega el itemFalla actual a la col. de itemFalla del
		#capturador al que pertenece esta.
		col_item_falla_capturadas = capturador.getColCapturasTotales()
		col_item_falla_capturadas.append(item_falla)
		print "En estado.registrar()"
		self.mostrar_capturas_asociadas(item_falla)
	
	def mostrar_capturas_asociadas(self,falla):
		print "Falla (lat:%s,long:%s) tiene las capturas:  " %\
					(falla.getEstado().getLatitud(),falla.getEstado().getLongitud())
		for cap in falla.getColCapturas():
			print "Captura: nombreAchivo(%s) - dirLocal(%s) - formato(%s) - extension(%s)" %\
					(cap.getFullPathCaptura(),cap.getDirLocal(),cap.getFormato(),cap.getExtension())
			print ""

	def completarDataFalla(self,api_client):
		"""Este metodo obtiene los datos necesarios para dar de alta la falla
		   con la latitud y longitud obtenida del GPS y retorna un diccionario
		   con todos los datos."""
		dir_data = self.api_client.obtenerDirServidor(self.latitud,
													self.longitud)
		respuesta = {}
		respuesta["id"] = self.id
		respuesta["calle"] = dir_data["calle"]
		respuesta["altura"] = dir_data["altura"]
		respuesta["idTipoMaterial"] = ID_TIPO_MATERIAL_DEFECTO
		respuesta["idTipoFalla"] = ID_TIPO_FALLA_DEFECTO
		#Fecha requerido por FallaEstadoModelo
		respuesta["fecha"] = fecha_string
		#Campos para establecer el estado de la falla en el
		# server como confirmada (FallaEstadoModelo)
		respuesta["idTipoEstado"] = ID_TIPO_ESTADO_CONFIRMADO
		respuesta["idUsuario"] = ID_USUARIO_CALLEJERO
		marcatiempo = time.time()
		fecha_string = datetime.datetime.fromtimestamp(marcatiempo).strftime('%Y-%m-%d %H:%M:%S')
		return respuesta

	# Confirmada.getAttributos()
	def getAttributos(self):
		"""Retorna un listado ordenado con los atributos del itemFalla."""
		calle = self.calleEstimada + "("+str(self.latitud)+")"

		rangoEstimado1 = rangoEstimado2 = DIRECCION_PHP_DIRECCION_NO_RETORNADA
		#Se verifica si alguna de las dos no se obtuvo
		if self.rangoEstimado1 != DIRECCION_PHP_DIRECCION_NO_RETORNADA:
			rangoEstimado1 = self.rangoEstimado1

		if self.rangoEstimado2 != DIRECCION_PHP_DIRECCION_NO_RETORNADA:
			rangoEstimado2 = self.rangoEstimado2

		#Se reemplaza el valor de una por el de otra, si alguna de las dos dirs 
		#se pudo obtener pero la otra no.
		if (rangoEstimado1 == DIRECCION_PHP_DIRECCION_NO_RETORNADA) and \
					(rangoEstimado2 != DIRECCION_PHP_DIRECCION_NO_RETORNADA):
			rangoEstimado1 = rangoEstimado2
		elif (rangoEstimado2 == DIRECCION_PHP_DIRECCION_NO_RETORNADA) and \
					(rangoEstimado1 != DIRECCION_PHP_DIRECCION_NO_RETORNADA):
			rangoEstimado2 = rangoEstimado1

		#Si ninguna se pudo obtener se reemplaza por el caracter "-"
		if rangoEstimado1 == DIRECCION_PHP_DIRECCION_NO_RETORNADA and \
				rangoEstimado2 == DIRECCION_PHP_DIRECCION_NO_RETORNADA:
			rangoEstimado1 = rangoEstimado2 = "-"
		  	  
		altura = str(rangoEstimado1) + "-" + str(rangoEstimado2)\
						+ "("+str(self.longitud)+")" 
		return list([self.id, calle, altura ])

	
	def getDicFallaEncoded(self):
		"""Retorna el diccionario de la falla codificado en utf-8 para enviar al servidor."""
		print "En getDicFallaEncoded()...\n"
		print "Criticidad: %s\n" % self.criticidad
		return {
			'id': str(self.id).encode("utf-8"),
			'latitud':str(self.latitud).encode("utf-8"),
			'longitud': str(self.longitud).encode("utf-8"),
			# Campos agregados para que el servidor los reciba
			# y registre una falla consistente en el sistema.
			'nombreTipoMaterial':str(self.tipoMaterial),
			'nombreTipoFalla':str(self.tipoFalla).encode("utf-8"),
			'nombreCriticidad':str(self.criticidad).encode("utf-8"),
			'observacion':str("Falla recolectada por personal de municipalidad en la calle").encode("utf-8"),
			'tipoEstado':str(ESTADO_POR_DEFAULT_SUBIDA_CAPTURAS).encode("utf-8")
		}
		
	#Confirmada.comparar()
	def comparar(self,other):
		print "En __cmp__() estado Confirmada con self.latitud: %s y self.longitud: %s\n" % (self.latitud,
																					self.longitud)
		if (self.latitud > other.getEstado().getLatitud()) and \
				(self.longitud > other.getEstado().getLongitud()):
			return 1
		elif (self.latitud == other.getEstado().getLatitud()) and \
				(self.longitud == other.getEstado().getLongitud()):
			return 0
		else:
			return -1

class Informada(Estado):
	""" Estado para las fallas informadas que se obtuvieron desde la aplicacion web."""

	def __init__(self,idfalla,altura,calle):
		self.id = idfalla
		self.altura = altura
		self.calle = calle

	def __repr__(self):
		return "Informada; id: %s - calle: %s - altura: %s " % \
			(self.id,self.calle,self.altura)

	def getId(self):
		return self.id

	def getAltura(self):
		return self.altura

	def getCalle(self):
		return self.calle

	def registrar(self,item_falla,capturador,captura):
		"""Recorre  CapturadorInformado.colCapturasTotales (de CapturadorInformadas),
			y actualiza  el listado de capturas de la falla en la lista."""

		# Se obtienen las fallas agregadas a capturadorInformadas.colCapturasTotales()
		# si item_falla ya existe se le appendea la captura, sino
		# se agrega item_falla con la captura actual seteada. 
		print "En registrar fallaInformada!"
		print "item_falla: %s" % type(item_falla)
		print "capturador: %s" % type(capturador)
		print "captura: %s" % type(captura)
		fallas_totales = capturador.getColCapturasTotales()
		falla = None
		for f in fallas_totales:
			f_id = f.getEstado().getId()
			item_falla_id = item_falla.getEstado().getId()
			print "Comparando item_falla_id(%s) vs f_id(%s)" % (item_falla_id,f_id)
			print ""
			if f_id == item_falla_id:
				falla = f
				break

		# Si no existe la falla se agrega a la coleccion de fallas totales del 
		# capturador, y se le agrega la captura. Si existe, simplemente se 
		# le agrega la captura a su coleccion de capturas.
		if falla is None:
			print "ItemFalla no encontrado: id= ",item_falla.getEstado().getId()
			fallas_totales.append(item_falla)
		else:
			print "Encontrado item_falla (%s)" % item_falla.getEstado().getId()
			print ""

		col_falla = item_falla.getColCapturas()
		col_falla.append(captura)
		print "Agregada captura a falla!"
		self.mostrar_capturas_asociadas(item_falla)

	def mostrar_capturas_asociadas(self,falla):
		print "Falla (%s) tiene las capturas:  " % falla.getEstado().getId() 
		if len(falla.getColCapturas()) > 0:
			print "Item_falla no tiene capturas!!!!"
		else:
			print "Item_falla agregado con capturas!"
			for cap in falla.getColCapturas():
				print "Captura: nombreAchivo(%s) - dirLocal(%s) - formato(%s) - extension(%s)" %\
						(cap.getNombreArchivoCaptura(),cap.getDirLocal(),cap.getFormato(),cap.getExtension())
				print ""
	
	def completarDataFalla(self,api_client):
		"""Este metodo solamente retorna un diccionario con la data 
			de la falla existente en el servidor. """
		respuesta = {}
		respuesta["id"] = self.id
		return respuesta		

	# Informada.getAttributos()
	def getAttributos(self):
		"""Retorna un listado ordenado con los atributos del itemFalla."""
		l = list([self.id, self.calle, self.altura])
		print "lista informado.getAttributos() es: %s\n" % l
		return l

	def getDicFallaEncoded(self):
		"""Retorna el diccionario de la falla codificado en utf-8 para enviar al server."""
		return {
			'id': str(self.id).encode("utf-8"),
			'calle':str(self.calle).encode("utf-8"),
			'altura': str(self.altura).encode("utf-8")
		}

	#Informada.comparar()
	def comparar(self,other):
		self_id = self.getId()  
		other_id = other.getEstado().getId()
		print "En __cmp__() estado Informada con self_id: %s y other_id: %s\n" % (self_id,other_id)
		if self_id > other_id:
			return 1
		elif self_id == other_id:
			return 0
		else:
			return -1
