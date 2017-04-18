from persistent import Persistent

class Captura(Persistent):
	def __init__(self,nombCap):
		self.nombre = nombCap
		self.extension = ".pcd"

	def __str__(self):
		return "{nombre: %s, extension: %s }, " % (self.nombre,self.extension)


class ItemFalla(Persistent):
  def __init__(self, is_selected=False, **kwargs):
    super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
    self.estado = None
    # Coleccion de objetos Captura
    self.colCapturas = []
    #NOTA: is_selected se modifica cuando el usuario selecciona una itemFalla para subir al servidor. 
    self.is_selected = False
    self.estaSubidaAlServidor = False # Flag que indica si se subio o no una falla
                                      # al servidor.


  def __str__(self):
  	cad = "-->{ 'estado': { %s }, 'capturas': [ %s ] }<--    " %\
  			(str(self.estado),self.colCapturas)
  	return cad

  def getEstado(self):
    return self.estado

  def setEstado(self,estado):
    self.estado = estado
    print "Cambiado el estado de la falla a : %s" % (estado)
    print ""
  
  def agregarCap(self,c):
    self.colCapturas.append(c)

  # Retorna la lista de capturas asociadas a una falla
  def getColCapturas(self):
    return self.colCapturas


