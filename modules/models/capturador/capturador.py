# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.app import App

import sys,os
from apiclient1 import ApiClientApp,ExcepcionAjax
from kivy.adapters.models import SelectableDataItem
from constantes import *
from utils import *
from captura import *
from estadofalla import *
from geofencing import *
from estrategia import *

from json import JSONEncoder,JSONDecoder
import json

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
from apiclient1 import *


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

class ListadoPropiedades(list):
  """Los objetos de esta clase representan un listado de objetos que representan
    las posibles propiedades de una falla con estado Confirmada. """

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

  def getCantPropsTipoFalla(self,nombreProp):
    """Cuenta la cantidad de propiedades maxima entre los distintos tipos de falla
        y retorna la cantidad maxima de esa propiedad, entre todos los tipos de falla."""
    cantMaxima = 0
    for tipoFalla in self:
      cantidadActual = tipoFalla.getCantProps(nombreProp) 
      if cantMaxima < cantidadActual:
        cantMaxima = cantidadActual
    print "Cantidad maxima de propiedades: %s es: %s\n" % (nombreProp,cantMaxima)
    return cantMaxima

  def getTipoFallaPorValor(self,nombreTipoFalla):
    """Retorna la referencia a una propiedad "tipoFalla" en base al nombre. """
    for tipoFalla in self:
      if tipoFalla.getValor() == nombreTipoFalla:
        return tipoFalla
    return None

  def getPropsAsociadasATipoFalla(self,nombreTipoFalla,nombreSubPropiedad):
    """Obtiene las subpropiedades de un tipo de falla dado su nombre y el de su subpropiedad.
        
        Ejemplos de invocacion de este tipo de metodo son las siguientes.

        getPropsAsociadasATipoFalla("bache","tipoMaterial")
        getPropsAsociadasATipoFalla("bache","criticidad")."""
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
from tinydb import TinyDB
import json

class Propiedad(object):
  """Esta clase representa los atributos de una propiedad necesaria para dar de alta
      en la aplicacion web un tipo de falla con estado Confirmada. """

  def __init__(self,myID,clave,valor,estaTipoFallaHabilitada):
    print "en constructor propiedad!"
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

  def estaHabilitada(self):
    return self.estaPropHabilitada

  # 
  def getPropsAsociadasPorNombre(self,nombreSubPropiedad):
    """Obtiene las subpropiedades de un tipo de falla dado su nombre y el de 
        su subpropiedad."""
    subProps = []
    for subProp in self.colPropsAsociadas:
      if subProp.getClave() == nombreSubPropiedad:
        subProps.append(subProp)
        #subProps.append(subProp.getValor())
    return subProps

  def getCantProps(self,nombreProp):
    """Retorna la cantidad de propiedades que tiene la propiedad actual con un nombre dado.
        Se emplea principalmente para las propiedades base(inmediatas) de los tipos de falla. """
    cantProps = 0
    for prop in tipoFalla.getColPropsAsociadas():
      if prop["clave"] == nombreProp:
        cantProps += 1
    return cantProps

  def toDict(self):
    """Convirte a diccionario la propiedad y sus atributos asociados."""
    dic = {"id": self.id,"clave": self.clave,"valor": self.valor,
            "colPropsAsociadas": []}
    for e in self.colPropsAsociadas:
      #dic["colPropsAsociadas"].append(str(e))
      dic["colPropsAsociadas"].append(e.toDict())
      print "Agregado elemento para backup propiedades: %s; type(e): %s\n" % (e,type(e))
      print "diccionario de la propiedad: %s; type(dic): %s\n" % (e.toDict(),type(e.toDict()))
    return dic

  def serializar(self):
    """Convierte la propiedad a formato JSON valido para almacenar en la BD local."""
    return json.dumps(str(self))

  def getValor(self):
    return self.valor

  def getColPropsAsociadas(self):
    return self.colPropsAsociadas

  def asociarPropiedad(self,p):
    self.colPropsAsociadas.append(p)

  def guardar(self,tinyDB):
    """Guarda una propiedad en la BD local serializada en formato json."""
    tinyDB.insert(self.toDict())

  def getClave(self):
    return self.clave

class ListadoFallas(list):
  """Clase para una listado de elementos ItemFalla."""  
  
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
  """Clase que representa a una Falla, y permite controlar el estado y realizar
    comparaciones entre los distintos tipos implementados. """

  def __init__(self, is_selected=False, **kwargs):
    #NOTA: is_selected se modifica cuando el usuario selecciona una itemFalla para subir al servidor. 
    super(ItemFalla, self).__init__(is_selected=is_selected, **kwargs)
    self.estado = None
    # Coleccion de objetos "Captura" asociados a la falla
    self.colCapturas = []
    self.estaSubidaAlServidor = False # Flag que indica si se subio o no una falla
                                      # al servidor.

  def __str__(self):
    cad = "-->{ 'estado': { %s }, 'capturas':  %s , 'is_selected': %s , 'estaSubidaAlServidor': %s }<--    " %\
        (str(self.estado),self.colCapturas,self.is_selected,self.estaSubidaAlServidor)
    return cad

  def __cmp__(self,other):
    print "En __cmp__() de itemfalla, con self: %s; other: %s; valor other: %s\n" % \
        (type(self),type(other), other)
    if isinstance(self.estado,other.getEstado().__class__):
      print "Son del mismo estado!\n"
      return self.estado.comparar(other)
    else:
      print "Son de distinto estado!\n"
      return -1

  def desSeleccionar(self):
    self.is_selected = False

  def seleccionar(self):
    self.is_selected = True


  def estaSubida(self):
    return self.estaSubidaAlServidor

  def marcarComoSubida(self):
    self.estaSubidaAlServidor = True

  def asignarPropiedades(self):
    """Asigna el tipofalla,tipoReparacion y tipoMaterial especificado por el usuario."""
    controlador = App.get_running_app()
    self.estado.setTipoFalla(controlador.getData("tipoFalla"))
    self.estado.setCriticidad(controlador.getData("criticidad"))
    self.estado.setTipoMaterial(controlador.getData("tipoMaterial"))
    print "Asignadas propiedades al estado de falla confirmada!"
    print "tipoFalla: %s; tipoReparacion: %s; tipoMaterial: %s\n" %\
          (controlador.getData("tipoFalla"),controlador.getData("criticidad"),
            controlador.getData("tipoMaterial"))

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

  def obtenerCapturasConsistentes(self):
    """Retorna una lista con las capturas consistentes asociadas a un ItemFalla."""
    miColCapturas = list()
    for cap in self.colCapturas:
      print "Iterando captura: %s\n" % cap
      if cap.esConsistente():
        miColCapturas.append(cap)
        print "agregando captura consistente: %s\n" % cap
    return miColCapturas

  def getColCapturas(self):
    """Retorna la lista de capturas asociadas a un ItemFalla."""
    return self.colCapturas


  def setColCapturas(self,col):
    """Setea la coleccion de capturas asociadas a un ItemFalla"""
    self.colCapturas = col


  def registrarCaptura(self,dataSensor,cap,capturador):
    """Registra la captura en disco, la agrega a la coleccion del elemento ItemFalla actual y registra la falla."""
    controlador = App.get_running_app()
    cap.almacenarLocalmente(dataSensor,capturador,controlador.args.tipoCaptura)
    self.estado.registrar(self,capturador,cap)
    self.getEstado().mostrar_capturas_asociadas(self)


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
    """Si la falla esta seleccionada, se convierte y se envia al servidor con todas sus capturas
        asociadas como un POST de tipo mime: multipart/form-data. """
    print "Inicio ItemFalla.enviar() para la falla:\n %s\n" % self
    controlador = App.get_running_app()
    logger = utils.instanciarLogger(LOG_FILE_CAPTURAS_INFO_SERVER)
    coleccionCapturas = self.obtenerCapturasConsistentes()
    if self.is_selected and len(coleccionCapturas):
      # Se convierte cada captura en un csv y luego se envia la falla en 
      # formato JSON al servidor.
      capturasConvertidas = []
      cantCapturasAEnviar = len(coleccionCapturas)

      #BACKUP!
      #Se marca el itemfalla como subido al servidor
      #self.marcarComoSubida()
      for i in xrange(0,len(coleccionCapturas)):
        #Si se supera el tamanio maximo de una peticion POST o si se supera
        # la cantidad de archivos permitida por peticion, se envia la peticion 
        # con la cant. actual de archivos y se vacia capturasConvertidas 
        # para seguir preparando las proximas peticiones.
        nombreArchCsv = coleccionCapturas[i].getFullPathCapturaConv()
        capturasConvertidas.append(nombreArchCsv) 
        cantCapturasAEnviar -= 1

        # Si los bytes_actuales de la colecccion de capturas + el tamanio de la captura actual
        # superan el MAX_POST_SIZE se invoca al api_client para su envio.
        # Sino, se continuan agregando mas capturas para enviar.
        #
        bytes_actuales_cap = utils.calcularTamanio([coleccionCapturas[i].getFullPathCapturaConv()])
        bytes_actuales_col = utils.calcularTamanio(capturasConvertidas)

        if bytes_actuales_col + bytes_actuales_cap >= MAX_POST_REQUEST_SIZE or \
                    len(capturasConvertidas) == MAX_FILE_UPLOADS_FOR_REQUEST or \
                      cantCapturasAEnviar == 0:
          #Se piden lso campos formateados para el envio a la falla
          falla_formateada = self.getDicFalla()
          try:
            bytes_leidos = api_client.postCapturas(url_server,
                                                falla_formateada,
                                                capturasConvertidas,
                                                bytes_leidos,
                                                logger)
          except ExcepcionDesconexion as e:
            print "Atrape la ExcepcionDesconexion!!!\n"
            raise ExcepcionDesconexion(e.message)
          
          capturasConvertidas = []
          print "Despues de enviar bytes!!\n"

        # NOTA: Se retorna de la funcion unicamente cuando se han enviado todos los 
        # objetos captura asociados a la falla
        if controlador.canceladaSubidaArchivos and cantCapturasAEnviar == 0:
          print "Cancelada la subida de archivos desde itemFalla.enviar()...\n"
          return 
      
      #Se marca el itemfalla como subido al servidor
      self.marcarComoSubida()
    return bytes_leidos

  def calcularTamanio(self):
    """Retorna el tamanio en bytes de los archivos asociados a una captura.
        Se invoca para actualizacion de la progressbar y el label con los bytes enviados/totales."""
    mybytes = 0
    nombres_capturas = []
    for captura in self.colCapturas:
      if captura.esConsistente():
        arch_csv = captura.getFullPathCapturaConv()
        nombres_capturas.append(arch_csv)
    mybytes = utils.calcularTamanio(nombres_capturas)
    return mybytes

  def setCalleEstimada(self,calle):
    self.estado.setCalleEstimada(calle)

  def setRangosEstimados(self,rango1,rango2):
    self.estado.setRangosEstimados(rango1,rango2)

  def getDicFalla(self):
    """Obtiene el diccionario completo para enviar cada falla al servidor.
        
        Es invocado desde enviar() y retorna el diccionario "falla_formateada" que
        se usa en ese metodo."""
    return self.estado.getDicFallaEncoded()

  def filtrarCapturasConsistentes(self,logger):
    """Valida las capturas asociadas a una falla, comprobando que existan en
        disco, retornando TRUE si al menos existe una captura valida asociada a la
        falla y FALSE en caso contrario."""
    print "En filtrarCapturas consistentes!\n"
    colCapsValidas = list()
    for cap in self.colCapturas:
      pathCsv = cap.getFullPathCapturaConv()
      print "Leyendo captura: %s ; path.exists(pathCsv):%s \n" % (pathCsv,
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


  #ItemFalla.descartar()
  # Recibe una coleccion de nombres de las capturas (pcds) que contienen los objetos
  # "Captura" asociados a los objetos "ItemFalla".
  #def descartar(self,colItemsFalla):
  def descartar(self,colNombresCapturasPcd):
    """Se descartan los objetos 'Captura' asociados al objeto 'Itemfalla' actual
        solo si los pcds asociados a cada 'Captura' se encuentran en colNombresCapturasPcd"""
    print "En itemfalla.descartar()\n"
    capEstaDescartada = False
    #Por cada captura de cada itemFalla...
    print "La coleccion 'colNombresCapturasPcd' tiene: \n"
    for e in colNombresCapturasPcd:
      print "tipo: %s; elemento: %s\n" % (type(e),e)

    print "La coleccion 'self.colCapturas' tiene: \n"
    for e in self.colCapturas:
      print "tipo: %s; elemento: %s\n" % (type(e),e)
      
    #colTotalObjCaptura = list()
    #for i in colNombresCapturasPcd:
    #  colTotalObjCaptura += i.getColCapturas()

    # Se iteran todos los objetos Captura asociados al ItemFalla actual y
    # se los descarta
    for cap in self.colCapturas:
      #if cap in colTotalObjCaptura:
      if cap.getFullPathCaptura() in colNombresCapturasPcd:
        print "Iterando Captura con path: %s\n" % cap.getFullPathCaptura() 
        print "Captura encontrada! en: %s con itemFalla: %s \n" % (self.colCapturas,self)
        cap.descartar(self)
        capEstaDescartada = True
        print "Descartada correctamente! \n"
        Capturador.mostrarCapturas(self.colCapturas)
        break
    
    if len(self.colCapturas) == 0:
      print "len(itemFalla.getColCapturas()): %s\n " % len(self.colCapturas)
      #colItemsFallaADescartar.append(itemFalla)
      return (self,capEstaDescartada)
      print "descartando itemFalla...\n"
    else:
      return (None,capEstaDescartada)

    print "Fin itemfalla.descartar()\n"

  def comprobarConsistencia(self):
    """Comprueba la consistencia de los archivos .pcd en disco con respecto a los
        objetos Captura en memoria, asociados a cada falla. """
    existenCapsInconsistentes = False
    print "Comprobando consistencia del item falla:     %s\n\n" % self
    for cap in self.colCapturas:
      if not cap.existeEnDisco():
        cap.marcarComoInconsistente()
        existenCapsInconsistentes = True
        print "captura inconsistente encontrada!\n"
    print "fin de comprobacion ...\n"
    return existenCapsInconsistentes

class Capturador(object):
  """Clase que representa a un capturador de fallas para fallas. """
  
  def __init__(self,apiclientComun,BDLocal=None,**kwargs):		
    #NOTA: Tanto colCapturasTotales como colCapturasConfirmadas 
    # contienen elementos "ItemFalla", que tienen objetos "Captura" asociados. 
    self.colCapturasTotales = [] #Todas las capturas hechas informadas y confirmadas.
    self.colCapturasConfirmadas = [] # Aquellas fallas "confirmadas"(seleccionadas) para enviar al servidor 
    self.apiClient = apiclientComun
    # self.apiClient = ApiClientApp()
    self.estrategia = EstrategiaConfirmados()
    self.api_geo = GeofencingAPI()
    self.bdLocalMuestras = BDLocal
    print "Inicializado %s" % self.__class__.__name__
    self.propsConfirmados = ListadoPropiedades() #Listado de objetos que se asocian
                                                  # con los atrigbutos de un tipoFalla confirmada
                                                  # y que son obligatorios(tipo reparacion y 
                                                  # tipo de material).

  def inicializarBDLocal(self,fullPathBD = None):
    """Inicializa la BDLocal con las coordenadas geograficas, fecha y nombre de captura
     (en formado JSON) del capturador actual."""
    if fullPathBD is None:
      self.bdLocalMuestras.inicializar()
      return
    self.bdLocalMuestras.inicializar(fullPathBD = fullPathBD)

  def getBDLocalMuestras(self):
    return self.bdLocalMuestras


  def getPropsConfirmados(self):
    """Retorna los tiposFalla con todas sus propiedades."""
    return self.propsConfirmados

  def setPropsConfirmados(self,p):
    """Retorna los tiposFalla con todas sus propiedades."""
    self.propsConfirmados = p

  def reestablecerApiClient(self):
    """Reestablece el contador de bytes totales a enviar a cero."""
    self.apiClient.reestablecerApiClient()
  
  def setCantBytesTotales(self,bytes_totales_a_enviar):
    """Se delega el metodo de apiClient que mantiene este atributo."""
    self.apiClient.setCantBytesTotales(bytes_totales_a_enviar)

  def getColCapturasTotales(self):
    return self.colCapturasTotales

  def setColCapturasTotales(self,col):
    self.colCapturasTotales = col

  def getColCapturasConfirmadas(self):
    return self.colCapturasConfirmadas

  def getCantidadCapturas(self,archivo_a_buscar,dirTrabajo,extensionArchivo):
    """ Retorna la cantidad de archivos que tienen un nombre dado
        en el directorio de trabajo especificado. Se detecta la
        extension desde la derecha del archivo."""
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

  # Capturador.asociarFalla()
  def asociarFalla(self,data, dir_trabajo, nombre_captura,id_falla,gps):
    """Asocia el ItemFalla con la captura recien realizada,
      se cambia el estado de la falla a Confirmada, y se utiliza
      API_GEO (Obtener LATITUD y LONGITUD del GPS). """
    print "En capturador FALLA NUEVA!!!\n"
    falla = ItemFalla()
    if gps == TIPO_GPS_DEFAULT:
      # COORDENADAS DE PRUEBA ARTIFICIALES
      latitud_prueba,longitud_prueba = self.api_geo.getLatLong()
    else:
      # COORDENADAS DE PRUEBA REALES
      latitud_prueba,longitud_prueba = self.api_geo.obtenerLatitudLongitud()
    
    estado = Confirmada(latitud_prueba,longitud_prueba).cambiar(falla)
    #Se agregan las propiedades a la falla
    falla.asignarPropiedades()
    return self.capturar(data, dir_trabajo, nombre_captura,falla,latitud_prueba,
      longitud_prueba)

  # capturador.capturar() invocado desde main.threadCapturarFalla()
  def capturar(self,dataSensor, dir_trabajo, nombre_captura,item_falla,latitud,longitud):
    """Metodo de captura de fallas por defecto, para fallas con estado Confirmada."""
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
    self.bdLocalMuestras.agregar(latitud,longitud,cap.getFullPathCaptura())
    print "Guardado archivo .pcd en BD_JSON!"
    print ""
    return cap.getFullPathCaptura()

  def filtrarCapturas(self):
    """Filtra las colCapturasTotales y agrega solamente las capturas seleccionadas en el listview
        a la colCapturasConfirmadas."""
    # Se vacian la coleccion de capturas confirmadas antes
    self.colCapturasConfirmadas = []
    self.estrategia.filtrar(self.colCapturasConfirmadas,self.colCapturasTotales,self)	 	
	

  def obtenerDirEstimada(self,itemFalla):
    """Obtiene la calle y altura de cada falla confirmada y las establece
        en el estado. """
    calle,rangoEstimado1,rangoEstimado2 = self.apiClient.obtenerDirEstimada(itemFalla.getEstado().getLatitud(),
                    itemFalla.getEstado().getLongitud())
    itemFalla.setCalleEstimada(calle)
    itemFalla.setRangosEstimados(rangoEstimado1,rangoEstimado2)

  # capturador.enviarCapturas()
  def enviarCapturas(self,url_server):
    """Envia las fallas registradas al servidor."""
    print "En capturador.enviarCapturas()\n"
    controlador = App.get_running_app()
    bytes_leidos = 0
    msgError = ""
    #Se obtienen las fallas confirmadas para envio
    for falla in self.getColCapturasConfirmadas():
      print "\nEnviando falla= %s; falla.is_selected=%s)\n" % (falla,falla.is_selected)
      if falla.is_selected:
        bytes_leidos += falla.enviar(URL_UPLOAD_SERVER,self.apiClient,bytes_leidos)
    
    print "Fin de capturador.enviarCapturas()!\n"
    


  def calcularTamanioCapturas(self):
    """Calcula el tamanio de las capturas asociadas a cada una de las fallas
        confirmadas para envio al server."""
    bytesEnviar = 0
    for falla in self.getColCapturasConfirmadas():
      if falla.is_selected:
        bytesEnviar += falla.calcularTamanio()
    return bytesEnviar

  # Capturador.descartar(capturas)
  # Recibe una lista de strings con los nombres de archivos de captura para descartar
  # iterando todos los objetos ItemFalla y descartando los objetos captura necesarios
  # asociadas a estas
  def descartar(self,capturas):
    """Este metodo descarta la captura de memoria y de disco. """
    print "Inicio de capturador.descartar()\n" 
    capEstaDescartada = False
    colItemsFallaADescartar = list()

    for itemFalla in self.colCapturasTotales:
      print "verificando long. capturas de itemfalla: \n\n %s \n" % itemFalla 
      #Descarta la Captura en itemFalla solo si esta en su coleccion
      tuplaResultado = itemFalla.descartar(capturas)
      capEstaDescartada = tuplaResultado[1]
      #Si no es None el resultado, se debe descartar itemFalla
      if tuplaResultado[0] is not None:
        print "Se eliminara de la coleccion itemFalla: %s\n" % tuplaResultado[0]
        colItemsFallaADescartar.append(tuplaResultado[0])
        
    print "colItemsFallaADescartar -->:\n\n"
    for miFalla in colItemsFallaADescartar:
      print "miFalla: %s \n" % miFalla

    #Se descartan las fallas que no contienen capturas
    self.descartarFallaSinCaps(colItemsFallaADescartar)
    print "Fin de capturador.descartar()\n"
    return capEstaDescartada


  # Capturador.descartarFallaSinCaps()
  def descartarFallaSinCaps(self,colItemsFallaADescartar):
    """Este metodo elimina aquellos itemFalla que no tienen al menos una 
       captura asociada. Se sobreescribe en esta clase ya que solo se usa para
       las fallas Confirmadas, debido a que los itemFalla de este tipo
       existen si tienen al menos una captura, mientras que las del tipo
       Informadas pueden existir incluso sin capturas asociadas. """
    print "En Capturador.descartarFallaSinCaps()!\n"
    # NOTA IMPORTANTE: Se recorren todas las las FALLAS CONFIRMADAS que no tienen al menos una captura,
    # y se borran del capturador. Para las FALLAS INFORMADAS, se debe
    # mantener el ITEMFALLA en la coleccion del capturador Informados.
    self.mostrarColItemFalla()
    print "len(self.colCapturasTotales) antes: %s\n" % len(self.colCapturasTotales)
    for falla in colItemsFallaADescartar:
      print "Descartando captura: %s\n" % falla
      self.colCapturasTotales.remove(falla)
    print "len(self.colCapturasTotales) despues: %s\n" % len(self.colCapturasTotales)
    self.mostrarColItemFalla()

  def mostrarColItemFalla(self):
    print "Inicio de mostrarColItemFalla() con capturador.colCapturasTotales ---> \n\n"
    for falla in self.colCapturasTotales:
      print "falla: %s \n\n" % falla
    print "Fin de mostrarColItemFalla() con capturador.colCapturasTotales \n"
  		
  @staticmethod
  def mostrarCapturas(colCaps):
    print "En mostrarCapturas()\n"
    for c in colCaps:
      print "captura asociada a la falla: %s \n" % c.getFullPathCaptura()
    print "Fin mostrarCapturas()\n"

  # Invocado desde main._callbackConservarCapsSubidas().
  # Capturador.descartarCapsSubidas()
  def descartarCapsSubidas(self):
    """Elimina los itemFalla de la colCapturasConfirmadas
        luego de haberlas registrado en el servidor."""
    colItemFalla = self.colCapturasConfirmadas
    #Se obtienen los nombres de los pcds asociados a los objetos "Captura"
    colNombresCapturasPcd = []
    for itemFalla in colItemFalla:
      for cap in itemFalla.getColCapturas():
        colNombresCapturasPcd.append(cap.getFullPathCaptura())

    for f in self.colCapturasConfirmadas:
      print "Iterando desde capturador.descartarCapsSubidas()\n"
      print "falla: %s\n" % f
      if f.is_selected and f.estaSubida():
        #f.descartar(colItemFalla)
        f.descartar(colNombresCapturasPcd)
        print "\n\nMostrando la coleccion colItemFalla despues de borrar una falla subida:\n%s\n"
    
    # Se obtienen las capturasConfirmadas no subidas (no seleccionadas) y
    # se actualiza la lista de capturas confirmadas con esas fallas.
    fallasNoDescartadas = self._filtrarCapturasConservadas(colItemFalla)
    self.colCapturasConfirmadas = fallasNoDescartadas
    ItemFalla.mostrarColItemFalla(colItemFalla)

  def _filtrarCapturasConservadas(self,colItemFalla):
    """Filtra aquellas capturas que no estan subidas."""
    fallasNoDescartadas = list()
    for f in colItemFalla:
      if not f.is_selected:
        fallasNoDescartadas.append(f)
    return fallasNoDescartadas
    
  #Invocado desde main.threadGetPropsConfirmadas()
  def obtenerPropsConfirmadas(self):
    dicPropsConfirmados = self.apiClient.getPropsConfirmados()
    print "Obtenidas las propiedades confirmadas!\n\n"
    print dicPropsConfirmados
    self.crearListaProps(dicPropsConfirmados,escaparCaracteres = True)

  def crearBackupConfirmados(self):
    """Vacia la BD Confirmadas y la actualiza con los datos
        que leyo del servidor."""
    print  "Inicio tinydb!!!\n"
    tinydb = TinyDB(LOCAL_BD_PROPS_CONFIRMADAS)
    if len(tinydb.all())>0:
      print "Vaciando BD TinyDB antigua...\n"
      tinydb.purge()
    print "Guardando elementos desde BD en BD_CONFIRMADA.json ...\n"
    self.propsConfirmados.guardar(tinydb)
    print "Creado un resplado de las propiedades de las fallas confirmadas!\n"

  def crearListaProps(self,listaProps,escaparCaracteres = False):
    """Retorna una lista de objetos "Propiedad" consistentes con los requerimientos para dar de alta
   un tipo de falla confirmada.
  
   Valida si el json obtenido desde el servidor es valido:
    -Debe contener al menos un tipoFalla en la coleccion general
    -Y cada tipo de falla debe tener asociado al menos un tipo de 
   reparacion y un tipo de material. Sino se debe usar una copia
   de la BD anterior.
  
  El formato de datos a parsear es el siguiente:
        listadoTiposFalla = [
           {
           "clave": "tipoFalla",
           "valor": "Bache",
           "colPropsAsociadas": [
                 {"clave": "tipoReparacion", "valor":"Sellado"},
                 {"clave": "tipoReparacion", "valor":"Cementado"},
                 {"clave": "tipoMaterial", "valor":"Pavimento asfaltico"]},
                 {"clave": "tipoMaterial", "valor":"Cemento"},
                 ...
                 ]
         },
           ... 
        ]"""
    print "En crearListaProps()...\n"
    if len(listaProps) == 0:
      msg = "Listado de tipos de falla incompleto" 
      raise ExcepcionTipoFallaIncompleta(msg)

    # Si la falla es valida, Se la crea y se asocian las propidades a la misma.
    for tipoFalla in listaProps:
      estaTipoFallaHabilitada = False
      if int(tipoFalla["id"]) in IDS_TIPOS_FALLA_HABILITADOS:
        estaTipoFallaHabilitada = True

      print "Validando propiedades...\n"
      self.validarPropsDeTipoFalla(tipoFalla)

      falla = Propiedad(tipoFalla["id"],tipoFalla["clave"],tipoFalla["valor"],
                          estaTipoFallaHabilitada)
      print "asociando props a subpropiedades: %s\n" % tipoFalla["colPropsAsociadas"]

      #Se asocian las propiedades que pueda tener la propiedad del tipo de falla
      for p in tipoFalla["colPropsAsociadas"]:
        print "Iterando colPropsAsociadas...\n"
        print "type(p): %s\n" % type(p)
        #TODO: DESCOMENTAR ESTO!
        #prop = json.loads(utils.escaparCaracteresEspeciales(p))
        prop = {}
        if escaparCaracteres:
          print "Escapando caracteres especiales desde servidor!\n"
          prop = json.loads(utils.escaparCaracteresEspeciales(p))
        else:
          print "No es necesario escapar. Props cargadas localmente...\n"
          prop = p

        propiedad = Propiedad(  prop["id"],
                                str(prop["clave"].encode("utf-8")),
                                str(prop["valor"].encode("utf-8")),
                                estaTipoFallaHabilitada)

        print "leidas propiedades principales falla!\n"
        print "prop: %s\n\n\n" % prop
        if prop.has_key("colPropsAsociadas") and (len(prop["colPropsAsociadas"]) > 0):
          print "La criticidad tiene propiedades!\n"
         
          for s in prop["colPropsAsociadas"]:
            print "subpropiedad de la criticidad: %s\n" % s
            print "s['clave']: %s\n" % s["clave"]
            print "s['valor']: %s\n" % s["valor"]
            subProp = Propiedad(1,s["clave"],s["valor"],estaTipoFallaHabilitada)
            print "instanciada!\n"
            propiedad.asociarPropiedad(subProp)
            print "asociada!\n"
            print "propiedad.colPropsAsociadas: %s\n" % propiedad.colPropsAsociadas

        print "Creada propiedad asociada: %s ...\n" % propiedad
        falla.asociarPropiedad(propiedad)
      self.propsConfirmados.append(falla)
    print "Fin de crearListaProps()...\n"
    print "self.propsConfirmados tiene: \n\n%s\n" % self.propsConfirmados

  def validarPropsDeTipoFalla(self,tipoFalla):
    """Valida el atributo "colPropsAsociadas" para que contenga
        al menos un tipo de material y un tipo de reparacion."""
    propiedades = tipoFalla["colPropsAsociadas"]
    print "type(propiedades): %s\n" % type(propiedades)
    print "propiedades: %s\n" % propiedades
    if len(propiedades) == 0:
      msg = "Atributos insuficientes para tipo de falla:\n %s" % tipoFalla["valor"]
      raise ExcepcionTipoFallaIncompleta(msg)

    contieneCriticidad = False
    contieneTipoMaterial = False
    for p in propiedades:
      # TODO: DESCOMENTAR ESTO!
      #cadenaProp = utils.escaparCaracteresEspeciales(p)
      #print "analizado p correctamente!\n"
      #prop = json.loads(cadenaProp)
      #prop = json.loads(cadenaProp)
      prop = p
      print "prop cargado!"
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

  def cargarAtributosDesdeBDLocal(self):
    """Abre una BD en JSON con TinyDB y si esta esta vacia, se 
        vacia la coleccion de propiedades del capturador."""
    db = TinyDB(LOCAL_BD_PROPS_CONFIRMADAS)
    listaElems = db.all()
    if len(listaElems) == 0:
      msg = "\nNo existen atributos locales para los tipos de falla\n"
      print msg
      self.propsConfirmados = ListadoPropiedades()
      raise ExcepcionSinDatosTiposFalla(msg)
    # Se crea la lista de propiedades y se guarda una copia local
    # en disco
    
    print "Los atributos leidos desde tinydb son: %s\n" % listaElems
    print type(listaElems)
    #for tipoFalla in listaElems:
      #Clase de tipoFalla al leer desde tinydb <class 'tinydb.database.Element'>
      #print "tipoFalla: %s; %s\n\n" % (tipoFalla,type(tipoFalla))

    #dicElementos = self._convertirElementosAJSON(listaElems)
    dicElementos = listaElems
    print "El listado de dicElementos es --->\n\n"
    for e in dicElementos:
      print "%s; \n" % e
    #self.crearListaProps(dicElementos)
    #TODO: DESCOMENTAR ESTO! 
    self.crearListaProps(listaElems,escaparCaracteres = False)


  def _convertirElementosAJSON(self, listaElems):
    """ Metodo interno para convertir los objetos de la clase tinydb.database.Element
    a un diccionario .JSON con strings. Necesario para la lectura de un archivo local
    JSON con tinydb."""
    listadoFinal = []
    for elemento in listaElems:
      dicStrings = {}
      #Se itera cada elemento "Element" y se produce un diccionario 
      print "Iterando elemento de tipo: %s\n" % type(elemento)
      print "Valor del elemento -->\n\n%s\n" % elemento
      for key,value in elemento.iteritems():
        print "key: %s; value: %s, type(value): %s\n" % (key,value,type(value))
        #dicStrings[key] = value
        clave = str(key.encode("utf-8"))
        print "clave: %s\n" % clave
        if type(value) is list:
          print "Codificando listado...\n"
          colPropsAsociadas1 = []
          for e in value:
            print "elemento del listado: %s; %s\n" % (e,type(e))
            print str(e.encode("utf-8"))
            print "\n\n-------------------------------------------->"
            colPropsAsociadas1.append(str(e.encode("utf-8")))
            
          print "ColPropsAsociadas1: %s\n" % colPropsAsociadas1
          dicStrings[clave] = colPropsAsociadas1  
          #json.loads(e,object_hook = self._decodifPropsJSON)
        else:
          valor = str(value.encode("utf-8"))
          dicStrings[clave] = valor

      listadoFinal.append(dicStrings)
    return listadoFinal

  #def _decodifPropsJSON(self,dic):
  #  print "diccionario -->\n"
  #  print dic
  #  print type(dic)

  # Invocado desde main al cambiar al screen de "Capturar falla nueva.
  def existenPropsCargadas(self):
    """Retorna True si existen propiedades cargadsa en la coleccion
        de propiedades del capturador. """
    print "En existenPropsCargadas(): %s\n" % len(self.propsConfirmados)
    return len(self.propsConfirmados) > 0 


  ################ METODO PARA ALAMCENAR CAPTURAS LOCALES CON OOBD ##################
  
  def obtenerCapturasNoSubidas(self):
    """Recorre la colCapturasTotales(incluye la colCapturasConfirmadas) y
        retorna solo aquellas que no fueron marcadas como subidas."""
    fallas = list() 
    for falla in self.colCapturasTotales:
      if not falla.estaSubida():
        fallas.append(falla)
    return fallas

  @staticmethod
  def persistirFallas(nameBD,fallas):
    """Se guarda el recorrido con fallas informadas y confirmadas."""
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

  @staticmethod
  def filtrarFallasConsistentes(colecccionFallas):
    """Dada una coleccion de fallas detecta si la falla contiene todas
      sus capturas en disco, en el path en el que fueron almacenadas
      anteriormente.

    Retorna la coleccion de itemfalla que tienen al menos una captura valida
    asociada y retorna True si existe al menos un itemfalla
    que no pudo ser instanciado debido a que no tiene al menos una
    captura valida."""
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

  @staticmethod
  def obtenerRecorrido(conn,clave):
    """Retorna una coleccion de itemFalla de la BD, pertenecientes a un recorrido."""
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

  @staticmethod
  def almacenarCapturasEnDisco(name_db,colItemFalla):
    """Almacena la coleccion actual de capturas en disco."""
    #Se forkea el proceso debido a que ZODB no permite el acceso
    # desde el mismo proceso a una falla  
    print "Inicio con name_db: %s\n" % name_db
    conn,stop_function = Capturador.abrirConexion(name_db)
    Capturador.almacenarRecorrido(conn,colItemFalla)
    Capturador.cerrarConexion(conn,stop_function)


  @staticmethod
  def leerCapturasDesdeDisco(name_db):
    """Lee tanto las capturas informadas y confirmadas desde disco."""
    #Se obtiene el recorrido
    print "Obteniendo recorrido...\n"
    conn1,stop_function = Capturador.abrirConexion(name_db)
    dicElems = {}
    dicElems["informados"] = Capturador.obtenerRecorrido(conn1,'recorridoInformados') 
    dicElems["confirmados"] = Capturador.obtenerRecorrido(conn1,'recorridoConfirmados') 
    print "Obtenido el recorrido con las capturas!\n"
    return dicElems,conn1,stop_function
    

class CapturadorInformados(Capturador):
  """ Esta clase es una subclase de Capturador y contiene comportamiento relacionado
    con la captura de fallas informadas."""
  def __init__(self,apiclientComun,bdLocal):
    Capturador.__init__(self,apiclientComun,bdLocal)
    self.colBachesInformados = ListadoFallas()
    self.estrategia = EstrategiaInformados()
  
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

  # capturadorinformados.asociarFalla()
  def asociarFalla(self,data, dir_trabajo, nombre_captura,id_falla,gps):
    """Asocia la falla con la captura recien realizada."""
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
    #return cap.getFullPathCaptura(),cap.getFullPathCapturaConv()
    return cap.getFullPathCaptura()

  # CapturadorInformados.descartarFallaSinCaps()
  def descartarFallaSinCaps(self,colItemsFallaADescartar):
    print "En CapturadorInformados.descartarFallaSinCaps()!\n"
