
from estadofalla import *
class Estrategia(object):
	def filtrar(self,colCapturasConfirmadas,colCapturasTotales):
		raise Exception("Error este metodo debe implementarse")



class EstrategiaConfirmados(Estrategia):

	def filtrar(self,colCapturasConfirmadas,colCapturasTotales):
		print "Inicio de estrategiaConfirmados.filtrar()"
		for falla in colCapturasTotales:
			# Se cambia el estado de la falla a confirmada con
			# la calle y altura de la misma, obtenida a partir de la (latitud,longitud) 
			# TODO: VER COMO CERRAR ESTO!
			# calle =  "Irigoyen"
			# altura = 200000
			# estado = Informada(idfalla,altura,calle)
			idfalla = 99
			altura = falla.getEstado().getLatitud()
			calle = falla.getEstado().getLongitud()
			falla.cambiarEstado(idfalla,altura,calle)
			colCapturasConfirmadas.append(falla)
			print ""
			print "Agregada falla confirmada"
			print "%s" % falla.getEstado()
			print "----------------------------------------"
		print "Fin de filtrar!"

class EstrategiaInformados(Estrategia):

	def filtrar(self,colCapturasConfirmadas,colCapturasTotales):
		print "Inicio de EstrategiaInformados.filtrar()"
		for falla in colCapturasTotales:
			colCapturasConfirmadas.append(falla)
			print "Agregada falla informada. id(%s) - calle(%s) - altura(%s)" % \
			(falla.getEstado().getId(),falla.getEstado().getCalle(),\
				falla.getEstado().getAltura())
			print ""
		print "Fin de filtrar!"







