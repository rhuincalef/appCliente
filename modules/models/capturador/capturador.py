
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
from estadofalla import *
from geofencing import *
from estrategia import *

from json import JSONEncoder


class ListadoFallas(list):  
  def __init__(self, *args):
    list.__init__(self, *args)

  def __contains__(self, item):
    item_id = item.getEstado().getId()
    for obj in self:
      obj_id = obj.getEstado().getId()
      if obj_id == item_id:
        return True
    return False

  def __repr__(self):
    cad = ""
    for o in self:
      cad += " - "+ str(o)
    return cad



class ItemFalla(SelectableDataItem):
  def __init__(self, is_selected=False, **kwargs):
    super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
    self.estado = None
    # Coleccion de objetos Captura
    self.colCapturas = []
    self.is_selected = False

  def getEstado(self):
    return self.estado


  def cambiarEstado(self,idfalla,altura,calle):
    estado_nuevo = Informada(idfalla,altura,calle)
    self.estado = estado_nuevo


  def estaSeleccionado(self):
    return self.is_selected


  def setEstado(self,estado):
    self.estado = estado
    print "Cambiado el estado de la falla a : %s" % (estado)
    print ""

  # Retorna la lista de capturas asociadas a una falla
  def getColCapturas(self):
    return self.colCapturas

  # Registra la captura en disco, la agrega a la coleccion de ItemFalla,
  # y registra la falla. 
  def registrarCaptura(self,dataSensor,item_falla,cap,capturador):
    self.estado.registrar(self,capturador,cap)
    cap.almacenarLocalmente(dataSensor,capturador)
    item_falla.getEstado().mostrar_capturas_asociadas(item_falla)

  def __cmp__(self,other):
    self_id = self.getEstado().getId()  
    other_id =other.getEstado().getId()
    if self_id > other_id:
      return 0
    elif self_id == other_id:
      return 0
    else:
      return -1

  # Si la falla esta seleccionada,se convierte y se
  # envia al servidor en formato json.
  # TODO: CONTINUAR POR ACA!!!
  def enviar(self,url_server,api_client,cantidad_fallas):
    print "Inicio ItemFalla "
    if self.is_selected:
      # Se convierte cada captura en un csv y luego se envia la falla en 
      # formato JSON al servidor.
      capturas_dic = {}
      for cap in self.colCapturas:
        data_cap = cap.convertir()
        #Se indexa la data por el nombre del archivo de la captura.
        # {"nombre_archivo_csv.csv"," CONTENIDO DE LA NUBE DE PUNTOS"}
        capturas_dic[cap.getNombreArchivoCaptura()] = data_cap

      falla_formateada = {
                          "id": self.getEstado().getId(),    
                          "calle": self.getEstado().getCalle(),    
                          "altura": self.getEstado().getAltura(),    
                          "data_capturas": capturas_dic
                          }
      falla_json = JSONEncoder.encode(falla_formateada)
      print "falla_json tiene los siguientes datos -->\n %s" % falla_json
      print ""
      print "Enviando captura ...\n"
      api_client.postCapturas(falla_json,cantidad_fallas)


class Capturador(object):

  def __init__(self):
    self.colCapturasTotales = []
    self.colCapturasConfirmadas = []
    self.apiClient = ApiClientApp()
    self.estrategia = EstrategiaConfirmados()
    print "Inicializado Capturador"

  def getColCapturasTotales(self):
    return self.colCapturasTotales

  def getColCapturasConfirmadas(self):
    return self.colCapturasConfirmadas

  # Retorna la cantidad de archivos que tienen un nombre dado
  # en el directorio de trabajo especificado. Se detecta la
  # extension desde la derecha del archivo.
  def getCantidadCapturas(self,archivo_a_buscar,dirTrabajo,extensionArchivo):
    dir_actual = os.getcwd()
    os.chdir(dirTrabajo)
    contador_arch = 1
    plantilla_archivo = archivo_a_buscar + SUBFIJO + "%s" + extensionArchivo
    while os.path.exists( plantilla_archivo % contador_arch):
        contador_arch += 1
    print "Cantidad de archivos .pcd con el nombre ",archivo_a_buscar, "es : ",contador_arch
    print ""
    os.chdir(dir_actual)
    return contador_arch
    

  # Asocia la falla con la captura recien realizada.
  def asociarFalla(self,data, dir_trabajo, nombre_captura,id_falla):
    falla = ItemFalla()
    api_geo = GeofencingAPI()
    latitud_prueba,longitud_prueba = api_geo.getLatLong()
    estado = Confirmada(latitud_prueba,longitud_prueba).cambiar(falla)
    # estado = Confirmada(LAT_PRUEBA,LONG_PRUEBA).cambiar(falla)
    self.capturar(data, dir_trabajo, nombre_captura,falla)


  def capturar(self,dataSensor, dir_trabajo, nombre_captura,item_falla):
    # Se instancia la captura(con los valores de la view anterior),
    # se almacena en disco y se se agrega a la lista de capturas del 
    # capturador.
    cap = Captura(nombre_captura,dir_trabajo,FORMATO_CAPTURA, EXTENSION_ARCHIVO)
    # Se indica a la falla que registre su captura, la alamcene en disco y
    # la agregue a su colCapturas .
    # def registrarCaptura(self,dataSensor,item_falla,cap,capturador):
    item_falla.registrarCaptura(dataSensor,item_falla,cap,self)
    print "Captura realizada con exito! Agregada: ",str(cap)
    print ""

  # Filtra las colCapturasTotales y agrega solamente las capturas confirmadas
  # a la colCapturasConfirmadas
  def filtrarCapturas(self):
    # Se vacian la coleccion de capturas confirmadas
    self.colCapturasConfirmadas = []
    self.estrategia.filtrar(self.colCapturasConfirmadas,self.colCapturasTotales)



  # Envia las fallas que capturo el capturador.
  def enviarCapturas(self,url_server,total_fallas_confirmadas,cant_actual_enviada):
    controlador = App.get_running_app()
    for falla in self.capturador.getColCapturasConfirmadas():
      falla.enviar(URL_UPLOAD_SERVER,self.apiClient)
      # Actualizacion grafica del porcentaje de fallas enviadas
      cant_actual_enviada = cant_actual_enviada + 1
      controlador.actualizar_porcentaje_envio(total_fallas_confirmadas,
                                              cant_actual_enviada)
  
# + Capturador > CapturadorInformado
#     -ColBachesInformados (Se envian la calle y/o altura y envia los informados en ese rango)
#     +solicitarInformados()

class CapturadorInformados(Capturador):
  def __init__(self):
    super(CapturadorInformados,self).__init__()
    self.colBachesInformados = ListadoFallas()
    self.estrategia = EstrategiaInformados()
    print "Inicializado CapturadorInformado"

  def getColBachesInformados(self):
    return self.colBachesInformados


  def inicializar_fallas(self):
    for obj in self.colBachesInformados:
      obj.is_selected = False

  def solicitarInformados(self,calle):
    try:
      # Hace un GET al servidor para obtener todos los baches en una calle
      # Para probar esta parte ejecutar apiclient/servidor_json.py.
      dic_json = self.apiClient.getInformados(calle)

      for key,tupla in dic_json.iteritems():
          falla = ItemFalla()
          estado = Informada(tupla["id"],tupla["calle"],tupla["altura"])
          estado.cambiar(falla)
          if falla not in self.colBachesInformados:
            self.colBachesInformados.append(falla)

      self.colBachesInformados = sorted(self.colBachesInformados)
      self.inicializar_fallas()
      self.mostrar_coleccion()

    except ExcepcionAjax, e:
      mostrarDialogo(titulo="Error en solicitud al servidor",
                      content= e.message)

    return self.colBachesInformados


  # Asocia la falla con la captura recien realizada.
  def asociarFalla(self,data, dir_trabajo, nombre_captura,id_falla):
    print "Inicio asociarFalla() para id_falla: ",id_falla
    print ""
    itemFalla = None
    for b in self.colBachesInformados:
      if id_falla == b.getEstado().getId():
        itemFalla = b
        print "Encontrado ItemFalla(%s): ",id_falla
        break
    if itemFalla is not None:
      self.capturar(data, dir_trabajo, nombre_captura,itemFalla)
      print "Fin de asociarFalla()"


  def mostrar_coleccion(self):
    for obj in self.colBachesInformados:
      obj_id = obj.getEstado().getId()
      obj_calle = obj.getEstado().getCalle()
      obj_altura = obj.getEstado().getAltura()
      print "Id falla: ",obj_id,"; Calle:",obj_calle,"; Altura: ",obj_altura





