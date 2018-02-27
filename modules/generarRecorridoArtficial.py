#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script para la generacion de recorridos artificiales con muestras 
# previamente capturadas. Empleado para la subida de fallas clasificables al servidor
# en la demostracion.



# Ejemplo de invocación -->
# $ python generarRecorridoArtficial.py -- --path_archivos "lala.pcd"



import sys, os
import argparse

from utils import cargarConfiguraciones

from apiclient1 import *
from capturador import *
from captura import *
#from estadofalla import *


def procesarArgumentos():
	parser = argparse.ArgumentParser(prog ="generarRecorridoArtificial.py", description="Generacion de recorridos artificiales con pcds propios")
	parser.add_argument('--path_archivos', nargs='+', metavar='Ruta-Archivo-PCD',help='Ruta del el/los archivo/s .PCD a ser agregados en el recorrido')
	args = parser.parse_args()
	if args.path_archivos is None:
		print "Error no existen .pcd para agregar en la captura!!!"
		try:
			sys.exit(1)
		except Exception as e:
			pass
	diccArgs = vars(args)
	return [elemento for elem in diccArgs.itervalues() for elemento in elem ]




##################################  Main  ###########################################

colPathPcds = procesarArgumentos()
cargarConfiguraciones()
print "colPathPcds -->%s" % colPathPcds

apiClientComun = ApiClientApp()
bdLocalMuestrasComun = BDLocal(fullPathBD = None)
capturador = Capturador(apiClientComun,bdLocalMuestrasComun)
nombreArchivoRec = "recorrido_artificial.rec"


colItems = list() # Lista de objetos ItemFalla
for pcd in colPathPcds:
	nombrePcd = pcd.split(".")[0]
	print "iterando elemento: %s, spliteado: %s\n" % (pcd, nombrePcd)
	item1 = ItemFalla()
	#Se crea el estado asociado a los atributos con los datos que emplea el servidor
	#Coordenada fake -->
	#est = Confirmada(-33432122,44212112)
	#Coordenada real -->
	est = Confirmada(-43.252563,-65.326809)
	est.setTipoFalla("baches")
	est.setCriticidad("bajo")
	est.setTipoMaterial("pavimento flexible")

	item1.setEstado(est)
	cap1 = Captura(nombrePcd, os.getcwd(), FORMATO_CAPTURA, EXTENSION_ARCHIVO)

	#Se establece el nombre final del archivo de captura
	nombFin = cap1.getNombreArchivo() + cap1.getExtension()
	print "Nombre de archivo final: %s\n" % nombFin
	cap1.setNombreArchivoCaptura(nombFin)

	#Se registra la captura con la falla
	#Estado.registrar(self,item_falla,capturador,captura)
	item1.getEstado().registrar(item1,capturador,cap1)
	colItems.append(item1)

print "Agregadas capturas a la coleccion!\n"

Capturador.almacenarCapturasEnDisco(nombreArchivoRec,
										colItems)
print "Guardado recorrido artificial en archivo: %s\n" % nombreArchivoRec


