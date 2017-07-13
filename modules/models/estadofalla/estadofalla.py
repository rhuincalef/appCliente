from constantes import *
import datetime
import time

from persistent import Persistent
#class Estado(object):
class Estado(Persistent):
	def cambiar(self,fallaItem):
		fallaItem.setEstado(self)

	# self.estado.registrar(self,item_falla,capturador,cap)
	def registrar(self,item_falla,capturador,captura):
		raise Exception("Error este metodo debe implementarse en subclases")

	def mostrar_capturas_asociadas(self,falla):
		raise Exception("Error este metodo debe implementarse en subclases")


	def completarDataFalla(self,api_client):
		raise Exception("Error este metodo debe implementarse en subclases")		

	# Retorna un listado ordenado con los atributos del itemFalla
	def getAttributos(self):
		raise Exception("Error este metodo se debe implementar en subclases")


	# Retorna un listado con los nombres de los atributos del dominio
	# que encapsula cada estado.
	def getNombreAtributos(self):
		atributos = [i for i in dir(self) if not inspect.ismethod(i) and not(i.startswith('__') and i.endswith('__') )]
		return atributos

	#Retorna el dicc de la falla codificado en utf-8
	def getDicFallaEncoded(self):
		raise Exception("Error este metodo se debe implementar en subclases")



class Confirmada(Estado):
	""" Estado para las fallas que se capturaron sobre la calle"""
	
	def __init__(self,lat,lon):
		self.id = "No asignado"
		self.latitud = lat
		self.longitud = lon
		self.calleEstimada = self.rangoEstimado1 = self.rangoEstimado2 = None
		self.tipoReparacion = self.tipoMaterial = self.tipoFalla = None


	def setCalleEstimada(self,c):
		self.calleEstimada = c
		
	def setRangosEstimados(self,rango1,rango2):
		self.rangoEstimado1 = rango1
		self.rangoEstimado2 = rango2


	def setTipoFalla(self,f):
		self.tipoFalla = f
		
	def setTipoReparacion(self,r):
		self.tipoReparacion = r

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

	#Backup!
	# // Agrega la falla a Capturador.colCapturasTotales.
	#def registrar(self,item_falla,capturador,captura):
	#	print "En capturador.registrar()...\n"
	#	col_caps_item_falla = item_falla.getColCapturas()
	#	col_caps_item_falla.append(captura)
	#	print "Appeandeada la captura!\n"
		#NOTA: Agrega el itemFalla actual a la col. de itemFalla del
		#capturador al que pertenece esta.
	#	col_item_falla_capturadas = capturador.getColCapturasTotales()
	#	col_item_falla_capturadas.append(item_falla)
		# Comentar despues esta linea!
	#	print "En estado.registrar()"
	#	self.mostrar_capturas_asociadas(item_falla)
	

	#NOTA: -Para las fallas nuevas, si estas no tienen al menos
	# una captura asociada se deben descartar de la colCapturas del 
	# capturador.
	# -Si es una falla informada, esta se conserva aun si no tiene
	# capturas asociadas.
	def registrar(self,item_falla,capturador,captura):
		print "En capturador.registrar()...\n"
		col_caps_item_falla = item_falla.getColCapturas()
		col_caps_item_falla.append(captura)
		print "Appeandeada la captura!\n"
		#NOTA: Agrega el itemFalla actual a la col. de itemFalla del
		#capturador al que pertenece esta.
		col_item_falla_capturadas = capturador.getColCapturasTotales()
		col_item_falla_capturadas.append(item_falla)
		# Comentar despues esta linea!
		print "En estado.registrar()"
		self.mostrar_capturas_asociadas(item_falla)
	


	def mostrar_capturas_asociadas(self,falla):
		print "Falla (lat:%s,long:%s) tiene las capturas:  " %\
					(falla.getEstado().getLatitud(),falla.getEstado().getLongitud())
		for cap in falla.getColCapturas():
			print "Captura: nombreAchivo(%s) - dirLocal(%s) - formato(%s) - extension(%s)" %\
					(cap.getFullPathCaptura(),cap.getDirLocal(),cap.getFormato(),cap.getExtension())
			print ""

	
	#Este metodo obtiene los datos necesarios para dar de alta la falla
	#(calle, altura, criticidad?,) con la lat. y long. obtenida del GPS y
	# retorna un dic con todos los datos.
	def completarDataFalla(self,api_client):
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


	# Retorna un listado ordenado con los atributos del itemFalla
	def getAttributos(self):
		calle = self.calleEstimada + "("+str(self.latitud)+")"
		#altura = str(self.alturaEstimada) + "("+str(self.longitud)+")" 
		altura = str(self.rangoEstimado1) + "-" + str(self.rangoEstimado2)\
						+ "("+str(self.longitud)+")" 
		return list([self.id, calle, altura ])
		#return list([self.id, self.latitud, self.longitud])


	#Retorna el dicc de la falla codificado en utf-8 para enviar al server
	def getDicFallaEncoded(self):
		print "En getDicFallaEncoded()...\n"
		print "TipoReparacion: %s\n" % self.tipoReparacion
		return {
			'id': str(self.id).encode("utf-8"),
			'latitud':str(self.latitud).encode("utf-8"),
			'longitud': str(self.longitud).encode("utf-8"),

			# Campos agregados para que el servidor los reciba
			# y registre una falla consistente en el sistema. 
			#'nombreTipoMaterial':str("Cemento").encode("utf-8"),
			#'nombreTipoFalla':str("Bache").encode("utf-8"),
			#'tipoReparacion': str("Cementar").encode("utf-8")
			'nombreTipoMaterial':str(self.tipoMaterial).encode("utf-8"),
			'nombreTipoFalla':str(self.tipoFalla).encode("utf-8"),
			'tipoReparacion':str(self.tipoReparacion),

			'nombreCriticidad':str("Media").encode("utf-8"),
			'observacion':str("Falla recolectada por personal de municipalidad en la calle").encode("utf-8"),
			'tipoEstado':str("Confirmado").encode("utf-8")
		}
		

class Informada(Estado):

	""" Estado para las fallas informadas se obtuvieron del servidor"""
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

	# // Recorre  CapturadorInformado.colCapturasTotales (de CapturadorInformadas),
	# // y actualiza  el listado de capturas de la falla en la lista.
	def registrar(self,item_falla,capturador,captura):
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
	
	#TODO: TERMINAR!
	# Este metodo solamente retorna un diccionario con la data 
	# de la falla existente en el servidor.		
	def completarDataFalla(self,api_client):
		respuesta = {}
		respuesta["id"] = self.id
		return respuesta		


	# Retorna un listado ordenado con los atributos del itemFalla
	def getAttributos(self):
		l = list([self.id, self.calle, self.altura])
		print "lista informado.getAttributos() es: %s\n" % l
		return l


	#Retorna el dicc de la falla codificado en utf-8 para enviar al server
	def getDicFallaEncoded(self):
		return {
			'id': str(self.id).encode("utf-8"),
			'calle':str(self.calle).encode("utf-8"),
			'altura': str(self.altura).encode("utf-8")
		}





