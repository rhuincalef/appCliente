# -*- coding: utf-8 -*-

import kivy
kivy.require('1.0.5')

import argparse

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys,os

reload(sys)
sys.setdefaultencoding("utf-8")

import subprocess

from kivy.animation import Animation

from constantes import *

from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelHeader,TabbedPanelStrip,TabbedPanelItem

#Se cargan las utilidades para cargar las configuraciones
import utils
from utils import *

#Se importan los iconfonts para los iconos y spinners
from iconfonts import *

#Configuracion de los paths de las views en archivo .cfg
from utilscfg import *
import importlib
from apiclient1 import *
from capturador import *
from captura import *
from customwidgets import *

import time
from kivy.event import EventDispatcher

#Se importan los dialogos de la libreria xpopup 
from notification import XLoading, XConfirmation, XMessage

#Librerias para monitoreo usb asincrono -->
from pyudev import Context, Monitor, MonitorObserver

from kivy.base import EventLoop
EventLoop.ensure_window()

#Import agregado para eliminar el warning
#import gi
#gi.require_version('Gtk','3.0')

from kivy.clock import Clock

from kivy.core.window import Window
import threading



class MainApp(App,EventDispatcher):
	def __init__(self,**kwargs):
		super(MainApp,self).__init__()
		#cargarConfiguraciones()
		self.args = self.validarArgs() #Argumentos enviados por linea de comandos.
		
		self.register_event_type('on_fin_obtencion_direcciones')
		self.register_event_type('on_finalizada_captura')
		self.register_event_type('on_fin_solicitud_prop_confirmada')

		#Evento producido en el AutoComplete.
		self.register_event_type('on_fin_obtencion_sugerencias')
		super(MainApp, self).__init__(**kwargs)

		# Los capturadores comparten el mismo apiClient, que lleva la cantidad
		# comun de bytes enviados y bytes totales a enviar, de ambos capturadores.
		apiClientComun = ApiClientApp()
		bdLocalMuestrasComun = BDLocal(fullPathBD = None)
		self.capturador = Capturador(apiClientComun,bdLocalMuestrasComun)
		self.capturadorInformados = CapturadorInformados(apiClientComun,bdLocalMuestrasComun)

		# Se comienzan a mostrar los dialogos al inicio de la aplicacion una vez 
		# que esta se instancio completamente.
		self.bind(on_start = self.instanciada_app)

		self.screen_manager = None
		self.dataViews = {} #Diccionario usado para envio de datos entre views 
							# (usado para las propiedades de las fallas confirmadas)

		self.canceladaSubidaArchivos = False
		#Se validan los argumentos enviados por linea de comandos.
		
		self.id_kinect_viewer = 0

		#Campo para determinar si existe una conexion con el sensor kinect
		#Este campo es modificado cada vez que se conecta o desconecta el kinect.
		#La monitorizacion y ejecucion del callback se realiza por medio del thread
		# daemon que se lanza en inicializarMonitorKinect()
		self.sensorConectado = estaSensorListo()
		print "Valor de self.sensorConectado: %s\n" % self.sensorConectado
		self.inicializarMonitorKinect()

		self.tabbedPanel = None

		tb_panel= MyTabbedPanel(do_default_tab= False,
									size_hint= (1,1),
									pos_hint= {'center_x': .5, 'center_y': .5},
									tab_pos = 'top_right',
									tab_height= 40,
									tab_width = 170)
		self.tabbedPanel = tb_panel

		self.configurarLoggingPrincipal()
		print "Inicializado MainApp!"

	# Realiza las redicciones de stderr y stdout al mismo tiempo, envia los
	# registros a la linea de comandos.
	def configurarLoggingPrincipal(self):
		from constantes import PATH_LOG_PRINCIPAL
		sys.stdout = sys.stderr = open(PATH_LOG_PRINCIPAL,"w")
		tee = subprocess.Popen(["tee", PATH_LOG_PRINCIPAL], stdin=subprocess.PIPE)
		os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
		os.dup2(tee.stdin.fileno(), sys.stderr.fileno())
		print "configurado el logging principal"

	def getBDLocalMuestras(self):
		return self.capturador.getBDLocalMuestras()

	#Inicializa la BD de Muestras local para el objeto "Capturador" (baches confirmados).
	# NOTA: LA BD de "CapturadorInformados" no se inicializa porque es la misma referencia. 
	def inicializarBDLocal(self,fullPathBD = None):
		self.capturador.inicializarBDLocal(fullPathBD = fullPathBD)


	#Handler por default del metodo de autocompletar
	def on_fin_obtencion_direcciones(self,*args):
		pass


	#Handler por default del metodo de autocompletar
	def on_fin_obtencion_sugerencias(self,*args):
		pass

	#Metoodo que realiza la peticion a ApiClient1 para el autocompletado de direcciones
	def solicitarSugerencias(self,nombreCalle,cantMaximaSugerencias):
		sugerencias = []
		try:
			sugerencias = self.capturador.apiClient.solicitarSugerencias(nombreCalle,cantMaximaSugerencias)
		except Exception as e:
			print "\n\n Excepcion ocurrida al solicitar las sugerencias desde el servidor (%s)\n\n " %\
				e
		finally:
			print "produciendo evento on_fin_obtencion_sugerencias con sugerencias: %s\n" % sugerencias
			#self.dispatch('on_fin_obtencion_direcciones',sugerencias)
			self.dispatch('on_fin_obtencion_sugerencias',sugerencias)

	#controlador.conexionSensorEstablecida()
	def conexionSensorEstablecida(self):
		return self.sensorConectado

	#Inicializa el thread que monitoriza y llama a handlerSensorConectado()
	# cuando ocurre un campo de estado en los puertos usb
	def inicializarMonitorKinect(self):
		context = Context()
		monitor = Monitor.from_netlink(context)
		monitor.filter_by(subsystem = 'usb')
		observer = MonitorObserver(monitor,
								event_handler=self.handlerSensorConectado,
								name='thread-observerMonitor')
		observer.start()
		print "INiciado thread de monitorizacion del sensor kinect...\n"

	# Metodo que actualizara el estado del sensor segun la actividad en el
	# puerto USB.
	def handlerSensorConectado(self,action,device):
		print "En handlerSensorConectado()...\n"
		estaListo = estaSensorListo()
		self.sensorConectado = estaListo
		if estaListo:
			print "Modificado controlador.sensorListo() a True!\n"
		else:
			print "Modificado controlador.sensorListo() a False!\n"

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
	def instanciada_app(self,app):
		print "instanciada la app!\n"
		if not self.conexionSensorEstablecida():
			self.mostrarDialogoMensaje( title='Error de conexión',
										text='El sensor no se encuentra conectado.\nConecte el sensor antes de realizar una nueva captura.'
										)
		popup = self.mostrarDialogoEspera(title="Carga de propiedades",
				content ="Cargando propiedades para fallas confirmadas...",
			)
		self.bind(on_fin_solicitud_prop_confirmada = self.mostrarResultPeticion)
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
							size_hint_y = 0.4,
							background = ESTILO_BACKGROUND_MODAL_XBASE,
							separator_color = COLOR_SEPARADOR_POPUPS
							)
		print "instanciado dialogo espera...\n"
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
	def threadFiltradoCapturas(self):
		print "Iniciando thread-filtrado de capturas"
		logger = utils.instanciarLogger(LOG_FILE_FILTRADO_CAPS)
		try:
			self.capturador.filtrarCapturas()
			self.capturadorInformados.filtrarCapturas()
			colCapturas = []
			colCapturas = self.capturador.getColCapturasConfirmadas() + \
				self.capturadorInformados.getColCapturasConfirmadas()
			screenCapturas = self.tabbedPanel.getSubMenuPorNombre('subircapturasservidor')
			screenCapturas.actualizarListaCaps(colCapturas)
			print "Finalizado thread-FiltradoCapturas...\n"

		except ConnectionError as e:
			print "ConnectionError en controlador.threadFiltradoCapturas()...\n"
			errMsg = "ConnectionError (%s)" % e.message
			utils.loggearMensaje(logger,errMsg)
			msg = "No se pueden subir archivos hasta que se haya\n establecido conexión con el servidor.\n Más información en %s%s" %\
				(LOGS_DEFAULT_DIR,LOG_FILE_FILTRADO_CAPS)
			popup = self.mostrarDialogoMensaje(title = "Error de conexión con el servidor",
												text = msg)
			popup.bind(on_dismiss=self._regresarAMainMenu)
		finally:
			#Se produce el evento desde capturador para cerrar el dialogo
			# de carga
			self.dispatch('on_fin_obtencion_direcciones')

	# Regresa al menu principal
	def _regresarAMainMenu(self,instance):
		print "En _regresarAMainMenu()...\n"

	def desSeleccionarInformados(self):
		print "En main.desSeleccionarInformados()...\n"
		for falla in self.capturadorInformados.getColBachesInformados():
			#falla.is_selected = False
			falla.desSeleccionar()
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
		#Reseteando estado de la subida de archivos.
		print "Reseteando flag de subida archivos...\n"
		self.canceladaSubidaArchivos = False
		
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
		#screen_upload = self.screen_manager.get_screen('enviocapturasserver')
		screenManager = self.tabbedPanel.getSubMenuPorNombre('subMenuServidor').manager
		screen_upload = screenManager.get_screen('enviocapturasserver')
		screen_upload.setMaxBarraProgreso(bytes_totales_a_enviar)
		
		hayErrorConServidor = False

		#Se adquiere el control y se inicia el thread del dialgo de pregunta
		# para caps subidas
		candadoFinSubidas.acquire()
		#t = threading.Thread(name = "thread-conservarCapsSubidas",
		#					target=self.threadConservarCapsSubidas, 
		#					args=(screen_upload,
		#						candadoFinSubidas,
		#						lista_capturadores,)
		#					)
		#Se configura el envio de los archivos como un proceso demonio.
		#t.setDaemon(True)
		#t.start()

		#Se planifica la actualizacion del reloj a espacios de tiempo regulares
		Clock.schedule_interval(self.actualizar_datos,0.0005)
		try:
			print "Iterando lista de capturadores para subir...\n"
			controlador = App.get_running_app()
			print "tipo: %s; controlador.canceladaSubidaArchivos: %s\n" % (type(controlador),
																			controlador.canceladaSubidaArchivos)
			print "tipo: %s; self.canceladaSubidaArchivos: %s\n" % (type(self),
																		self.canceladaSubidaArchivos)

			print "Lista capturadores: %s\n" % lista_capturadores
			for capturador in lista_capturadores:
				print "Iterando capturador %s\n" % type(capturador)
				capturador.enviarCapturas(URL_UPLOAD_SERVER)
				if self.canceladaSubidaArchivos:
					print "Cancelada la subida de archivos desde main.threadSubidaCapturas\n"
					break

		except ExcepcionAjax, e:
			self.mostrarDialogoMensaje( title="Problema en la subida de archivos",
										text=e.message
										)
			hayErrorConServidor = True

		except ExcepcionDesconexion as e:
			print "Entre por ExcepcionDesconexion...\n"
			self.mostrarDialogoMensaje( title="Problema de conexion con servidor",
										text=e.message
										)
			hayErrorConServidor = True
			print "hayErrorConServidor: %s\n" % hayErrorConServidor

		finally:
			if not hayErrorConServidor:
				print "No hay error en la subida de archivos al servidor!\n"
				t = threading.Thread(name = "thread-conservarCapsSubidas",
								target=self.threadConservarCapsSubidas, 
								args=(screen_upload,
									candadoFinSubidas,
									lista_capturadores,)
								)
				#Se configura el envio de los archivos como un proceso demonio.
				t.setDaemon(True)
				t.start()
			else:
				print "Ocurrio error con el servidor...\n"

			print "Desplanificando el callback de actualizacion del screen!\n"
			Clock.unschedule(self.actualizar_datos)
			print "Liberando el lock!\n"
			candadoFinSubidas.release()


	#Invocado desde threadSubirCapturas
	def threadConservarCapsSubidas(self,screen_upload,candadoFinSubidas,lista_capturadores):
		candadoFinSubidas.acquire()
		print "Liberado el candadoFinSubidas\n"
		self.mostrarDialogoMensaje( title= "Subida de capturas",
									text = "La operacion de subida de archivos ha finalizado")

		controlador = App.get_running_app()
		conservarDialogo = controlador.mostrarDialogoConfirmacion(
									title = "Conservar capturas enviadas",
									content = "¿Desea conservar las capturas enviadas al servidor en disco?",
									callback = self._callbackConservarCapsSubidas)
		
	def _callbackConservarCapsSubidas(self,instance):
		if instance.is_confirmed():
			print "Si conservar las capturas subidas en disco!\n"
			return
		print "Eliminando las capturas subidas de disco...\n"
		listaCapturadores = [self.capturador, self.capturadorInformados]
		for capturador in listaCapturadores:
			capturador.descartarCapsSubidas()
		print "Eliminadas todas las capturas subidas!\n"
		print "main.canceladaSubidaArchivos: %s\n" % self.canceladaSubidaArchivos


	# Actualiza los labels de cantidad de bytes subidos
	# en la pantalla enviocapturasservidor
	def actualizar_datos(self,dt):
		screenManager = self.tabbedPanel.getSubMenuPorNombre('subMenuServidor').manager
		screen_upload = screenManager.get_screen('enviocapturasserver')
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

	#def finalizadaCaptura(self,origenEvt,pcdNombre,csvNombre,popup):
	def finalizadaCaptura(self,origenEvt,pcdNombre,popup):
		print "En main.finalizadaCaptura() con: pcd=%s; popup=%s; origenEvt=%s;\n" %\
				(pcdNombre,type(popup),type(origenEvt))

		popup.bind(on_dismiss = self.cerradoPopupCaptura)
		popup.dismiss()
		#Se pregunta al usuario si quiere visualizar la captura		
		controlador = App.get_running_app()
		controlador.mostrar_dialogo_visualizacion(pcdNombre)

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
		pathPcd = capturador_a_usar.asociarFalla(data, dir_trabajo, nombre_captura,id_falla,
															self.args.gps)
		#Se dispara el evento 'on_finalizada_captura' con los nombres de archivos
		# pcd y csv 
		#self.dispatch('on_finalizada_captura',pathPcd,pathCsv,popup)
		self.dispatch('on_finalizada_captura',pathPcd,popup)
		
	def getCapturadorInformados(self):
		return self.capturadorInformados

	#def mostrar_dialogo_visualizacion(self,pathCapturaPcd,pathCapturaCsv):
	def mostrar_dialogo_visualizacion(self, pathCapturaPcd):
		#NOTA: Se retrasa levemente el dibujado del dialogo_visualizacion para
		# darle tiempo al popup a que se cierre y no hayan problemas de 
		# redibujado con el dialogo.
		time.sleep(1)
		print "MOSTRADO DIALOGO DE VISUALIZACION!! \n"
		# NOTA: El nombre de la captura .pcd y .csv  son enviados desde el metodo capturador.capturar()
		# en appCliente
		#args = [ {"pcdFile":pathCapturaPcd},
		#		{"csvFile":pathCapturaCsv} ]
		args = [ { "pcdFile": pathCapturaPcd} ]
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



	#main.descartar()
	def descartar(self,popup):
		print "En descartar()..."
		dicCaps = popup.args
		capturas = list() 
		capturas.append(dicCaps[0]['pcdFile'])
		print "Las capturas recibidas son :%s\n" % capturas
		estaDescartada = self.capturador.descartar(capturas)
		if not estaDescartada:
			self.capturadorInformados.descartar(capturas)
			print "Captura descartada en self.capturador: %s ; self.capturadorInformados: %s\n" % (estaDescartada,estaDescartada)



	def conservar(self,popup):
		print "Se conserva la captura %s en disco!" % popup.args
	
	def mostrarCaptura(self,caps):
		print "Visualizando captura %s...\n" % caps
		try:
			print "PATH_VIEW_PCD_FILE_SCRIPT: %s\n" % PATH_VIEW_PCD_FILE_SCRIPT
			print "caps[0]: %s\n" % caps[0]
			#subprocess.check_call([PATH_VIEW_PCD_FILE_SCRIPT,
			#		caps[0]["pcdFile"] ])
			subprocess.check_call("pcl_viewer "+ "\"" + caps[0]["pcdFile"] + "\"", shell=True)
			print "Abierto visualizador\n"
		except Exception as e:
			err = "Error OS con pcl_viewer(%s)\n" % e
			print err
			self.mostrarDialogoMensaje( title="Error al visualizar captura",
										text=err						
										)

	def noMostrarCaptura(self,caps):
		print "No se visualizara la captura %s...\n" % caps

	#Construir aca las instancias del modelo que son usadas por la App.
	# NOTA: Emplear el metodo App.get_running_app() para obtener la instancia
	# actual de MainAPP.
	def build(self):
		#Se registran los fonts
		register('default_font',NOMBRE_FONT_TTF, NOMBRE_FONT_DICT)
		print "En build()\n"
		self.title = TITULO_APP
		Builder.load_string(ESTILO_TREE_VIEW)

		#self.lockPropsConfirmadas = threading.Condition()
		#popup = self.mostrarDialogoEspera(title="Carga de propiedades",
		#		content ="Cargando propiedades para fallas confirmadas..." )

		#t = threading.Thread(name = "thread-getPropsConfirmadas",
		#						target = self.threadGetPropsConfirmadas, 
		#						args = (popup,self.lockPropsConfirmadas,) 
		#						#args = (self.lockPropsConfirmadas,) 
		#					)
		#t.setDaemon(True)
		#t.start()
		#print "Adquiriendo el lock desde main... \n"
		#self.lockPropsConfirmadas.acquire()
		#self.lockPropsConfirmadas.wait(5)
		
		#print "DESPERTO MAIN!\n"
		#tb_panel= MyTabbedPanel(do_default_tab= False,
		#							size_hint= (1,1),
		#							pos_hint= {'center_x': .5, 'center_y': .5},
		#							tab_pos = 'top_right',
		#							tab_height= 40,
		#							tab_width = 170)
		#self.tabbedPanel = tb_panel
		#self.tabbedPanel.inHabilitarSubMenus([PREFIJO_ID_TP_ITEM + "subMenuSeleccionarBD"])
		Window.bind(on_resize=self.ventanaCambioTamanio)
		print "bindeados eventos\n"
		return self.tabbedPanel

	#Handler de ventana
	def ventanaCambioTamanio(self,window,width,height):
		print "Ventana cambio tamanio %s, %s, %s!\n" % (type(window),
														type(width),
														type(height))
		print "nuevo tamanio %s, %s, %s!\n" % (window,
														width,
														height)
		# Se modifica el padding y spacing de todas los screens de la app que tienen footer
		for screen in self.tabbedPanel.getScreensRedimensionables():
			print "iterando screen %s\n" % type(screen)
			print " screen.ids: %s\n" % screen.ids
			screen.redimensionarFooter(width)


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
	#def threadGetPropsConfirmadas(self,popup,lockPropsConfirmadas):
	def threadGetPropsConfirmadas(self,popup):
		resultPeticion = {
						"titulo":"Petición al servidor"
						}
		msg = ""
		msg2 = ""
		print "Iniciando threadGetPropsConfirmadas()...\n"
		logger = utils.instanciarLogger(LOG_FILE_CAPTURAS_PROPS_CONFIRMADA)
		try:

			# Se cargan las propiedades desde el servidor y si se tiene exito
			# se crea un resplado local
			self.capturador.obtenerPropsConfirmadas()
			print "Despues de capturador.obtenerPropsConfirmadas()\n"
			self.capturador.crearBackupConfirmados()
			msg = "Tipos de falla obtenidos correctamente desde servidor!"

			self.dataViews["esErrorFatal"] = False
		
		except (ExcepcionTipoFallaIncompleta,ExcepcionAjax) as e:
			print "Hu\n"
			utils.loggearMensaje(logger,str(e.message))
			# Si no se puede conectar con el servidor se intenta
			# cargar un respaldo de los atributos de los tipos de falla
			try:
				self.capturador.cargarAtributosDesdeBDLocal()
				print "Despues de capturador.cargarAtributosDesdeBDLocal()\n"
				msg = "Tipos de falla cargados desde BD Local.\n Más información en %s%s" %\
					(LOGS_DEFAULT_DIR,LOG_FILE_CAPTURAS_PROPS_CONFIRMADA)

			except ExcepcionSinDatosTiposFalla as e:
				msg = "ERROR al obtener tipos de falla.\nSin datos disponibles.\n Más información en %s%s" %\
					(LOGS_DEFAULT_DIR,LOG_FILE_CAPTURAS_PROPS_CONFIRMADA)
				errMsg = "ExcepcionSinDatosTiposFalla ocurrio:\n %s" % e.message
				utils.loggearMensaje(logger,errMsg)
				self.dataViews["esErrorFatal"] = True

			except ExcepcionTipoFallaIncompleta as e:
				msg = " Error en la carga atributos locales.\n Más información en %s%s" %\
					(LOGS_DEFAULT_DIR,LOG_FILE_CAPTURAS_PROPS_CONFIRMADA)
				errMsg = "ExcepcionTipoFallaIncompleta ocurrio:\n %s" % e.message
				utils.loggearMensaje(logger,errMsg)		

		except Exception as e: 
			msg = "Excepcion desconocida en threadGetPropsConfirmadas.\n Mas información en %s%s\n" %\
				(LOGS_DEFAULT_DIR,LOG_FILE_CAPTURAS_PROPS_CONFIRMADA)
			errMsg = "Excepcion desconocida (%s) ocurrio en threadGetPropsConfirmadas:\n  ------------------>> message:  %s" % (type(e),e.message)
			utils.loggearMensaje(logger,errMsg)

		finally:
			resultPeticion["msg"] = msg 
			print msg
			popup.bind(on_dismiss = self.desvanecidoPopupConfirmadas)
			popup.dismiss()

			print "inicializando el screen de propsTipoFallaConfirmada!\n"
			self.tabbedPanel.getSubMenuPorNombre("propsFallaConfirmada").inicializarDropDownPrincipal()
			
			print "incializada el screen de propsTipoFallaConfirmada!\n"
			self.mostrarResultPeticion(resultPeticion,popup)
			#print "notificando a main...\n"
			#	lockPropsConfirmadas.notify_all()


	#Muestra un dialogo que indica si las propiedades se pudieron 
	#cargar desde la BD, o si se usara la DB local.
	def mostrarResultPeticion(self,dicInfo,popup):
		time.sleep(1)
		print "MOSTRANDO EL RESULTADO DE LA PETICION...\n"
		popup.dismiss()
		dialogoPeticionProps = self.mostrarDialogoMensaje(
								text= dicInfo["msg"],
								title = dicInfo["titulo"])

		dialogoPeticionProps.bind(on_dismiss = self.comprobarConexionSensor)

	# Muestra un dialogo de espera donde se comprueba la conexion con el sensor. 
	#def comprobarConexionSensor(self):
	def comprobarConexionSensor(self,instance):
		print "En comprobarConexionSensor().\n"
		popup = self.mostrarDialogoEspera(title="Conexión con el sensor",
				content ="Comprobando la correcta conexión al sensor Kinect...",
			)
		t = threading.Thread(name = "thread-threadComprobarConexionSensor",
								target = self.threadComprobarConexionSensor, 
								args = (popup,)
							)
		t.setDaemon(True)
		t.start()

	def threadComprobarConexionSensor(self,popup):
		time.sleep(1)
		print "En threadComprobarConexionSensor() \n"
		if not self.tabbedPanel.getSubMenuPorNombre("capturaKinect").recibiendoDatosKinect():
			print "No recibiendo data...\n"
			self.mostrarDialogoConfirmacion(
									title = "Conexión al sensor kinect",
									content = "No se estan recibiendo datos del sensor, si desea capturar debe reconectarlo.\n¿Desea continuar ejecutando la aplicación?",
									callback = self._callbackContinuarSensor)
		popup.dismiss()
		print "Luego de threadCOnexionSensor: %s\n" % self.dataViews["esErrorFatal"]
		if self.dataViews["esErrorFatal"]:
			print "Error fatal: Sin atributos para tipos de fallas confirmadas...\n"
			self.stop()

	def _callbackContinuarSensor(self,instance):
		print "En _callbackContinuarSensor() \n"
		if instance.is_confirmed():
			print "Si continuar ejecutando app!\n"
			return
		print "Matando la aplicacion...\n"
		App.stop(App.get_running_app())

	def _defaultDialogoMensajeHandler(self,instance):
		pass

	#Muestra un dialogo de mensaje con un boton de aceptar
	def mostrarDialogoMensaje(self,text = "", title=""):
		return XMessage(text= text, title=title 
							,background = ESTILO_BACKGROUND_MODAL_XBASE,
							separator_color = COLOR_SEPARADOR_POPUPS )

	#Muestra un dialogo de confirmacion con los botones "Si","No".
	def mostrarDialogoConfirmacion(self,content = "",title="",callback=None,
									args = []):
		if callback is None:
			callback = self.confirmDefaultHandler
		XConfirmation(title = title,text = content,on_dismiss = callback,
						args = args,
						background = ESTILO_BACKGROUND_MODAL_XBASE,
						separator_color = COLOR_SEPARADOR_POPUPS)


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


	#Llamado desde menu.py (menu principal de la app)
	#main.cargarRecorrido().
	def cargarRecorrido(self,archivo):
		dicElems = Capturador.cargarRecorrido(archivo)
		dicElems["informados"],hayInformadosCorruptos = Capturador.filtrarFallasConsistentes(dicElems["informados"])
		dicElems["confirmados"],hayConfirmadosCorruptos = Capturador.filtrarFallasConsistentes(dicElems["confirmados"])

		self.capturador.setColCapturasTotales(dicElems["confirmados"])
		self.capturadorInformados.setColCapturasTotales(dicElems["informados"])
		if len(dicElems["confirmados"]) == 0 and len(dicElems["informados"]) == 0:
			raise ExcepcionRecorridoVacio
		print "\nMostrando la coleccion de fallas cargadas: \n"
		self.mostrarColItemFalla()			
		msg = "Existen elementos falla"
		if hayInformadosCorruptos:
			msg += " informados,"
		if hayConfirmadosCorruptos:
			msg += " confirmados"
		msg += " que \nse encuentran inconsistentes y se han ignorado.\nMás información en: %s." %\
					(LOGS_DEFAULT_DIR + LOG_FILE_CAPTURAS_CORRUPTAS_DEFAULT)
		if hayInformadosCorruptos or hayConfirmadosCorruptos:
			self.mostrarDialogoMensaje(title="Carga de fallas",
										text=msg)


	# GuardarRecorrido en menu principal (AlmacenarRecorrido() ).
	# Guarda en un recorrido las fallas (en un archivo .rec) confirmadas e informados de los capturadores
	# y vacia las colecciones de los dos capturadores.
	# "nameBD" es el nombre del archivo de fallas que se guarda en disco.
	def persistirFallas(self,nameBD):
		print "En persistirFallas()\n nameBD: %s ...\n" % nameBD
		print "Mostrando la coleccion de fallas persistidas...\n"
		self.mostrarColItemFalla()
		
		fallas = self.capturador.obtenerCapturasNoSubidas() +\
			self.capturadorInformados.obtenerCapturasNoSubidas()

		
		if len(fallas) == 0:
			print "No existen fallas no subidas para almacenar en recorrido!\n"
			self.mostrarDialogoMensaje( title='Sin fallas no subidas',
										text='No existen fallas (no subidas) para \nalmacenar en un recorrido.'
										)
			return

		print "Existe al menos una falla no subida para almacenar, continuando...\n"
		Capturador.persistirFallas(nameBD,fallas)
		# Se vacian las colecciones de los capturadores al
		# guardar el recorrido.
		self.capturador.setColCapturasTotales([])
		self.capturadorInformados.setColCapturasTotales([])
		print "Fin de persistirFallas()\n"

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
#
#$ python main.py 2>&1 | tee log.txt
#$ python main.py -- --gps realgps 2>&1 | tee log.txt
if __name__ == '__main__':
    MainApp().run()
