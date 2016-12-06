class Estado(object):
	def cambiar(self,fallaItem):
		fallaItem.setEstado(self)

	# self.estado.registrar(self,item_falla,capturador,cap)
	def registrar(self,item_falla,capturador,captura):
		raise Exception("Error este metodo debe implementarse en subclases")


class Confirmada(Estado):
	""" Estado para las fallas que se capturaron sobre la calle"""
	
	def __init__(self,lat,lon):
		self.latitud = lat
		self.longitud = lon

	# // Agrega la falla a Capturador.colCapturasTotales.
	def registrar(self,item_falla,capturador,captura):
		col_caps_item_falla = item_falla.getColCapturas()
		col_caps_item_falla.append(captura)
		col_capturas_realizadas = capturador.getColCapturasTotales()
		col_capturas_realizadas.append(item_falla)


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
		# Se obtienen las fallas agregadas a la colCapturasTotales()
		#  y si item_falla ya existe se le appendea la captura.
		# Si no existe, se agrega item_falla con la captura actual. 
		fallas_totales = capturador.getColCapturasTotales()
		falla = None
		for f in fallas_totales:
			if f.id == item_falla.id:
				falla = f
				break
		if falla is None:
			print "ItemFalla no encontrado: id= ",item_falla.id
			fallas_totales.append(captura)
		else:
			col_falla = falla.getColCapturas()
			col_falla.append(captura)
					









