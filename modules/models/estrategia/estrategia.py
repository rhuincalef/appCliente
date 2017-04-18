# La estrategia se refiere a readaptar los ItemFalla nuevos e informados
# para subirlos al servidor, que cuenten con alguna captura asociada y,
# agregarlos a la colCapturasConfirmadas que mantiene el controlador.

from estadofalla import *

class Estrategia(object):
	def filtrar(self,colCapturasConfirmadas,colCapturasTotales,capturador):
		raise Exception("Error este metodo debe implementarse")



class EstrategiaConfirmados(Estrategia):

	#TODO: Verificar si se puede armar una clase "ColFallasInformadas"
	# que busque una falla dada su latitud y longitud!

	#Filtra solo las fallas nuevas que tienen al menos una captura asociada.
	def filtrar(self,colFallasConfirmadas,colFallasTotales,capturador):
		#Se recorren todas las fallas nuevas recolectadas y se agregan
		#solo aquellas que tienen alguna captura asociada a la colFallasConfirmadas.
		for i in xrange(0,len(colFallasTotales)):
			if len(colFallasTotales[i].getColCapturas()) > 0:
				#Se genera el idFalla negativo(valido solo para las fallasnuevas
				#capturadas en la calle)			
				idfalla = i * (-1)
				latitud = colFallasTotales[i].getEstado().getLatitud()
				longitud = colFallasTotales[i].getEstado().getLongitud()
				colFallasConfirmadas.append(colFallasTotales[i])

				#Se estima la calle y altura y se asigna a la falla actual.
				capturador.obtenerDirEstimada(colFallasTotales[i])
		
	# Retorna una tupla con (NOMBRE_CALLE,ALTURA) para mostrar en
	# subircapturasservidor.py
	def estimarCalleAltura(self,colCapturasConfirmadas,api_client):
		for falla in self.colCapturasConfirmadas:
		 	(calle,altura) = falla.estimarCalleAltura()
	


	#BACKUP!
	#def filtrar(self,colCapturasConfirmadas,colCapturasTotales):
	#	print "Inicio de estrategiaConfirmados.filtrar()"
		# Se cambia el estado de la falla a confirmada con
		# la calle y altura de la misma, obtenida a partir de la (latitud,longitud) 
	#	for falla in colCapturasTotales:
			# TODO: VER COMO CERRAR ESTO!
			# calle =  "Irigoyen"
			# altura = 200000
			# estado = Informada(idfalla,altura,calle)
		#	idfalla = 99
		#	altura = falla.getEstado().getLatitud()
		#	calle = falla.getEstado().getLongitud()
		#	falla.cambiarEstado(idfalla,altura,calle)
		#	colCapturasConfirmadas.append(falla)
		#	print ""
		#	print "Agregada falla confirmada"
		#	print "%s" % falla.getEstado()
		#	print "----------------------------------------"
		#print "Fin de filtrar!"


class EstrategiaInformados(Estrategia):

	def filtrar(self,colCapturasConfirmadas,colCapturasTotales,capturador):
		for falla in colCapturasTotales:
			if len(falla.getColCapturas()) > 0:
				colCapturasConfirmadas.append(falla)
		







