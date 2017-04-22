# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

import argparse

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys,os

import subprocess

from kivy.animation import Animation

from constantes import *

# Agrega las vistas al path de Python
def agregar_vistas(listaVistas):
    for vista in listaVistas:
        path_local = vista
        sys.path.append(os.path.join( os.getcwd(), path_local))
        # sys.path.append(os.path.join(os.path.dirname('__file__'), path_local  ))

#Configuracion y carpetas de las vistas de la app.
agregar_vistas(LISTADO_MODULOS)

#Se importan los iconfonts para los iconos y spinners
from iconfonts import *


#Configuracion de los paths de las views en archivo .cfg
from utilscfg import *

from kinectviewer import KinectScreen
import importlib
from menu import *
from settingscreen import *
from kinectviewer import *
from subircapturasservidor import *
from apiclient1 import *
from capturador import *
from captura import *

import utils
import time
from utils import *

from kivy.event import EventDispatcher

#Se importan los dialogos de la libreria xpopup 
from notification import XLoading, XConfirmation, XMessage


class MainApp(App,EventDispatcher):
	def __init__(self,**kwargs):
		super(MainApp,self).__init__()
		self.args = self.validarArgs() #Argumentos enviados por linea de comandos.
		
		self.register_event_type('on_fin_obtencion_direcciones')
		self.register_event_type('on_finalizada_captura')
		self.register_event_type('on_fin_solicitud_prop_confirmada')
		super(MainApp, self).__init__(**kwargs)

		# Los capturadores comparten el mismo apiClient, que lleva la cantidad
		# comun de bytes enviados y bytes totales a enviar, de ambos capturadores.
		apiClientComun = ApiClientApp()
		self.capturador = Capturador(apiClientComun)
		self.capturadorInformados = CapturadorInformados(apiClientComun)
		self.bind(on_start = self.instanciada_app)
		self.screen_manager = None
		self.dataViews = {} #Diccionario usado para envio de datos entre views 
							# (usado para las propiedades de las fallas confirmadas)

		self.canceladaSubidaArchivos = False
		#Se validan los argumentos enviados por linea de comandos.
		
		self.id_kinect_viewer = 0
		print "Inicializado MainApp!"


	def agregarData(self,clave,valor):
		self.dataViews[clave] = valor 

	def borrarData(self,clave):
		del self.dataViews[clave]

	def getData(self,clave):
		return self.dataViews[clave]


	#Handler por default requerido por Kivy
	def on_fin_obtencion_direcciones(self,*args):
		pass

	#Handler por default requerido por Kivy
	def on_finalizada_captura(self,*args):
		pass


	def on_fin_solicitud_prop_confirmada(self,*args):
		pass


	# Metodo invocado al instanciar la aplicacion. Se muestran los
	# mensajes de problema de conexion con el sensor, falta de 
	# propiedades para los tipos de falla.
	#
	def instanciada_app(self,app):
		if not conexionSensorEstablecida():
			self.mostrarDialogoMensaje( title='Error de conexion',
										text='El sensor no se encuentra conectado.\nConecte el sensor antes de realizar una nueva captura.'
										)
		popup = self.mostrarDialogoEspera(title="Carga de propiedades",
				content ="Cargando propiedades para fallas confirmadas...",
			)
		
		#self.bind(on_fin_solicitud_prop_confirmada = self.mostrarResultPeticion)
		#Se configura el envio de los archivos como un proceso demonio.
		t = threading.Thread(name = "thread-getPropsConfirmadas",
								target = self.threadGetPropsConfirmadas, 
								args = (popup,) 
							)
		t.setDaemon(True)
		t.start()

	def getCapturador(self):
		return self.capturador

	def obtenerInformados(self,calle):
		return self.capturadorInformados.solicitarInformados(calle)


	#Lee el archivo .json a partir del stream
	def leerFallas(self,stream):
		self.capturador.leerFallas(stream)
		self.capturadorInformados.leerFallas(stream)


	#Guarda el archivo .json a partir del stream
	def guardarFallas(self,stream):
		self.capturador.guardarFallas(stream)
		self.capturadorInformados.guardarFallas(stream)


	#Se llama desde todos los lugares donde es necesario mostrar
	# un dialogo de carga
	def mostrarDialogoEspera(self,title="",content="",gif = PATH_ICONO_RELOJ):
		dialogo = XLoading(title=title,
							content = content,
							auto_open=False,
							gif = gif,
							size_hint_x = 0.5,
							size_hint_y = 0.4)
		dialogo.open()
		return dialogo



	def filtrarCapturas(self):
		popup = self.mostrarDialogoEspera(title ="Subida  de capturas",
										content= "Estimando direcciones de capturas confirmadas...")

		self.bind(on_fin_obtencion_direcciones = popup.dismiss)

		#Se configura el envio de los archivos como un proceso demonio.
		t = threading.Thread(name = "thread-filtrarCapturas",
								target = self.threadFiltradoCapturas, 
								args = () 
							)
		t.setDaemon(True)
		t.start()

	#Filtra aquellos itemFalla que tengan al menos una captura asocida
	#
	def threadFiltradoCapturas(self):
		self.capturador.filtrarCapturas()
		self.capturadorInformados.filtrarCapturas()
		colCapturas = []
		colCapturas = self.capturador.getColCapturasConfirmadas() + \
						self.capturadorInformados.getColCapturasConfirmadas()

		# Se deseleccionan las fallas antes de cargar el screen con las mismas
		print "\nLas fallas filtradas de los capturadores son: \n"
		for falla in colCapturas:
			print "%s\n" % falla
			print "-----------------------------\n"
		print "\n\n"

		#Se produce el evento desde capturador para cerrar el dialogo
		# de carga
		self.dispatch('on_fin_obtencion_direcciones')
		screenCapturas = self.screen_manager.get_screen('subircapturasservidor')
		screenCapturas.actualizarListaCaps(colCapturas)
		print "Finalizado thread-FiltradoCapturas...\n"
		

	#Este elemento establece el campo is_selected como FALSE de las fallas
	# informadas al regresar de esa vista
	def desSeleccionarInformados(self):
		for falla in self.capturadorInformados.getColBachesInformados():
			falla.is_selected = False
			print "Deseleccionando falla informada: %s\n" % falla
		print "Fin desSeleccionarFalla!\n"




	#Envia las capturas filtradas al servidor con POST
	def subir_capturas(self):
		#print "Enviando fallas nuevas ..."
		bytes_totales_a_enviar = 0
		bytes_totales_a_enviar = self.capturador.calcularTamanioCapturas()+\
							self.capturadorInformados.calcularTamanioCapturas()

		#print "Los bytes_totales_a_enviar son : %s" % bytes_totales_a_enviar
		#print ""
		lista_capturadores = [self.capturador,self.capturadorInformados]
		print "\nlista_capturadores desde subir_capturas: %s\n" % len(lista_capturadores)
		#Este candado es adqurido por threadSubidaCapturas al iniciar y cuando 
		# se termine o se cancele la subida de archivos, se libera desde ese thread
		# y es adquirido por mostrarDialogoConservar
		candadoFinSubidas = threading.Lock()
		t = threading.Thread(name = "thread-subir_capturas",
								target=self.threadSubidaCapturas, 
								args=(bytes_totales_a_enviar,
									lista_capturadores,
									candadoFinSubidas,)
							)
		#Se configura el envio de los archivos como un proceso demonio.
		t.setDaemon(True)
		t.start()

			

	# Metodo que paraleliza el envio al servidor de los objetos
	def threadSubidaCapturas(self,bytes_totales_a_enviar,lista_capturadores,candadoFinSubidas):
		print "En threadSubidaCapturas...\n"
		# Se actualiza el valor maximo de la progressbar con los bytes totales
		# de la peticion
		screen_upload = self.screen_manager.get_screen('enviocapturasserver')
		screen_upload.setMaxBarraProgreso(bytes_totales_a_enviar)
		#Se adquiere el control y se inicia el thread del dialgo de pregunta
		# para caps subidas
		candadoFinSubidas.acquire()
		t = threading.Thread(name = "thread-conservarCapsSubidas",
							target=self.threadConservarCapsSubidas, 
							args=(screen_upload,
								candadoFinSubidas,
								lista_capturadores,)
							)
		#Se configura el envio de los archivos como un proceso demonio.
		t.setDaemon(True)
		t.start()

		#Se planifica la actualizacion del reloj a espacios de tiempo regulares
		Clock.schedule_interval(self.actualizar_datos,0.0005)
		try:
			print "Iterando lista de capturadores...\n"
			print "Lista capturadores: %s\n" % lista_capturadores
			for capturador in lista_capturadores:
				print "Iterando capturador %s\n" % type(capturador)
				capturador.enviarCapturas(URL_UPLOAD_SERVER)
				if self.canceladaSubidaArchivos:
					print "Cancelada la subida de archivos desde main.threadSubidaCapturas\n"
					break
		except ExcepcionAjax, e:
			self.mostrarDialogoMensaje( title="Error en la subida de archivos",
										text=e.message
										)
		finally:
			print "Desplanificando el callback de actualizacion del screen!\n"
			Clock.unschedule(self.actualizar_datos)
			print "Liberando el lock!\n"
			candadoFinSubidas.release()

	#Invocado desde threadSubirCapturas
	def threadConservarCapsSubidas(self,screen_upload,candadoFinSubidas,lista_capturadores):
		candadoFinSubidas.acquire()
		print "Liberado el candadoFinSubidas\n"
		self.mostrarDialogoMensaje( title= "Subida de capturas",
									text = "La carga de capturas en el servidor se ha realizado con exito!")

		controlador = App.get_running_app()
		conservarDialogo = controlador.mostrarDialogoConfirmacion(
									title = "Conservar capturas enviadas",
									content = "¿Desea conservar las capturas enviadas al servidor en disco?",
									callback = self._callbackConservarCapsSubidas)
		self.canceladaSubidaArchivos = False


	def _callbackConservarCapsSubidas(self,instance):
		if instance.is_confirmed():
			print "Si conservar las capturas subidas en disco!\n"
			return
		print "Eliminando las capturas subidas de disco...\n"
		listaCapturadores = [self.capturador, self.capturadorInformados]
		for capturador in listaCapturadores:
			capturador.descartarCapsSubidas()
		print "Eliminadas todas las capturas subidas!\n"

	# Actualiza los labels de cantidad de bytes subidos
	# en la pantalla enviocapturasservidor
	def actualizar_datos(self,dt):
		screen_upload = self.screen_manager.get_screen('enviocapturasserver')
		bytes_read = self.capturador.apiClient.bytes_acumulados
		screen_upload.actualizar_datos(bytes_read)

	#Captura de baches nuevos(no informados) e informados
	def capturar(self,data,dir_trabajo,nombre_captura,id_falla):
		print "En main.capturar(): getData()? %s\n " % self.getData("idFalla")
		print "En main.capturar(): id_falla? %s\n " % id_falla
		popup = self.mostrarDialogoEspera(title="Creacion de captura",
										content ="Almacenando falla localmente ...",)
		
		self.bind(on_finalizada_captura = self.finalizadaCaptura)
		
		#Se configura el envio de los archivos como un proceso demonio.
		t = threading.Thread(name = "thread-threadCapturarFalla",
								target = self.threadCapturarFalla, 
								args = (data,dir_trabajo,nombre_captura,
									id_falla,popup,) 
							)
		t.setDaemon(True)
		t.start()

	
	def finalizadaCaptura(self,origenEvt,pcdNombre,csvNombre,popup):
		print "En main.finalizadaCaptura() con: pcd=%s; csv=%s; popup=%s; origenEvt=%s;\n" %\
				(pcdNombre,csvNombre,type(popup),type(origenEvt))

		popup.bind(on_dismiss=self.cerradoPopupCaptura)
		popup.dismiss()
		#Se pregunta al usuario si quiere visualizar la captura		
		controlador = App.get_running_app()
		controlador.mostrar_dialogo_visualizacion(pcdNombre,
												csvNombre)

	def cerradoPopupCaptura(self,evt):
		print "CERRADO EL POPUP CAPTURA!!!\n"


	# main.threadCapturarFalla()
	def threadCapturarFalla(self,data,dir_trabajo,nombre_captura,id_falla,popup):
		print "threadCapturarFalla id_falla:  %s ; FALLA_NO_ESTABLECIDA: %s\n" % (id_falla,FALLA_NO_ESTABLECIDA)
		print "dir_trabajo desde kinectviewer es: %s\n" % dir_trabajo
		print ""
		capturador_a_usar = self.capturador
		if id_falla != FALLA_NO_ESTABLECIDA:
			print "Seleccionando capturadorInformados...\n"
			capturador_a_usar = self.capturadorInformados
		else:
			print "Seleccionando capturarFallaNueva...\n"

		print "tipo capturador: %s" % type(capturador_a_usar) 
		pathPcd, pathCsv = capturador_a_usar.asociarFalla(data, dir_trabajo, nombre_captura,id_falla,
															self.args.gps)
		#Se dispara el evento 'on_finalizada_captura' con los nombres de archivos
		# pcd y csv 
		self.dispatch('on_finalizada_captura',pathPcd,pathCsv,popup)
		


	def getCapturadorInformados(self):
		return self.capturadorInformados


	def inicializar(self,sm):
		conf = leer_configuracion(PATH_ARCHIVO_CONFIGURACION)
		self.cargar_vistas(sm,conf)
    
	def cargar_vistas(self,sm,listaVistas):
		for kev,tupla in listaVistas.iteritems():
			Builder.load_file(tupla["ruta_kv"])
			MyClass = getattr(importlib.import_module(tupla["modulo"]), 
			tupla["clase"])
			instance = MyClass()
			screen = MyClass(name=tupla["nombre_menu"])
			sm.add_widget(screen)

	def mostrar_dialogo_visualizacion(self,pathCapturaPcd,pathCapturaCsv):
		#NOTA: Se retrasa levemente el dibujado del dialogo_visualizacion para
		# darle tiempo al popup a que se cierre y no hayan problemas de 
		# redibujado con el dialogo.
		time.sleep(1)
		print "MOSTRADO DIALOGO DE VISUALIZACION!! \n"
		# NOTA: El nombre de la captura .pcd y .csv  son enviados desde el metodo capturador.capturar()
		# en appCliente
		args = [ {"pcdFile":pathCapturaPcd},
				{"csvFile":pathCapturaCsv} ]

		popupVisualizar = self.mostrarDialogoConfirmacion(title="Visualizacion de captura",
															content = "¿Desea visualizar la captura?",
															callback = self.desvanecidoVisualizar,
															args = args )

	#Handler para cuando se desvanece el dialogo de visualizar
	def desvanecidoVisualizar(self,popup):
		if popup.is_confirmed():
			print "Si desea visualizar!!\n"
			self.mostrarCaptura(popup.args)
		else:
			print "NO desea visualizar\n"
			self.noMostrarCaptura(popup.args)
		self.mostrarDialogoConfirmacion( title= "Conservacion de la captura",
										 content = "¿Desea conservar la captura?",
										 args = popup.args,
										 callback = self.desvanecidoConservar)

	#Handler para cuando se desvanece el dialogo de conservar
	def desvanecidoConservar(self,popup):
		if popup.is_confirmed():
			print "Si desea conservar la captura\n"
			self.conservar(popup)
		else:
			print "NO desea conservar la captura\n"
			self.descartar(popup)
			

	#AGREGADO RODRIGO
	def descartar(self,popup):
		print "En descartar()..."
		dicCaps = popup.args
		capturas = list() 
		capturas.append(dicCaps[0]['pcdFile'])
		capturas.append(dicCaps[1]['csvFile'])
		print "Las capturas recibidas son :%s\n" % capturas
		estaDescartada = self.capturador.descartar(capturas)
		if not estaDescartada:
			self.capturadorInformados.descartar(capturas)
			print "Captura descartada en self.capturador: %s ; self.capturadorInformados: %s\n" % (estaDescartada,estaDescartada)


	#AGREGADO RODRIGO
	def conservar(self,popup):
		print "Se conserva la captura %s en disco!" % popup.args
	

	#AGREGADO RODRIGO
	def mostrarCaptura(self,caps):
		print "Visualizando captura %s...\n" % caps
		try:
			print "PATH_VIEW_PCD_FILE_SCRIPT: %s\n" % PATH_VIEW_PCD_FILE_SCRIPT
			print "caps[0]: %s\n" % caps[0]
			#subprocess.check_call([PATH_VIEW_PCD_FILE_SCRIPT,
			#		caps[0]])
			subprocess.check_call([PATH_VIEW_PCD_FILE_SCRIPT,
					caps[0]["pcdFile"] ])
			print "Abierto visualizador\n"
		except Exception as e:
			err = "Error OS con pcl_viewer(%s)\n" % e
			print err
			self.mostrarDialogoMensaje( title="Error al visualizar captura",
										text=err						
										)
			
	#AGREGADO RODRIGO
	def noMostrarCaptura(self,caps):
		print "No se visualizara la captura %s...\n" % caps

	#Construir aca las instancias del modelo que son usadas por la App.
	# NOTA: Emplear el metodo App.get_running_app() para obtener la instancia
	# actual de MainAPP.
	def build(self):
		#Se registran los fonts
		register('default_font',NOMBRE_FONT_TTF, NOMBRE_FONT_DICT)
		print "En build()"
		sm = ScreenManager()
		self.title = TITULO_APP
		self.inicializar(sm)
		sm.current = SCREEN_PRINCIPAL
		self.screen_manager = sm
		return sm


	# Obtiene las propiedades que se emplean para dar de alta
	# los tipos de fallas confirmadas.
	# -Si se pueden obtener desde el servidor, se cargan en memoria,
	# y se actualiza la BD JSON de propiedades local.
	# -Si no se pueden obtener desde el servidor, se cargan las que
	# estan de manera local. Si la BD local no tiene propiedades,
	# al efectuar la operacion "Capturar falla nueva", se muestra 
	# un msg indicando que se conecte a internet para obtener las
	# propiedades de los tipos de falla confirmadas y se retorna
	# al screen principal.
	def threadGetPropsConfirmadas(self,popup):
		resultPeticion = {
						"titulo":"Peticion al servidor"
						}
		msg = ""
		msg2 = ""
		try:
			# Se cargan las propiedades desde el servidor y si se tiene exito
			# se crea un resplado local
			self.capturador.obtenerPropsConfirmadas()
			print "Despues de capturador.obtenerPropsConfirmadas()\n"
			self.capturador.crearBackupConfirmados()
			msg = "Tipos de falla obtenidos correctamente\n desde servidor!"
		except (ExcepcionTipoFallaIncompleta,ExcepcionAjax) as e:
			msgAux = "Excepcion:\n %s" % e
			msg2 = "\n(" + msgAux + ")" 
			print msg2
			print "\n%s\n" % msg
			# Si no se puede conectar con el servidor se intenta
			# cargar un respaldo de los atributos de los tipos de falla
			try:
				self.capturador.cargarAtributosDesdeBDLocal()
				print "Despues de capturador.cargarAtributosDesdeBDLocal()\n"
				msg = "Tipos de falla cargados desde BD Local."
			except ExcepcionSinDatosTiposFalla as e:
				msg = "ERROR al obtener tipos de falla.\n Sin datos disponibles: %s\n" % e
			except ExcepcionTipoFallaIncompleta as e:
				msg = "ExcepcionTipoFallaIncompleta en carga atributos locales:\n %s" % e

		except Exception as e: 
			msg = "Excepcion desconocida en threadGetPropsConfirmadas\n: %s\n" % e 
		finally:
			resultPeticion["msg"] = msg + msg2 
			print msg + msg2
			popup.bind(on_dismiss = self.desvanecidoPopupConfirmadas)
			popup.dismiss()
			self.mostrarResultPeticion(resultPeticion,popup)

	#Muestra un dialogo que indica si las propiedades se pudieron 
	#cargar desde la BD, o si se usara la DB local.
	def mostrarResultPeticion(self,dicInfo,popup):
		time.sleep(1)
		print "MOSTRANDO EL RESULTADO DE LA PETICION...\n"
		popup.dismiss()
		self.mostrarDialogoMensaje(
								text= dicInfo["msg"],
								title = dicInfo["titulo"])

	def _defaultDialogoMensajeHandler(self,instance):
		pass

	#Muestra un dialogo de mensaje con un boton de aceptar
	def mostrarDialogoMensaje(self,text = "", title=""):
		return XMessage(text= text, title=title)

	#Muestra un dialogo de confirmacion con los botones "Si","No".
	def mostrarDialogoConfirmacion(self,content = "",title="",callback=None,
									args = []):
		if callback is None:
			callback = self.confirmDefaultHandler
		XConfirmation(title = title,text = content,on_dismiss = callback,
						args = args)


	def confirmDefaultHandler(self,popup):
		pass

	def desvanecidoPopupConfirmadas(self,evt):
		print "SE DESVANECIO EL POPUPCONFIRMADAS!\n"


	def estanCargadasPropTipoFalla(self):
		return self.capturador.existenPropsCargadas()

	def getPropsConfirmados(self):
		return self.capturador.getPropsConfirmados()


	def getAtributosAsociados(self,nombreTipoFalla):
		return self.capturador.getAtributosAsociados(nombreTipoFalla)

	#Invoca a capturador para determinar si son atributos validos para
	# el tipo de falla seleccionado(valida si no dejo sin seleccionar 
	# el tipoReparacion y tipoMaterial)
	def sonPropiedadesValidas(self,tipoFalla,tipoReparacion,tipoMaterial):
		return self.capturador.sonPropiedadesValidas(tipoFalla,tipoReparacion,tipoMaterial)

	#Llamado desde menu.py (menu principal de la app)
	#main.cargarRecorrido().
	def cargarRecorrido(self,archivo):
		dicElems = Capturador.cargarRecorrido(archivo)
		self.capturador.setColCapturasTotales(dicElems["confirmados"])
		self.capturadorInformados.setColCapturasTotales(dicElems["informados"])
		if len(dicElems["confirmados"]) == 0 and len(dicElems["informados"]) == 0:
			raise ExcepcionRecorridoVacio
		print "\nMostrando la coleccion de fallas cargadas: \n"
		self.mostrarColItemFalla()


	#Obtiene las fallas confirmadas e informados de los capturadores.
	def persistirFallas(self,nameBD):
		fallas = self.capturador.obtenerCapturasNoSubidas() +\
			self.capturadorInformados.obtenerCapturasNoSubidas()
		Capturador.persistirFallas(nameBD,fallas)
		print "Mostrando la coleccion de fallas persistidas...\n"
		self.mostrarColItemFalla()
		# Se vacian las colecciones de los capturadores al
		# guardar el recorrido.
		self.capturador.setColCapturasTotales([])
		self.capturadorInformados.setColCapturasTotales([])

	#Metodo de prueba
	def mostrarColItemFalla(self,col=None):
		print "\n++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		print "Mostrando itemfallas con estado Confirmado: \n"
		for falla in self.capturador.getColCapturasTotales():
			print "%s\n" % falla
		print "\n\n-------------------------------------------\n"
		print "Mostrando itemfallas con estado Informado: \n"
		for falla in self.capturadorInformados.getColCapturasTotales():
			print "%s\n" % falla
		print "\n++++++++++++++++++++++++++++++++++++++++++++++++++\n"
		
	def existenFallasCargadas(self):
		result = True
		if len(self.capturador.getColCapturasTotales()) == 0 and\
				len(self.capturadorInformados.getColCapturasTotales()) == 0:
			result = False
		return result

	#Valida los argumentos enviados por linea de comandos.
	def validarArgs(self):
		parser = argparse.ArgumentParser(prog ="main.py", description="Modulo principal de la aplicacion cliente para captura de fallas.")
		parser.add_argument('--gps', metavar='TIPO-GPS',help='Tipo de gps a emplear en la aplicacion. Opciones: fakegps | realgps.Default: fakegps.')
		parser.add_argument('--tipoCaptura', metavar='TIPOS-CAPTURA',help='Tipo de archivos de captura.Opciones: xyz_rgb | xyz. Default: xyz_rgb.')
		args = parser.parse_args()
		if (args.gps is not None) and (args.gps not in OPCIONES_GPS):
			try:
				parser.print_help()
				sys.exit(1)
			except Exception as e:
				pass
		if (args.tipoCaptura is not None) and (args.tipoCaptura not in OPCIONES_CAPTURA):
			try:
				parser.print_help()
				sys.exit(1)
			except Exception as e:
				pass
		if args.gps is None:
			args.gps = TIPO_GPS_DEFAULT 
		if args.tipoCaptura is None:
			args.tipoCaptura = TIPO_CAPTURA_DEFAULT
		print "Los argumentos enviados por consola son: %s\n" % args
		return args



#Ejemplo de la ejecucion del programa para enviar los comandos parseados por argparse:
#$ python main.py -- --gps realgps 2>&1 | tee log.txt
if __name__ == '__main__':
    MainApp().run()
