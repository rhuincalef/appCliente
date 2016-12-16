# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App

import sys,os
from apiclient1 import ApiClientApp,ExcepcionAjax
from kivy.adapters.models import SelectableDataItem
from constantes import *
from utils import *
# from utils import mostrarDialogo,calcularTamanio
from captura import *
from estadofalla import *
from geofencing import *
from estrategia import *


from json import JSONEncoder,JSONDecoder


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


  # Se llama cuando se necesita la representacion compatible con json
  # para guardar en disco
  def __str__(self):
    representacion_string = "{}"
    # Segun el tipo de estado se retorna una representacion distinta.
    if type(self.estado) is Informada:
      representacion_string = '{ "idFalla": %s, "calle": %s, "altura": %s, "tipo": "informada", "data_capturas": %s }' %\
        (self.estado.getId(),self.estado.getCalle(),self.estado.getAltura(),
          str(self.colCapturas) )
    else:
      representacion_string = '{ "idFalla": %s, "calle": %s, "altura": %s, "tipo": "confirmada","latitud": %s,"longitud": %s,"data_capturas": %s }' %\
        (99,"Unknown","Unknown",str(self.estado.getLatitud()),str(self.estado.getLongitud()),
          str(self.colCapturas))
    return representacion_string


  # Si la falla esta seleccionada,se convierte y se envia al servidor con todas sus capturas
  # asociadas como un POST de tipo mime: multipart/form-data.
  def enviar(self,url_server,api_client):
    print "Inicio ItemFalla "
    if self.is_selected:
      # Se convierte cada captura en un csv y luego se envia la falla en 
      # formato JSON al servidor.
      capturasConvertidas = []
      cantCapturasAEnviar = len(self.colCapturas)
      for cap in self.colCapturas:
        #Si se supera el tamanio maximo de una peticion POST o si se supera
        # la cantidad de archivos permitida por peticion, se envia la peticion 
        # con la cant. actual de archivos y se vacia capturasConvertidas 
        # para seguir preparando las proximas peticiones.
        print "Convirtiendo captura de la falla: %s" % cap
        nombreArchCsv = cap.convertir()
        capturasConvertidas.append(nombreArchCsv)
        cantCapturasAEnviar -= 1 
        print "Archivo %s generado " % nombreArchCsv
        print ""
        bytes_actuales_col = calcularTamanio(capturasConvertidas) 
        bytes_actuales_cap = calcularTamanio([cap.getNombreArchivoCaptura()])
        if (bytes_actuales_col + bytes_actuales_cap) >= MAX_POST_REQUEST_SIZE or \
                    len(capturasConvertidas) == MAX_FILE_UPLOADS_FOR_REQUEST or \
                      cantCapturasAEnviar == 0:
          print "bytes_actuales_col: %s -MAX_POST_SIZE: %s" %\
              (bytes_actuales_col,MAX_POST_REQUEST_SIZE)
          print ""
          print "len(capturasConvertidas)= %s ; MAX_FILE_UPLOADS_FOR_REQUEST= %s" %\
            (len(capturasConvertidas),MAX_FILE_UPLOADS_FOR_REQUEST)
          print "cantCapturasAEnviar = %s" % cantCapturasAEnviar
          print ""
          falla_formateada = {
                          "id": self.getEstado().getId(),    
                          "calle": self.getEstado().getCalle(),    
                          "altura": self.getEstado().getAltura(),    
                          "data_capturas": capturasConvertidas
                          }
          api_client.postCapturas(url_server,falla_formateada)
          print "Enviando la peticion: %s " % falla_formateada
          print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
          capturasConvertidas = []


  # Retorna el tamanio en bytes de los .pcd asociados a una captura.
  # Se invoca para actualizacion de la progressbar y el label con 
  # los bytes enviados/totales
  def calcularTamanio(self):
    bytes = 0
    nombres_capturas = []
    for captura in self.colCapturas:
      arch_pcd = captura.getFullPathCaptura()
      nombres_capturas.append(arch_pcd)
    bytes = calcularTamanio(nombres_capturas)
    print "Los bytes totales calculados que se enviaran son: %s" %\
        bytes
    print ""
    return bytes


class Capturador(object):

  def __init__(self,apiclientComun):
    self.colCapturasTotales = []
    self.colCapturasConfirmadas = []
    self.apiClient = apiclientComun
    # self.apiClient = ApiClientApp()
    self.estrategia = EstrategiaConfirmados()
    print "Inicializado Capturador"


  #Reestablece el contador de bytes totales a enviar a cero
  def reestablecerApiClient(self):
    self.apiClient.reestablecerApiClient()

  # Se delega el metodo de apiClient que mantiene este atributo
  def setCantBytesTotales(self,bytes_totales_a_enviar):
    self.apiClient.setCantBytesTotales(bytes_totales_a_enviar)


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
  

  #Lee el archivo json especificado de disco.
  def leerFallas(self,stream):
    try:
      content = stream.read()
      #TODO: Terminar de configurar PARSER FALLAS PARA QUE INSTANCIE LAS FALLAS
      # COMPLETAS CON SU ESTADO, LOS OBJETOS CAPTURA Y DEMAS.
      # CONTINUAR POR ACA!!!

      lista_fallas = JSONDecoder(object_hook=parser_fallas).decode(content)
      print "El listado de objetos json parseados tiene: %s" % lista_fallas
      self.colCapturasTotales = lista_fallas
    except Exception, e:
      raise Exception("Error leyendo el archivo de fallas desde disco")


  #Guarda el archivo json especificado de disco.
  def guardarFallas(self,stream):
      json_str = ""
      try:
        for captura in self.colCapturasTotales:
          json_str = json_str +" "+ str(captura) 

        print "El json_str a guardar es: %s " % json_str
        stream.write(json_str)
      except Exception, e:
        raise Exception("Error escribiendo el archivo de fallas en disco")
      


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
  def enviarCapturas(self,url_server):
    controlador = App.get_running_app()
    for falla in self.getColCapturasConfirmadas():
      falla.enviar(URL_UPLOAD_SERVER,self.apiClient)
      # Actualizacion grafica del porcentaje de fallas enviadas
      # cant_actual_enviada = cant_actual_enviada + 1
      # controlador.actualizar_barra_progreso(total_fallas_confirmadas,
      #                                         cant_actual_enviada)
    # return cant_actual_enviada


  # Calcula el tamanio de las capturas asociadas a cada una de las fallas
  # confirmadas para envio al server.
  def calcularTamanioCapturas(self):
    bytes = 0
    for falla in self.getColCapturasConfirmadas():
      bytes += falla.calcularTamanio()
    return bytes



# + Capturador > CapturadorInformado
#     -ColBachesInformados (Se envian la calle y/o altura y envia los informados en ese rango)
#     +solicitarInformados()

class CapturadorInformados(Capturador):
  def __init__(self,apiclientComun):
    Capturador.__init__(self,apiclientComun)
    # super(CapturadorInformados,self).__init__()
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





