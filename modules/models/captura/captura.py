# +Captura
# 		-NombreCaptura
# 		-DirLocal
# 		-Formato
# 		+convertir() //Se utilizara json para el envio al servidor.

class Captura(object):
	def __init__(self,nombre,dirLocal,formatoArchivo):
		self.nombreCaptura = nombre 
		self.dirLocal = dirLocal 
		self.formato = formatoArchivo 

	#Conversion a json para enviar al servidor
	def convertir(self):
		pass


		
