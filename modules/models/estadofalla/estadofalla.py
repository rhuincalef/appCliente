class Estado(object):
	def cambiar(self,fallaItem):
		fallaItem.setEstado(self)

	# self.estado.registrar(self,item_falla,capturador,cap)
	def registrar(self,item_falla,capturador,captura):
		raise Exception("Error este metodo debe implementarse en subclases")

	def mostrar_capturas_asociadas(self,falla):
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


class Informada(Estado):

	""" Estado para las fallas informadas se obtuvieron del servidor"""
	def __init__(self,idfalla,altura,calle):
		self.id = idfalla
		self.altura = altura
		self.calle = calle


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
		if falla is None:
			print "ItemFalla no encontrado: id= ",item_falla.getEstado().getId()
			fallas_totales.append(item_falla)
		else:
			col_falla = falla.getColCapturas()
			col_falla.append(captura)
			print "Encontrado item_falla (%s)" % item_falla.getEstado().getId()
			print ""
			#self.mostrar_capturas_asociadas(falla)

	def mostrar_capturas_asociadas(self,falla):
		print "Falla (%s) tiene las capturas:  " % falla.getEstado().getId() 
		for cap in falla.getColCapturas():
			print "Captura: nombreAchivo(%s) - dirLocal(%s) - formato(%s) - extension(%s)" %\
					(cap.getNombreArchivoCaptura(),cap.getDirLocal(),cap.getFormato(),cap.getExtension())
			print ""
		









