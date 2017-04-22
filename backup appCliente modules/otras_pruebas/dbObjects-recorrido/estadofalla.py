
from persistent import Persistent
class Estado(Persistent):

	def cambiar(self,fallaItem):
		fallaItem.setEstado(self)

class Informado(Estado):
	def __init__(self,id,calle,altura,*kwargs):
		self.id = id
		self.altura = altura
		self.calle= calle

	def __str__(self):
		return "'id': %s, 'calle': %s, 'altura': %s" %\
			(self.id,self.calle,self.altura)

class Confirmado(Estado):
	def __init__(self,lat,lng,*kwargs):
		self.latitud = lat
		self.longitud = lng	

	def __str__(self):
		return "'latitud': %s, 'longitud': %s " %\
			(self.latitud,self.longitud)


