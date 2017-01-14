from constantes import *
import datetime
import time
class Estado(object):
	def cambiar(self,fallaItem):
		fallaItem.setEstado(self)

	# self.estado.registrar(self,item_falla,capturador,cap)
	def registrar(self,item_falla,capturador,captura):
		raise Exception("Error este metodo debe implementarse en subclases")

	def mostrar_capturas_asociadas(self,falla):
		raise Exception("Error este metodo debe implementarse en subclases")


	def completarDataFalla(self,api_client):
		raise Exception("Error este metodo debe implementarse en subclases")		


class Confirmada(Estado):
	""" Estado para las fallas que se capturaron sobre la calle"""
	
	def __init__(self,lat,lon):
		self.latitud = lat
		self.longitud = lon

	def getLatitud(self):
		return self.latitud

	def getLongitud(self):
		return self.longitud

	def __repr__(self):
		return "Confirmada; latitud: %s - longitud: %s " % \
			(self.latitud,self.longitud)


	# // Agrega la falla a Capturador.colCapturasTotales.
	def registrar(self,item_falla,capturador,captura):
		col_caps_item_falla = item_falla.getColCapturas()
		col_caps_item_falla.append(captura)
		col_capturas_realizadas = capturador.getColCapturasTotales()
		col_capturas_realizadas.append(item_falla)
		# Comentar despues esta linea!
		#self.mostrar_capturas_asociadas(item_falla)
	

	def mostrar_capturas_asociadas(self,falla):
		print "Falla (lat:%s,long:%s) tiene las capturas:  " %\
					(falla.getEstado().getLatitud(),falla.getEstado().getLongitud())
		for cap in falla.getColCapturas():
			print "Captura: nombreAchivo(%s) - dirLocal(%s) - formato(%s) - extension(%s)" %\
					(cap.getNombreArchivoCaptura(),cap.getDirLocal(),cap.getFormato(),cap.getExtension())
			print ""

	#TODO: TERMINAR!
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







