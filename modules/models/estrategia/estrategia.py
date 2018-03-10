from estadofalla import *

class Estrategia(object):
	"""La estrategia se refiere a readaptar los ItemFalla (confirmados e informados)
		para subirlos al servidor, que cuenten con alguna captura asociada y,
		agregarlos a la colCapturasConfirmadas que mantiene el controlador."""

	def filtrar(self,colCapturasConfirmadas,colCapturasTotales,capturador):
		raise Exception("Error este metodo debe implementarse")

class EstrategiaConfirmados(Estrategia):

	#Filtra solo las fallas nuevas que tienen al menos una captura asociada.
	def filtrar(self,colFallasConfirmadas,colFallasTotales,capturador):
		#Se recorren todas las fallas nuevas recolectadas y se agregan
		#solo aquellas que tienen alguna captura asociada a la colFallasConfirmadas.
		for i in xrange(0,len(colFallasTotales)):
			if len(colFallasTotales[i].getColCapturas()) > 0:
				#Se estima la calle y altura y se asigna a la falla actual.
				capturador.obtenerDirEstimada(colFallasTotales[i])
				colFallasConfirmadas.append(colFallasTotales[i])
				
	
	def estimarCalleAltura(self,colCapturasConfirmadas,api_client):
		"""Retorna una tupla con (nombre_calle,altura) para mostrar en
			la pantalla donde se seleccionan las fallas para subir al servidor. """
		for falla in self.colCapturasConfirmadas:
		 	(calle,altura) = falla.estimarCalleAltura()
	
class EstrategiaInformados(Estrategia):

	def filtrar(self,colCapturasConfirmadas,colCapturasTotales,capturador):
		for falla in colCapturasTotales:
			if len(falla.getColCapturas()) > 0:
				colCapturasConfirmadas.append(falla)
