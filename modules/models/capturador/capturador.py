
# +Capturador
# 		-ColCapturasTotales
# 		-ColCapturasConfirmadas(Capturas que se van a subir al servidor)
# 		-apiClient
# 		+filtrarCapturas(colCapturasTotales)
# 		+enviarCapturas(apiClient)

import sys,os
from apiclient1 import ApiClientApp,ExcepcionAjax
from kivy.adapters.models import SelectableDataItem
from constantes import *
from utils import mostrarDialogo
from captura import *

class Capturador(object):

  def __init__(self):
    self.colCapturasTotales = []
    self.colCapturasConfirmadas = []
    self.apiClient = ApiClientApp()
    print "Inicializado Capturador"

  # Retorna la cantidad de archivos que tienen un nombre dado
  # en el directorio de trabajo especificado. Se detecta la
  # extension desde la derecha del archivo.
  def getCantidadCapturas(self,archivo_a_buscar,dirTrabajo,extensionArchivo):
    dir_actual = os.getcwd()
    os.chdir(dirTrabajo)
    print "Cambiando a dirTrabajo: "+ dirTrabajo
    print ""
    contador_arch = 1
    plantilla_archivo = archivo_a_buscar + SUBFIJO + "%s" + extensionArchivo
    print "La plantilla de la captura es: " + plantilla_archivo
    print ""
    while os.path.exists( plantilla_archivo % contador_arch):
        contador_arch += 1
    print "Cantidad de archivos .pcd con el nombre ",archivo_a_buscar, "es : ",contador_arch
    print ""
    os.chdir(dir_actual)
    return contador_arch
    


  # Retorna la cantidad de archivos que tienen un nombre dado
  # en el directorio de trabajo especificado. Se detecta la
  # extension desde la derecha del archivo.
  # def getCantidadCapturas(archivo_a_buscar,dirTrabajo):
  #   cantActual = 0
  #   patron = NOMBRE_ARCHIVO + "[0-9]" + "\\" + EXTENSION_ARCHIVO
  #   print "El patron es: ", patron
  #   expr = re.compile(patron)
  #   #Obtiene una lista de nombres de archivos ordenada
  #   listado = sorted(os.listdir(dirTrabajo))
  #   print "listado -->"
  #   print listado
  #   print ""
  #   for file in listado:
  #       res = expr.search(file)
  #       print "examinando ",file
  #       if res != None:
  #         print "Archivo encontrado!"    
  #         #Si es un .pcd se
  #         index_extension = rfind(file,".pcd")
  #         cad_archivo = file[:index_extension]
  #         print "cad_archivo encontrado es: ",cad_archivo
  #         print "archivo_a_buscar encontrado es: ",archivo_a_buscar+ str(cantActual)
  #         if (archivo_a_buscar+ str(cantActual)) == cad_archivo:
  #           cantActual += 1
  #   print "Cantidad de archivos .pcd con el nombre ",archivo_a_buscar, "es : ",cantActual
  #   print ""
  #   #Se retorna el siguiente
  #   return cantActual



  def capturar(self,dataSensor, dir_trabajo, nombre_captura):
    # Se instancia la captura(con los valores de la view anterior),
    # se almacena en disco y se se agrega a la lista de capturas del 
    # capturador.
    cap = Captura(nombre_captura,dir_trabajo,FORMATO_CAPTURA, EXTENSION_ARCHIVO)
    cap.almacenar(dataSensor,self)
    # TODO: SI es necesario agregar aca la parte de asociar una falla con una captura.
    self.colCapturasTotales.append(cap)
    print "Captura realizada con exito!Agregada: ",str(cap)
    print ""



  # Filtra las colCapturasTotales y solamente deja en capturas
  def filtrarCapturas(self):
    pass

  def enviarCapturas(self):
    pass

# + Capturador > CapturadorInformado
# 		-ColBachesInformados (Se envian la calle y/o altura y envia los informados en ese rango)
# 		+solicitarInformados()


class ListadoFallas(list):  
  def __init__(self, *args):
    list.__init__(self, *args)

  def __contains__(self, item):
    for obj in self:
      if obj.id == item.id:
        return True
    return False

  def __repr__(self):
    cad = ""
    for o in self:
      cad += " - "+ str(o)
    return cad



class ItemFalla(SelectableDataItem):
  def __init__(self,id_falla,calle,altura, is_selected=False, **kwargs):
    super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
    self.id = id_falla
    self.calle = calle
    self.altura = altura
    self.is_selected = False

  def __cmp__(self,other):
    if self.id > other.id:
      return 0
    elif self.id == other.id:
      return 0
    else:
      return -1
  

class CapturadorInformados(Capturador):
  def __init__(self):
    super(CapturadorInformados,self).__init__()
    self.colBachesInformados = ListadoFallas()
    # self.colBachesInformados = []
    print "Inicializado CapturadorInformado"

  def getColBachesInformados(self):
    return self.colBachesInformados


  def inicializar_fallas(self):
    for obj in self.colBachesInformados:
      obj.is_selected = False
    print "ItemFallas inicializadas ..."


  #TODO: Este metodo debe agregar nuevos elementos a la colBachesInformados
  # sin repetir! 
  def solicitarInformados(self,calle):
    #TODO: Este diccionario se obtiene a partir del metodo de apiClient que realiza
    # las peticiones al servidor.
    # dic_json= {
    # "1":{ "id": 1,
    #     "calle": "Belgrano",
    #     "altura": 200},
    # "2":{ "id": 2,
    #     "calle": "Irigoyen",
    #     "altura": 200},
    # "3":{ "id": 3,
    #     "calle": "Ameguino",
    #     "altura": 200},
    # "4":{ "id": 4,
    #     "calle": "Pellegrini",
    #     "altura": 200},
    # "5":{ "id": 5,
    #     "calle": "9 de Julio",
    #     "altura": 200},
    # "6":{ "id": 6,
    #     "calle": "Aedo",
    #     "altura": 200},
    # "7":{ "id": 7,
    #     "calle": "Callao",
    #     "altura": 200}
    # }
    try:
      # Hace un GET al servidor para obtener todos los baches en una calle
      # Para probar esta parte ejecutar apiclient/servidor_json.py.
      dic_json = self.apiClient.getInformados(calle)

      for key,tupla in dic_json.iteritems():
          falla = ItemFalla(tupla["id"],tupla["calle"],tupla["altura"])
          if falla not in self.colBachesInformados:
            self.colBachesInformados.append(falla)

      self.colBachesInformados = sorted(self.colBachesInformados)
      self.inicializar_fallas()
      self.mostrar_coleccion()

    except ExcepcionAjax, e:
      mostrarDialogo(titulo="Error en solicitud al servidor",
                      content= e.message)

    return self.colBachesInformados

  def mostrar_coleccion(self):
    for obj in self.colBachesInformados:
      print "Id falla: ",obj.id,"; Calle:",obj.calle,"; Altura: ",obj.altura





