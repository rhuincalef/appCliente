#import signal, os
#import time

#TIMEOUT_KINECT_SEG = 5 

#class ExcepcionTimeout(Exception):
#	pass

#def handlerTimeout(signum, frame):
#	print 'Llamando al manejador!\n'
#	raise ExcepcionTimeout("Error al abrir el dispositivo.\n Dispositivo ocupado\n")

#def getKinectData(funcion):
	# Set the signal handler and a 5-second alarm
#	signal.signal(signal.SIGALRM, handlerTimeout)
#	signal.alarm(TIMEOUT_KINECT_SEG)
#	funcion()
#	signal.alarm(0) # Disable the alarm


#def miFuncion():
#	print "Llamando a mi funcion!\n"
#	time.sleep(10)


#Otro programa...
#try:
#	print "INSTRUCCION 1...\n"
#	getKinectData(miFuncion)
#	print "INSTRUCCION 2...\n"
#except ExcepcionTimeout as e:
#	msg = "ExcepcionTimeout ocurrida:\n %s\n" % e
#	print msg

##################################################################
#import freenect
#try:
#	e = freenect.s
#except Exception as e:#
#	raise e

#########################################################################################
####################### MANIPULACION MANUAL DE KINECT CON FREENECT#######################
#########################################################################################

import freenect, threading
import signal, os
context = freenect.init()
dev = freenect.open_device(context,0)

#Modificar el dispositivo con el Dev,grados_deseados
#freenect.set_tilt_degs(dev,1)

depths = None
finalizar_captura = False

def handler(signum, frame):
	global context
	global dev
	global finalizar_captura
	print "Interrumpido el proceso, cerrando dispositivo\n"
	finalizar_captura = True


def callbackDepth(dev, depth, timestamp):
	global depths
	print "Obtenida depth en %s\n ..." % timestamp
	print "depth:\n %s\n" % depth[0]
	depths = depth


def callbackBody(dev,ctx):
	print "Llamada la funcion callbackBody! freenect.num_devices(context) = %s \n" % freenect.num_devices(ctx)
	if finalizar_captura:
		print "Cerrando dispositivo...\n"
		freenect.close_device(dev)
		freenect.shutdown(ctx)		
		raise freenect.Kill()
	#if depths is not None:
	#	print "Matando el runloop...\n"
	#	freenect.close_device(dev)
	#	freenect.shutdown(ctx)
	#	raise freenect.Kill()



#def callbackVideo(dev, video, timestamp):
#	pass

#freenect.runloop(depth=callbackDepth,video=callbackVideo,dev=dev)
#freenect.set_depth_callback(dev,callbackDepth)
#NOTA IMPORTANTE: Cuando se interrumpe esta funcion, el recurso no se libera
# por lo que al ejecutarla de nuevo, el dispositivo se encuentra bloqueado
def fnConcurrente():
	try:
		while True:			
			freenect.runloop(depth=callbackDepth,body=callbackBody,dev=dev)
			print "Reconectando sensor...\n"
			#time.sleep(2)
			if freenect.num_devices(context) == 0:
				print "NO hay sensor detectado!\n"
			else:
				print "Detectado sensor!\n"
	except Exception as e:
		print "Excepcion generica! %s\n" % e

#Configuracion de la interrupcion
signal.signal(signal.SIGINT, handler)

fnConcurrente()
#t = threading.Thread(target=fnConcurrente)
#t.setDaemon(True)
#t.start()
#t.join()

#...
#freenect.close_device(dev)

#########################################################################
#import signal, os
#import time
#import freenect

#TIMEOUT_KINECT_SEG = 5 

#class ExcepcionTimeout(Exception):
#	pass

#def handlerTimeout(signum, frame):
#	print 'Llamando al manejador!\n'
#	raise ExcepcionTimeout("Error al abrir el dispositivo.\n Dispositivo ocupado\n")

#def getKinectData(funcion):
#	# Set the signal handler and a 5-second alarm
#	signal.signal(signal.SIGALRM, handlerTimeout)
#	signal.alarm(TIMEOUT_KINECT_SEG)
##	print funcion()[0]
#	signal.alarm(0) # Disable the alarm


#Otro programa...
#try:
#	print "INSTRUCCION 1...\n"
#	getKinectData(freenect.sync_get_depth)
#	print "INSTRUCCION 2...\n"
#except ExcepcionTimeout as e:
#	msg = "ExcepcionTimeout ocurrida:\n %s\n" % e
#	print msg
#	freenect.Kill()
#	print "Detenido el runloop principal!!\n"

############################################################################################
#################### DETECCION DE CONEXION ED DISPOSITIVOS USB EN PYTHON ###################
############################################################################################
# $sudo pip install pyudev
#import pyudev

#context = pyudev.Context()
#monitor = pyudev.Monitor.from_netlink(context)
#monitor.filter_by(subsystem='usb')
#for device in iter(monitor.poll, None):
#	if device.action == 'add':
#		print "device.values: %s\n" % device.values()
#		print('{} connected'.format(device))
#		print('{0} ({1})'.format(device.device_node, device.device_type))
		# do something



#from pyudev import Context, Monitor, MonitorObserver
#context = Context()
#monitor = Monitor.from_netlink(context)
#monitor.filter_by(subsystem='input')
#def print_device_event(device):
#	print('background event {0.action}: {0.device_path}'.format(device))
#observer = MonitorObserver(monitor, callback=print_device_event, name='monitor-observer')
#observer.start()
#...
#observer.stop()



#Obtener el idProducto y vendedor de dispositivo usb con PyUsb.
# NOTA: El ID de dispositivo que se muestra con $libusb desde Linux, son
# en raelidad conformados por el idVendor+':'+idProduct
# NOTA2: Los ids de los dispositivos del kinect son:
#			- ID 045e:02ae Microsoft Corp. Xbox NUI Camera
#			- ID 045e:02b0 Microsoft Corp. Xbox NUI Motor
#			- ID 045e:02ad Microsoft Corp. Xbox NUI Audio
#			- ID 0409:005a NEC Corp. HighSpeed Hub
#
# Instalacion de PyUsb -->
#$ sudo pip install pyusb

#import usb
#busses = usb.busses()
#for bus in busses:
#	devices = bus.devices
#	for dev in devices:
#		print "Device:%s\n" % dev.filename
#		print "  idVendor: %d 0x(%04x)" % (dev.idVendor, dev.idVendor)
#		print "  idProduct: %d 0x(%04x)" % (dev.idProduct, dev.idProduct)





#Monitoreo asincrono -->
#from pyudev import Context, Monitor, MonitorObserver
#import usb
#from sensordata import *

#Retorna un str de hex sin el prefijo '0x'
#def convertirAHex(valor):
#	cadena = "%04x" % valor
#	return cadena

# Escanea los puertos USB y retorna True si todos los dispositivos
# estan listos.
#def estaSensorListo():
#	busses = usb.busses()
#	CAMERA_OK = MOTOR_OK = AUDIO_OK = HUB_OK = False
#	for bus in busses:
#		devices = bus.devices
##		for dev in devices:
#			idDev = convertirAHex(dev.idVendor) + ":" + convertirAHex(dev.idProduct)
#			print "Device:%s\n" % dev.filename
#			print "  idVendor: %d 0x(%04x)" % (dev.idVendor, dev.idVendor)
#			print "  idProduct: %d 0x(%04x)" % (dev.idProduct, dev.idProduct)
#			print "idDev= %s; ID_USB_CAMERA: %s\n" % (idDev,ID_USB_CAMERA)
#			print "-----------------------------------------------\n\n"
#
#			if idDev == ID_USB_CAMERA:
#				print "Camara detectada!\n"
#				CAMERA_OK = True
#			if idDev == ID_USB_MOTOR:
#				print "Motor detectada!\n"
#				MOTOR_OK = True
##			if idDev == ID_USB_AUDIO:
#				print "Audio detectada!\n"
#				AUDIO_OK = True
##			if idDev == ID_USB_HUB:
##				print "HUB detectado!\n"
#				HUB_OK = True
#	return CAMERA_OK and MOTOR_OK and AUDIO_OK and HUB_OK 
	



#Metodo que estara en MainApp.py
#def handlerSensorConectado(action,device):
#	print "Conexion de sensor ocurrida con device: %s\n" % device
#	print "Accion: %s\n" % action
#	if estaSensorListo():
#		#TODO: Aca se debe cambiar el atributo controlador.sensorListo a TRUE.
#		print "Modificado controlador.sensorListo() a True!\n"
##	else:
#		print "Modificado controlador.sensorListo() a False!\n"
#	print "Si no esta iniciado el thread observer iniciarlo sino nada !\n"



#context = Context()
#monitor = Monitor.from_netlink(context)
#monitor.filter_by(subsystem = 'usb')
#observer = MonitorObserver(monitor,
#									event_handler=handlerSensorConectado,
#									name='thread-observerMonitor')
#observer.start()

#TODO: CUANDO LA Aplicacion termine se debe finalizar el thread con
# observer.stop() (Opcional)
#print "Esperando a que termine el thread observer...\n"
#observer.join()
#print "Termino!!!\n"
