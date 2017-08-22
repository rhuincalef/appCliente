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

#Borrado de capturas de una falla en disco
import subprocess
import threading



############################ Imports para el almacenamiento de un recorrido de fallas
import ZODB, ZODB.FileStorage
import time
import BTrees.OOBTree

from capturador import * #Definicion de itemFalla
from estadofalla import * #Definicion de Estado
import transaction
from zc.lockfile import LockError

#Interfaz para la creacion de procesos
from multiprocessing import Process, Pipe, Queue
import ZEO
import copy

from os import path




#NOTA: Los objetos "ListadoPropiedades" y "Propiedad"
# son las propiedades necesarias para dar de alta
# un tipo de falla con estado "Confirmado".


class ExcepcionTipoFallaIncompleta(Exception):
  pass

class ExcepcionSinDatosTiposFalla(Exception):
  pass

class ExcepcionRecorridoVacio(Exception):
  pass



#TipoMaterial ocurre en --> TipoFalla
#TipoReparacion es para --> TipoFalla
#listadoTiposFalla = [
# 	{
# 	"clave": "tipoFalla",
# 	"valor": "Bache",
# 	"colPropsAsociadas": [
#			 		{"clave": "tipoReparacion", "valor":"Sellado"},
#			 		{"clave": "tipoReparacion", "valor":"Cementado"},
#			 		{"clave": "tipoMaterial", "valor":"Pavimento asfaltico"]},
#			 		{"clave": "tipoMaterial", "valor":"Cemento"},
#			 		...
#					]
#	},
# 	...	
#]


#-ListadoPropiedades
#	-colPropiedad
#	+__contains__()
#	+agregarProp(propiedad)
#	+eliminarProp(propiedad)
#	+guardar(tinyDB) -Guarda la propiedad en disco

#Listado de elementos Propiedad
class ListadoPropiedades(list):  
  def __init__(self, *args):
    list.__init__(self, *args)

  def __contains__(self, prop):
    clave_prop = prop.getClave()
    for obj in self:
      if prop.getClave() == clave_prop:
        return True
    return False

  def __repr__(self):
    cad = ""
    for o in self:
      cad += " - "+ str(o)
    return cad

  def agregarProp(self,propiedad):
    self.append(propiedad)


  def eliminarProp(self,propiedad):
    self.remove(propiedad)

  def guardar(self,tinyDB):
    for o in self:
      o.guardar(tinyDB)


  #AGREGADO RODRIGO
  #Cuenta la cantidad de propiedades maxima entre los distintos tipos de falla
  # y retorna la cantidad maxima de esa propiedad, entre todos los tipos de falla.
  def getCantPropsTipoFalla(self,nombreProp):
    cantMaxima = 0
    for tipoFalla in self:
      cantidadActual = tipoFalla.getCantProps(nombreProp) 
      if cantMaxima < cantidadActual:
        cantMaxima = cantidadActual
    print "Cantidad maxima de propiedades: %s es: %s\n" % (nombreProp,cantMaxima)
    return cantMaxima


  #AGREGADO RODRIGO
  # Retorna la referencia a una propiedad "tipoFalla" en base al nombre
  def getTipoFallaPorValor(self,nombreTipoFalla):
    for tipoFalla in self:
      if tipoFalla.getValor() == nombreTipoFalla:
        return tipoFalla
    return None


  #AGREGADO RODRIGO
  # Obtiene las subpropiedades de un tipo de falla dado su nombre y el de 
  # su subpropiedad.
  # .getPropsAsociadasATipoFalla("bache","tipoMaterial")
  # .getPropsAsociadasATipoFalla("bache","criticidad")
  def getPropsAsociadasATipoFalla(self,nombreTipoFalla,nombreSubPropiedad):
    subProps = []
    for prop in self:
      if prop.getValor() == nombreTipoFalla:
        subProps = prop.getPropsAsociadasPorNombre(nombreSubPropiedad)
    return subProps



#-Propiedad
#	-clave
#	-valor
#	-colPropsAsociadas #Propiedades asociadas validas con las 
						#reglas establecidas en la BD
#	+asociarPropiedad(prop)
#	+getPropsAsociadas() # Retorna
#	+getClave()
#	+getValor()
#	+guardar(tinyDB)

# NOTA: Representa una propiedad como:
# clave = "tipoCriticidad";  valor = "Media"
from tinydb import TinyDB
import json
#class JSONSerializable(object):
#  def __repr__(self):
#    return json.dumps(self.__dict__)   

#class Propiedad(JSONSerializable):
class Propiedad(object):
  def __init__(self,myID,clave,valor,estaTipoFallaHabilitada):
    self.clave = str(clave)
    self.valor = str(valor)
    self.colPropsAsociadas = []
    #Campos agregados
    self.id = myID
    # Este campo se emplea para habilitar/deshabilitar la seleccion de elementos en el 
    # widget "CustomDropdown".
    self.estaPropHabilitada = estaTipoFallaHabilitada

  def __repr__(self):
    return str(self.toDict())

  #AGREGADO RODRIGO
  def estaHabilitada(self):
    return self.estaPropHabilitada


  #AGREGADO RODRIGO
  # Obtiene las subpropiedades de un tipo de falla dado su nombre y el de 
  # su subpropiedad.
  def getPropsAsociadasPorNombre(self,nombreSubPropiedad):
    subProps = []
    for subProp in self.colPropsAsociadas:
      if subProp.getClave() == nombreSubPropiedad:
        subProps.append(subProp.getValor())
    return subProps



  #AGREGADO RODRIGO
  #Retorna la cantidad de propiedades que tiene la propiedad actual con un nombre dado.
  #SE EMPLEA PRINCIPALMENTE PARA LAS PROPS DIRECTAS DE LOS TIPOS DE FALLA.
  def getCantProps(self,nombreProp):
    cantProps = 0
    for prop in tipoFalla.getColPropsAsociadas():
      if prop["clave"] == nombreProp:
        cantProps += 1
    return cantProps

  # Convirte a diccionario la propiedad y sus atributos
  # asociados
  def toDict(self):
    dic = {"id": self.id,"clave": self.clave,"valor": self.valor,
            "colPropsAsociadas": []}
    for e in self.colPropsAsociadas:
      dic["colPropsAsociadas"].append(str(e))
    return dic

  # Convierte la propiedad a formato JSON valido para almacenar
  # en la BD local.  
  def serializar(self):  
    return json.dumps(str(self))
  def getValor(self):
    return self.valor
  def getColPropsAsociadas(self):
    return self.colPropsAsociadas
  def asociarPropiedad(self,p):
    self.colPropsAsociadas.append(p)
	# Guarda una propiedad en la BD local serializada en formato json.
  def guardar(self,tinyDB):
    tinyDB.insert(self.toDict())
  def getClave(self):
    return self.clave


#Listado de elementos ItemFalla
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

######################## Clase que representa a una Falla ####################
from persistent import Persistent

class ItemFalla(SelectableDataItem,Persistent):
  def __init__(self, is_selected=False, **kwargs):
    #NOTA: is_selected se modifica cuando el usuario selecciona una itemFalla para subir al servidor. 
    super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
    self.estado = None
    # Coleccion de objetos Captura
    self.colCapturas = []
    #self.is_selected = False
    self.estaSubidaAlServidor = False # Flag que indica si se subio o no una falla
                                      # al servidor.


  def __str__(self):
    cad = "-->{ 'estado': { %s }, 'capturas':  %s , 'is_selected': %s , 'estaSubidaAlServidor': %s }<--    " %\
        (str(self.estado),self.colCapturas,self.is_selected,self.estaSubidaAlServidor)
    return cad

  def __cmp__(self,other):
    self_id = self.getEstado().getId()  
    other_id = other.getEstado().getId()
    print "En __cmp__() con self_id: %s y other_id: %s\n" % (self_id,other_id)
    if self_id > other_id:
      return 1
    elif self_id == other_id:
      return 0
    else:
      return -1


  def desSeleccionar(self):
    self.is_selected = False

  def seleccionar(self):
    self.is_selected = True


  def estaSubida(self):
    return self.estaSubidaAlServidor

  def marcarComoSubida(self):
    self.estaSubidaAlServidor = True

  #Asigna el tipofalla,tipoReparacion y tipoMaterial especificado por el usuario
  def asignarPropiedades(self):
    controlador = App.get_running_app()
    self.estado.setTipoFalla(controlador.getData("tipoFalla"))
    #self.estado.setTipoReparacion(controlador.getData("tipoReparacion"))
    self.estado.setCriticidad(controlador.getData("criticidad"))
    self.estado.setTipoMaterial(controlador.getData("tipoMaterial"))
    print "Asignadas propiedades al estado de falla confirmada!"
    print "tipoFalla: %s; tipoReparacion: %s; tipoMaterial: %s\n" %\
          (controlador.getData("tipoFalla"),controlador.getData("criticidad"),
            controlador.getData("tipoMaterial"))
    #print "tipoFalla: %s; tipoReparacion: %s; tipoMaterial: %s\n" %\
    #      (controlador.getData("tipoFalla"),controlador.getData("tipoReparacion"),
    #        controlador.getData("tipoMaterial"))                           


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

  # Registra la captura en disco,la convierte a .csv,
  # la agrega a la coleccion de ItemFalla y registra la falla. 
  def registrarCaptura(self,dataSensor,cap,capturador):
    controlador = App.get_running_app()
    cap.almacenarLocalmente(dataSensor,capturador,controlador.args.tipoCaptura)
    self.estado.registrar(self,capturador,cap)
    nombreArchCsv = cap.convertir()
    print "Convertida con nombre de archivo %s \n" % nombreArchCsv
    self.getEstado().mostrar_capturas_asociadas(self)




  # Se llama cuando se necesita la representacion compatible con json
  # para guardar en disco
  #def __str__(self):
  #  representacion_string = "{}"
    # Segun el tipo de estado se retorna una representacion distinta.
  #  if type(self.estado) is Informada:
  #    representacion_string = '{ "idFalla": %s, "calle": %s, "altura": %s, "tipo": "informada", "data_capturas": %s ,"is_selected": %s }' %\
  #      (self.estado.getId(),self.estado.getCalle(),self.estado.getAltura(),
  #        str(self.colCapturas),self.is_selected )
  #  else:
  #    representacion_string = '{ "idFalla": %s, "calle": %s, "altura": %s, "tipo": "confirmada","latitud": %s,"longitud": %s,"data_capturas": %s ,"is_selected": %s }' %\
  #      (99,"Unknown","Unknown",str(self.estado.getLatitud()),str(self.estado.getLongitud()),
  #        str(self.colCapturas),self.is_selected)
  #  return representacion_string




  # Si la falla esta seleccionada,se convierte y se envia al servidor con todas sus capturas
  # asociadas como un POST de tipo mime: multipart/form-data.
  #
  # NOTA IMPORTANTE1: LOS ITEMFALLA CONFIRMADOS TIENEN UNA COLECCION DE 1 
  # CAPTURA, MIENTRAS QUE LOS ITEMFALLA INFORMADOS TIENEN ASOCIADA UNA COLECCION
  # DE VARIAS CAPTURAS.
  #
  # NOTA IMPORTANTE2: LA CANCELACION DE SUBIDA DE ARCHIVOS SE HACE POR ITEMFALLA,
  # ASI QUE SI EL USUARIO PULSA CANCELAR, SE DEBE TERMINAR DE SUBIR TODAS LAS CAPTURAS
  # ASOCIADAS CON EL ITEMFALLA COMPLETO, Y LUEGO TERMINAR LA SUBIDA.
  #
  # Itemfalla.enviar()
  #
  def enviar(self,url_server,api_client,bytes_leidos):
    print "Inicio ItemFalla.enviar() para la falla:\n %s\n" % self
    controlador = App.get_running_app()
    #Agregado Rodrigo
    logger = utils.instanciarLogger(LOG_FILE_CAPTURAS_INFO_SERVER)

    if self.is_selected:
      # Se convierte cada captura en un csv y luego se envia la falla en 
      # formato JSON al servidor.
      capturasConvertidas = []
      cantCapturasAEnviar = len(self.colCapturas)

      #Se marca el itemfalla como subido al servidor
      self.marcarComoSubida()

      for i in xrange(0,len(self.colCapturas)):
        #print "Iterando captura de itemfalla con controlador.canceladaSubidaArchivos:%s y cantCapturasAEnviar: %s...\n" %\
        #  (controlador.canceladaSubidaArchivos,cantCapturasAEnviar)

        #Si se supera el tamanio maximo de una peticion POST o si se supera
        # la cantidad de archivos permitida por peticion, se envia la peticion 
        # con la cant. actual de archivos y se vacia capturasConvertidas 
        # para seguir preparando las proximas peticiones.
        #
        #print "Convirtiendo captura de la falla: %s" % cap
        #nombreArchCsv = cap.convertir()
        nombreArchCsv = self.colCapturas[i].getFullPathCapturaConv()
        capturasConvertidas.append(nombreArchCsv) 
        cantCapturasAEnviar -= 1

        # Si los bytes_actuales de la colecccion de capturas + el tamanio de la captura actual
        # superan el MAX_POST_SIZE se invoca al api_client para su envio.
        # Sino, se continuan agregando mas capturas para enviar.
        #bytes_actuales_cap = calcularTamanio([self.colCapturas[i].getFullPathCapturaConv()])
        #bytes_actuales_col = calcularTamanio(capturasConvertidas)
        bytes_actuales_cap = utils.calcularTamanio([self.colCapturas[i].getFullPathCapturaConv()])
        bytes_actuales_col = utils.calcularTamanio(capturasConvertidas)

        if bytes_actuales_col + bytes_actuales_cap >= MAX_POST_REQUEST_SIZE or \
                    len(capturasConvertidas) == MAX_FILE_UPLOADS_FOR_REQUEST or \
                      cantCapturasAEnviar == 0:
          #print "bytes_actuales_col: %s ; MAX_POST_SIZE: %s\n" %\
              #(bytes_actuales_col,MAX_POST_REQUEST_SIZE)          
          #print "len(capturasConvertidas)= %s ; MAX_FILE_UPLOADS_FOR_REQUEST= %s" %\
            #(len(capturasConvertidas),MAX_FILE_UPLOADS_FOR_REQUEST)
          #print "cantCapturasAEnviar = %s\n" % cantCapturasAEnviar

          #Se piden lso campos formateados para el envio a la falla
          falla_formateada = self.getDicFalla()
          #print "Enviando la peticion: %s\n " % falla_formateada
          bytes_leidos = api_client.postCapturas(url_server,
                                                falla_formateada,
                                                capturasConvertidas,
                                                bytes_leidos,
                                                logger)
          #print "\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"
          capturasConvertidas = []

        # NOTA: Se retorna de la funcion unicamente cuando se han enviado todos los 
        # objetos captura asociados a la falla
        if controlador.canceladaSubidaArchivos and cantCapturasAEnviar == 0:
          print "Cancelada la subida de archivos desde itemFalla.enviar()...\n"
          return 
    return bytes_leidos


  # Retorna el tamanio en bytes de los ".csv "asociados a una captura.
  # Se invoca para actualizacion de la progressbar y el label con 
  # los bytes enviados/totales.
  def calcularTamanio(self):
    mybytes = 0
    nombres_capturas = []
    for captura in self.colCapturas:
      arch_csv = captura.getFullPathCapturaConv()
      nombres_capturas.append(arch_csv)
    #mybytes = calcularTamanio(nombres_capturas)
    mybytes = utils.calcularTamanio(nombres_capturas)
    return mybytes


  def setCalleEstimada(self,calle):
    self.estado.setCalleEstimada(calle)

  def setRangosEstimados(self,rango1,rango2):
    self.estado.setRangosEstimados(rango1,rango2)


  # Obtiene el diccionario completo para enviar cada falla al servidor.
  # Es invocado desde enviar() y retorna el diccionario "falla_formateada"
  # que se usa en ese metodo.
  def getDicFalla(self):
    return self.estado.getDicFallaEncoded()


  # Descarta un item falla de la coleccion de fallas confirmadas de 
  # un capturador(Invocado desde Capturador).
  #
  # itemfalla.descartar()
  #  
  def descartar(self,colItemFallasSubidos):
    print "En itemFalla.descartar()...\n"
    print "La coleccion antes de descartar el itemfalla con sus capturas tiene:%s\n"
    ItemFalla.mostrarColItemFalla(colItemFallasSubidos)
    for captura in self.colCapturas:
      captura.descartar(self.colCapturas)
    print "Fin de itemFalla.descartar()\n"


  # Valida las capturas asociadas a una falla, comprobando que existan en
  # disco y retornando TRUE si al menos existe una captura valida asociada a la
  # falla. Si no, retorna FALSE.
  # NOTA: Se comprueba la validez de los  archivos .csv que son los que
  # se envian al servidor.
  # 
  def filtrarCapturasConsistentes(self,logger):
    print "En filtrarCapturas consistentes!\n"
    colCapsValidas = list()
    for cap in self.colCapturas:
      pathCsv = cap.getFullPathCapturaConv()
      print "Leyendo csv: %s ; path.exists(pathCsv):%s \n" % (pathCsv,
                                                          path.exists(pathCsv))
      msg = ""
      if path.exists(pathCsv):
        colCapsValidas.append(cap)
      else:
        atributo1 = atributo2 = atributo3 =None
        atributo1 = self.estado.getId()
        if isinstance(self.estado,Confirmada):
          atributo2 = self.estado.getLatitud()
          atributo3 = self.estado.getLongitud()
        else:
          atributo2 = self.estado.getCalle()
          atributo3 = self.estado.getAltura()
        
        msg = 'Captura de falla (%s,%s,%s) %s no encontrada.Descartando...' %\
        (atributo1,atributo2,atributo3,pathCsv)
        utils.loggearMensaje(logger,msg)

    #Se establece la colCapturas actualizada a la falla
    self.colCapturas = colCapsValidas
    #Se retorna True si se agregaron caps validas a la itemfalla.colCapturas
    result = False 
    if len(self.colCapturas) > 0:
      result = True
    return result 



  @staticmethod
  def mostrarColItemFalla(col):
    print "----------------------------------------------------------\n"
    print "En itemfalla.mostrarColItemFalla()...\n"
    print "----------------------------------------------------------\n"
    for item in col:
      print "%s\n" % item
      print "+++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    print "----------------------------------------------------------\n"
    print "Fin de itemfalla.mostrarColItemFalla()...\n"
    print "----------------------------------------------------------\n"


class Capturador(object):
  def __init__(self,apiclientComun,**kwargs):		
    #NOTA: Tanto colCapturasTotales como colCapturasConfirmadas 
    # contienen elementos "ItemFalla", que tienen objetos "Captura" asociados. 
    self.colCapturasTotales = [] #Todas las capturas hechas informadas y confirmadas.
    self.colCapturasConfirmadas = [] # Aquellas seleccionadas para enviar al servidor 
    self.apiClient = apiclientComun
    # self.apiClient = ApiClientApp()
    self.estrategia = EstrategiaConfirmados()
    self.api_geo = GeofencingAPI()
    print "Inicializado Capturador"
    self.propsConfirmados = ListadoPropiedades() #Listado de objetos que se asocian
    # con los atrigbutos de un tipoFalla confirmada
    # y que son obligatorios(tipo reparacion y 
    # tipo de material).


  #Retorna los tiposFalla con todas sus propiedades
  def getPropsConfirmados(self):
    return self.propsConfirmados




  #Reestablece el contador de bytes totales a enviar a cero
  def reestablecerApiClient(self):
    self.apiClient.reestablecerApiClient()

  # Se delega el metodo de apiClient que mantiene este atributo
  def setCantBytesTotales(self,bytes_totales_a_enviar):
    self.apiClient.setCantBytesTotales(bytes_totales_a_enviar)


  def getColCapturasTotales(self):
    return self.colCapturasTotales

  def setColCapturasTotales(self,col):
    self.colCapturasTotales = col

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

  # Asocia el ItemFalla con la captura recien realizada,
  # se cambia el estado de la falla a Confirmada, y se utiliza
  # API_GEO (Obtener LATITUD y LONGITUD del GPS).
  #
  # capturador.asociarFalla()
  def asociarFalla(self,data, dir_trabajo, nombre_captura,id_falla,gps):
    print "En capturador FALLA NUEVA!!!\n"

    falla = ItemFalla()
    if gps == TIPO_GPS_DEFAULT:
      # COORDENADAS DE PRUEBA ARTIFICIALES
      latitud_prueba,longitud_prueba = self.api_geo.getLatLong()
    else:
      # COORDENADAS DE PRUEBA REALES
      latitud_prueba,longitud_prueba = self.api_geo.obtenerLatitudLongitud()
    
    #TODO: Al momento de crear el estado de confirmada se debe dar un ID negativo
    # a la falla, que es relativo a su posicion en la coleccion de fallas confirmadas.
    estado = Confirmada(latitud_prueba,longitud_prueba).cambiar(falla)
    
    #Se agregan las propiedades a la falla
    falla.asignarPropiedades()
    #self.capturar(data, dir_trabajo, nombre_captura,falla,latitud_prueba,
    #  longitud_prueba)
    return self.capturar(data, dir_trabajo, nombre_captura,falla,latitud_prueba,
      longitud_prueba)

  #Metodo de captura de fallas nuevas
  # capturador.capturar() invocado desde main.threadCapturarFalla()
  def capturar(self,dataSensor, dir_trabajo, nombre_captura,item_falla,latitud,longitud):
    print "En capturador.capturar()\n"
    print "dir_trabajo: %s ; nombre_captura: %s\n" % (dir_trabajo,nombre_captura)
    # Se instancia la captura(con los valores de la view anterior),
    # se almacena en disco y se se agrega a la lista de capturas del 
    # capturador.
    cap = Captura(nombre_captura,dir_trabajo,FORMATO_CAPTURA, EXTENSION_ARCHIVO)
    # Se indica a la falla que registre su captura, la alamcene en disco y
    # la agregue a su colCapturas .
    item_falla.registrarCaptura(dataSensor,cap,self)

    print "Captura realizada con exito! Agregada: ",str(cap)
    print ""
    self.api_geo.almacenarCapturaLocal(latitud,longitud,cap.getFullPathCaptura())
    print "Guardado archivo .pcd en BD_JSON!"
    print ""
    #AGREGADO RODRIGO
    return cap.getFullPathCaptura(),cap.getFullPathCapturaConv()

  # Filtra las colCapturasTotales y agrega solamente las capturas seleccionadas en el listview
  # a la colCapturasConfirmadas
  def filtrarCapturas(self):
    # Se vacian la coleccion de capturas confirmadas
    self.colCapturasConfirmadas = []
    self.estrategia.filtrar(self.colCapturasConfirmadas,self.colCapturasTotales,self)	 	
	

  #Obtiene la calle y altura de cada falla confirmada y las establece
  # en el estado 
  def obtenerDirEstimada(self,itemFalla):
    calle,rangoEstimado1,rangoEstimado2 = self.apiClient.obtenerDirEstimada(itemFalla.getEstado().getLatitud(),
                    itemFalla.getEstado().getLongitud())
    itemFalla.setCalleEstimada(calle)
    itemFalla.setRangosEstimados(rangoEstimado1,rangoEstimado2)


  

  # Envia las fallas que capturo el capturador.
  # capturador.enviarCapturas()
  def enviarCapturas(self,url_server):
    print "En capturador.enviarCapturas()\n"
    controlador = App.get_running_app()
    bytes_leidos = 0
    for falla in self.getColCapturasConfirmadas():
      #print "\nEnviando falla %s\n" % (falla,falla.is_selected)
      if falla.is_selected:
        bytes_leidos += falla.enviar(URL_UPLOAD_SERVER,self.apiClient,bytes_leidos)
    print "Fin de capturador.enviarCapturas()!\n"


  # Calcula el tamanio de las capturas asociadas a cada una de las fallas
  # confirmadas para envio al server.
  def calcularTamanioCapturas(self):
    bytesEnviar = 0
    for falla in self.getColCapturasConfirmadas():
      if falla.is_selected:
        bytesEnviar += falla.calcularTamanio()
    return bytesEnviar


  #Este metodo descarta la captura de memora y de disco(.pcd y .csv)
  #capturador.descartar()
  def descartar(self,capturas):
    print "Inicio de capturador.descartar()\n"
    colItemFalla = self.colCapturasTotales
    capEstaDescartada = False
    for itemFalla in colItemFalla:
      #Por cada captura de cada itemFalla...
      colCaps = itemFalla.getColCapturas()
      for cap in colCaps:
        if cap.getFullPathCaptura() in capturas:
          print "Captura encontrada! en: %s \n" % capturas
          cap.descartar(colCaps)
          capEstaDescartada = True
          print "Descartada correctamente! \n"
          Capturador.mostrarCapturas(colCaps)
          break
    print "Fin de capturador.descartar()\n"
    return capEstaDescartada
  		
  @staticmethod
  def mostrarCapturas(colCaps):
    print "En mostrarCapturas()\n"
    for c in colCaps:
      print "captura asociada a la falla: %s \n" % c.getFullPathCaptura()
    print "Fin mostrarCapturas()\n"


  # Invocado desde main.noConservarCapsLuegoSubida().
  # Elimina los itemFalla de la colCapturasConfirmadas
  # luego de haberlas registrado en el servidor.
  # capturador.descartarCapsSubidas()
  #
  def descartarCapsSubidas(self):
    colItemFalla = self.colCapturasConfirmadas
    for f in colItemFalla:
      print "Iterando desde capturador.descartarCapsSubidas()\n"
      print "falla: %s\n" % f
      if f.is_selected and f.estaSubida():
        f.descartar(colItemFalla)
        print "\n\nMostrando la coleccion colItemFalla despues de borrar una falla subida:\n%s\n"
    # Se obtienen las capturasConfirmadas no subidas (no seleccionadas) y
    # se actualiza la lista de capturas confirmadas con esas fallas.
    fallasNoDescartadas = self._filtrarCapturasConservadas(colItemFalla)
    self.colCapturasConfirmadas = fallasNoDescartadas
    ItemFalla.mostrarColItemFalla(colItemFalla)


  #Filtra aquellas capturas que no estan subidas
  def _filtrarCapturasConservadas(self,colItemFalla):
    fallasNoDescartadas = list()
    for f in colItemFalla:
      if not f.is_selected:
        fallasNoDescartadas.append(f)
    return fallasNoDescartadas
    


  #Invocado desde main.threadGetPropsConfirmadas()
  def obtenerPropsConfirmadas(self):
    dicPropsConfirmados = self.apiClient.getPropsConfirmados() 
    self.crearListaProps(dicPropsConfirmados)

  # Vacia la BD Confirmadas y la actualiza con los datos
  # que leyo del servidor.
  def crearBackupConfirmados(self):
    tinydb = TinyDB(LOCAL_BD_PROPS_CONFIRMADAS)
    if len(tinydb.all())>0:
      tinydb.purge()
    self.propsConfirmados.guardar(tinydb)
    print "Creado un resplado de las propiedades de las fallas confirmadas!\n"


  # Retorna una lista de objetos "Propiedad" consistentes con los requerimientos para dar de alta
  # un tipo de falla confirmada.
  # Valida si el json obtenido desde el servidor es valido:
  #  -Debe contener al menos un tipoFalla en la coleccion general
  #  -Y cada tipo de falla debe tener asociado al menos un tipo de 
  # reparacion y un tipo de material. Sino se debe usar una copia
  # de la BD anterior.
  #
  #FORMATO A PARSEAR -->
#listadoTiposFalla = [
#   {
#   "clave": "tipoFalla",
#   "valor": "Bache",
#   "colPropsAsociadas": [
#         {"clave": "tipoReparacion", "valor":"Sellado"},
#         {"clave": "tipoReparacion", "valor":"Cementado"},
#         {"clave": "tipoMaterial", "valor":"Pavimento asfaltico"]},
#         {"clave": "tipoMaterial", "valor":"Cemento"},
#         ...
#         ]
# },
#   ... 
#]

  def crearListaProps(self,listaProps):
    print "En crearListaProps()...\n"
    if len(listaProps) == 0:
      msg = "Listado de tipos de falla incompleto" 
      raise ExcepcionTipoFallaIncompleta(msg)

    # Si la falla es valida, Se la crea y se asocian las propidades a la misma.
    for tipoFalla in listaProps:
      print "tipoFalla['id']: %s\n" % tipoFalla["id"]
      estaTipoFallaHabilitada = False
      if int(tipoFalla["id"]) in IDS_TIPOS_FALLA_HABILITADOS:
        estaTipoFallaHabilitada = True

      self.validarPropsDeTipoFalla(tipoFalla)
      falla = Propiedad(tipoFalla["id"],tipoFalla["clave"],tipoFalla["valor"],
                          estaTipoFallaHabilitada)
      #Se asocian las propiedades que pueda tener la propiedad del tipo de falla
      for p in tipoFalla["colPropsAsociadas"]:
        prop = json.loads(utils.escaparCaracteresEspeciales(p))
        propiedad = Propiedad(  prop["id"],
                                str(prop["clave"].encode("utf-8")),
                                str(prop["valor"].encode("utf-8")),
                                estaTipoFallaHabilitada)
        print "Creada propiedad asociada: %s ...\n" % propiedad
        falla.asociarPropiedad(propiedad)
      self.propsConfirmados.append(falla)

    print "Fin de crearListaProps()...\n"
    print "self.propsConfirmados tiene: \n\n%s\n" % self.propsConfirmados


  #Valida el atributo "colPropsAsociadas" para que contenga
  # al menos un tipo de material y un tipo de reparacion.
  def validarPropsDeTipoFalla(self,tipoFalla):
    propiedades = tipoFalla["colPropsAsociadas"]
    if len(propiedades) == 0:
      msg = "Atributos insuficientes para tipo de falla:\n %s" % tipoFalla["valor"]
      raise ExcepcionTipoFallaIncompleta(msg)

    contieneCriticidad = False
    contieneTipoMaterial = False
    for p in propiedades:
      #print "Propiedad actual antes: %s\n" % p
      cadenaProp = utils.escaparCaracteresEspeciales(p)
      prop = json.loads(cadenaProp)
      if prop["clave"] == "criticidad":
        contieneCriticidad = True
      if prop["clave"] == "tipoMaterial":
        contieneTipoMaterial = True
        
    if not contieneCriticidad:
      msg = "Error TipoFalla %s \nsin ningun tipo de reparacion disponible" %\
            tipoFalla["valor"] 
      raise ExcepcionTipoFallaIncompleta(msg)
    if not contieneTipoMaterial:
      msg = "Error TipoFalla %s \nsin ningun tipo de material disponible" %\
            tipoFalla["valor"] 
      raise ExcepcionTipoFallaIncompleta(msg)



#BACKUP VERSION ANTERIOR!
#  def crearListaProps(self,listaProps):
#    print "En crearListaProps()...\n"
#    if len(listaProps) == 0:
#      msg = "Listado de tipos de falla incompleto" 
#      raise ExcepcionTipoFallaIncompleta(msg)

#    # Si la falla es valida, Se la crea
 #   # y se asocian las propidades a la misma.
#    for tipoFalla in listaProps:
#      self.validarPropsDeTipoFalla(tipoFalla)
#      falla = Propiedad(tipoFalla["clave"],tipoFalla["valor"])
#      for p in tipoFalla["colPropsAsociadas"]:
#        prop = json.loads(utils.escaparCaracteresEspeciales(p))
#        propiedad = Propiedad(str(prop["clave"].encode("utf-8")),
#                                str(prop["valor"].encode("utf-8")))
#        falla.asociarPropiedad(propiedad)
#      self.propsConfirmados.append(falla)

#  #Valida el atributo "colPropsAsociadas" para que contenga
#  # al menos un tipo de material y un tipo de reparacion.
##  def validarPropsDeTipoFalla(self,tipoFalla):
#    propiedades = tipoFalla["colPropsAsociadas"]
#    if len(propiedades) == 0:
#      msg = "Atributos insuficientes para tipo de falla:\n %s" % tipoFalla["valor"]
#      raise ExcepcionTipoFallaIncompleta(msg)
#
#    contieneTipoReparacion = False
#    contieneTipoMaterial = False
#    for p in propiedades:
#      #print "Propiedad actual antes: %s\n" % p
#      cadenaProp = utils.escaparCaracteresEspeciales(p)
##      
#      prop = json.loads(cadenaProp)
#      if prop["clave"] == "tipoReparacion":
#        contieneTipoReparacion = True
#      if prop["clave"] == "tipoMaterial":
#        contieneTipoMaterial = True

#    if not contieneTipoReparacion:
#      msg = "Error TipoFalla %s \nsin ningun tipo de reparacion disponible" %\
#            tipoFalla["valor"] 
#      raise ExcepcionTipoFallaIncompleta(msg)
#    if not contieneTipoMaterial:
#      msg = "Error TipoFalla %s \nsin ningun tipo de material disponible" %\
#            tipoFalla["valor"] 
#      raise ExcepcionTipoFallaIncompleta(msg)



  # Abre una BD en JSON con TinyDB y si esta esta vacia, se 
  # vacia la coleccion de propiedades del capturador.  
  def cargarAtributosDesdeBDLocal(self):
    db = TinyDB(LOCAL_BD_PROPS_CONFIRMADAS)
    listaElems = db.all()
    if len(listaElems) == 0:
      msg = "\nNo existen atributos locales \npara los tipos de falla"
      print msg
      self.propsConfirmados = ListadoPropiedades()
      raise ExcepcionSinDatosTiposFalla(msg)
    #self.apiClient.parsear_datos_confirmados()
    # Se crea la lista de propiedades y se guarda una copia local
    # en disco
    self.crearListaProps(listaElems)


  # Retorna True si existen propiedades cargadsa en la coleccion
  # de propiedades del capturador. Invocado desde main al cambiar
  # al screen de "Capturar falla nueva"
  def existenPropsCargadas(self):
    return len(self.propsConfirmados) > 0 

  #Retorna la lista de atributos dato un nombre de tipoFalla
  def getAtributosAsociados(self,nombreTipoFalla):
    props = []
    for tFalla in self.propsConfirmados:
      if tFalla.getValor() == nombreTipoFalla:
        props = tFalla.getColPropsAsociadas()
        break
    return props


  # Invocado desde propsFallaConfirmada.py al seleccionar los atributos
  # para el tipo de falla
  def sonPropiedadesValidas(self,tipoFalla,tipoReparacion,tipoMaterial):
    esTipoRepValido = esTipoMatValido = False
    atributos = self.getAtributosAsociados(tipoFalla)
    for a in atributos:
      if a.getValor() == tipoReparacion:
        esTipoRepValido = True
      if a.getValor() == tipoMaterial:
        esTipoMatValido = True
    if esTipoRepValido and esTipoMatValido:
      return True
    return False

  ################ METODO PARA ALAMCENAR CAPTURAS LOCALES CON OOBD ##################
  # https://pypi.python.org/pypi/ZEO/4.2.0b1
  # 1- Se instala zeo con pip
  # $ pip install zeo
  # Instalar: 
  # $ sudo pip install zope.testing zope.interface
  # 2- Se ejecuta el servidor zeo con: python runzeo -C zeo.config

  #Inicializacion del servidor:
  # import ZEO
  # addres,stop = ZEO.server(path='zeoServer/BDRECORRIDOS.bd') 
  # db = ZEO.DB(addr)
  # connection = db.open()
  # ....
  # connection.close()
  # stop()

  # Recorre la colCapturasTotales(incluye la colCapturasConfirmadas) y
  # retorna solo aquellas que no fueron marcadas como subidas.
  def obtenerCapturasNoSubidas(self):
    fallas = list() 
    for falla in self.colCapturasTotales:
      if not falla.estaSubida():
        fallas.append(falla)
    return fallas


  @staticmethod
  #Se guarda el recorrido con fallas informadas y confirmadas
  def persistirFallas(nameBD,fallas):
    print "En Capturador.persistirFallas()...\n"
    #Se bloquea el proceso padre hasta que se lea algo desde el PIPE 
    Capturador.almacenarCapturasEnDisco(nameBD,fallas)
    print "Guardadas las fallas!\n"


  @staticmethod
  def cargarRecorrido(nameBD):
    dicElems1,conn1,stop_function = Capturador.leerCapturasDesdeDisco(nameBD)
    # Se hace una copia profunda de los elementos leidos antes de cerrar la conexion
    # con la BD.
    dicElems = copy.deepcopy(dicElems1)
    Capturador.cerrarConexion(conn1,stop_function)
    return dicElems


  # Dada una coleccion de fallas detecta si la falla contiene todas
  # sus capturas .csv en disco, en path en el que fueron almacenadas
  # anteriormente.
  # Retorna la coleccion de itemfalla que tienen al menos una cap. valida
  # asociada y retorna True si existe al menos un itemfalla
  # que no pudo ser instanciado debido a que no tiene al menos una
  # cap. valida.
  @staticmethod
  def filtrarFallasConsistentes(colecccionFallas):
    print "Validando capturas...\n"
    colNueva = ListadoFallas()
    hayFallasCorruptas = False
    logger = utils.instanciarLogger(LOG_FILE_CAPTURAS_CORRUPTAS_DEFAULT)
    print "================================================\n"
    for falla in colecccionFallas:
      # Si valida las capturas de una falla y actualiza la coleccion de 
      # la misma con capturas que aun existen en disco.
      if falla.filtrarCapturasConsistentes(logger):
        colNueva.append(falla)
      else:
        hayFallasCorruptas = True
    return colNueva,hayFallasCorruptas


  @staticmethod
  def almacenarRecorrido(connection,colItemFalla,clave='recorridoInformados'):
    #Se crea la BD con un prefijo predefinido + fecha actual
    root = connection.root
    #Se crea la estructura por la cual se accedera a la colCapturas, 
    #definiendo un espacio de nombres "recorrido".
    root.recorridoInformados = BTrees.OOBTree.BTree()
    root.recorridoConfirmados = BTrees.OOBTree.BTree()
    indexInformada = indexConfirmada = 0
    for falla in colItemFalla:
      if isinstance(falla.getEstado(),Informada): 
        root.recorridoInformados[indexInformada] = falla
        indexInformada += 1 
      else:
        root.recorridoConfirmados[indexConfirmada] = falla
        indexConfirmada +=1
    #Se asientan los cambios en la BD
    transaction.commit()

  #Retorna una coleccion de itemFalla de la BD, pertenecientes a un recorrido
  @staticmethod
  def obtenerRecorrido(conn,clave):
    print "En obtenerRecorrido...\n"
    raiz = conn.root()
    colElems = list()
    for index in raiz[clave]:
      colElems.append(raiz[clave][index])
    return colElems


  @staticmethod
  def abrirConexion(nombre):
    addres,stop = ZEO.server(path=nombre)
    db = ZEO.DB(addres)
    connection = db.open()
    return connection,stop


  @staticmethod
  def cerrarConexion(connection,stop):
    connection.close()
    stop()
    print "Cerrando conexion!\n"

  #Almacena la coleccion actual de capturas en disco
  @staticmethod
  def almacenarCapturasEnDisco(name_db,colItemFalla):
    #Se forkea el proceso debido a que ZODB no permite el acceso
    # desde el mismo proceso a una falla  
    print "Inicio con name_db: %s\n" % name_db
    conn,stop_function = Capturador.abrirConexion(name_db)
    Capturador.almacenarRecorrido(conn,colItemFalla)
    Capturador.cerrarConexion(conn,stop_function)



  #Lee las capturas que estan informadas y confirmadas
  @staticmethod
  def leerCapturasDesdeDisco(name_db):
    #Se obtiene el recorrido
    print "Obteniendo recorrido...\n"
    conn1,stop_function = Capturador.abrirConexion(name_db)
    dicElems = {}
    dicElems["informados"] = Capturador.obtenerRecorrido(conn1,'recorridoInformados') 
    dicElems["confirmados"] = Capturador.obtenerRecorrido(conn1,'recorridoConfirmados') 
    print "Obtenido el recorrido con las capturas!\n"
    return dicElems,conn1,stop_function
    


# + Capturador > CapturadorInformado
#     -ColBachesInformados (Se envian la calle y/o altura y envia los informados en ese rango)
#     +solicitarInformados()
#
class CapturadorInformados(Capturador):
  def __init__(self,apiclientComun):
    Capturador.__init__(self,apiclientComun)
    self.colBachesInformados = ListadoFallas()
    self.estrategia = EstrategiaInformados()

  #def getColBachesInformados(self):
  #  return self.colBachesInformados
  
  def getColBachesInformados(self):
    print "sorted(self.colBachesInformados): %s\n" % sorted(self.colBachesInformados)
    print "self.colBachesInformados: %s\n" % self.colBachesInformados
    return self.colBachesInformados

  def inicializar_fallas(self):
    for obj in self.colBachesInformados:
      obj.is_selected = False
  
  def solicitarInformados(self,calle):
    print "Inicio de solicitarInformados()...\n"
    # Hace un GET al servidor para obtener todos los baches en una calle
    # Para probar esta parte ejecutar apiclient/servidor_json.py.
    dic_json = self.apiClient.getInformados(calle)
    for key,tupla in dic_json.iteritems():
      falla = ItemFalla()
      estado = Informada(tupla["id"],tupla["altura"],tupla["calle"])
      estado.cambiar(falla)
      if falla not in self.colBachesInformados:
        print "Falla con id %s no esta en colBachesInformados, agregando!\n" % falla.getEstado().getId()
        self.colBachesInformados.append(falla)
        #self.colBachesInformados = sorted(self.colBachesInformados,reverse=True)
    self.colBachesInformados.sort()
    self.inicializar_fallas()
    CapturadorInformados.mostrar_coleccion(self.colBachesInformados)
    return self.colBachesInformados



  #BACKUP!
  #def solicitarInformados(self,calle):
  #  try:
  #    print "Inicio de solicitarInformados()...\n"
      # Hace un GET al servidor para obtener todos los baches en una calle
      # Para probar esta parte ejecutar apiclient/servidor_json.py.
  #    dic_json = self.apiClient.getInformados(calle)
  #    for key,tupla in dic_json.iteritems():
  #      falla = ItemFalla()
  #      estado = Informada(tupla["id"],tupla["altura"],tupla["calle"])
  #      estado.cambiar(falla)
  #      if falla not in self.colBachesInformados:
  #        print "Falla con id %s no esta en colBachesInformados, agregando!\n" % falla.getEstado().getId()
  #        self.colBachesInformados.append(falla)
          #self.colBachesInformados = sorted(self.colBachesInformados,reverse=True)
  #    self.colBachesInformados.sort()
  #    self.inicializar_fallas()
  #    CapturadorInformados.mostrar_coleccion(self.colBachesInformados)
  #  except ExcepcionAjax, e:
  #    controlador = App.get_running_app()
  #    controlador.mostrarDialogoMensaje(title="Error en solicitud al servidor",
  #                                        text= e.message)
  #  return self.colBachesInformados



  # Asocia la falla con la captura recien realizada.
  # capturadorinformados.asociarFalla()
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
      return self.capturar(data, dir_trabajo, nombre_captura,itemFalla)
      print "Fin de asociarFalla()"

  @staticmethod
  def mostrar_coleccion(colInformados):
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    print "\n\nMostrando la coleccion despues de solicitarInformados()...\n"
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    for obj in colInformados:
      obj_id = obj.getEstado().getId()
      obj_calle = obj.getEstado().getCalle()
      obj_altura = obj.getEstado().getAltura()
      print "Id falla: ",obj_id,"; Calle:",obj_calle,"; Altura: \n",obj_altura
    print "---------------------------------------------------------------\n"
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    print "\n\nFin de muestra de la coleccion solicitarInformados()...\n"
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

  def capturar(self,dataSensor, dir_trabajo, nombre_captura,item_falla):
    cap = Captura(nombre_captura,dir_trabajo,FORMATO_CAPTURA, EXTENSION_ARCHIVO)
    item_falla.registrarCaptura(dataSensor,cap,self)
    return cap.getFullPathCaptura(),cap.getFullPathCapturaConv()

#Agregado metodo para captura de falla informada.
#NOTA: Difiere del de falla nueva porque no almacena latitud ni longitud y no utiliza la api de geofencing.
# Se instancia la captura(con los valores de la view anterior),
# se almacena en disco y se se agrega a la lista de capturas del 
# capturador.
# Se indica a la falla que registre su captura, la alamcene en disco y
# la agregue a su colCapturas.
