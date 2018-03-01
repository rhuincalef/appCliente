#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script para la generacion de recorridos artificiales con muestras 
# previamente capturadas. Empleado para la subida de fallas clasificables al servidor
# en la demostracion.



# Ejemplo de invocación -->
# $ python generarRecorridoArtficial.py -- --path_archivos "lala.pcd"

# python generarRecorridoArtficial.py -- --arch_salida "RECORRIDOS_TESTING_CLASIFICADOR/bache/rec_bache.rec" --path_archivos "RECORRIDOS_TESTING_CLASIFICADOR/bache/baches_9.pcd" 2>&1 | tee generador.txt
# python generarRecorridoArtficial.py -- --arch_salida "RECORRIDOS_TESTING_CLASIFICADOR/grieta/rec_grieta.rec" --path_archivos "RECORRIDOS_TESTING_CLASIFICADOR/grieta/grieta_1.pcd" 2>&1 | tee generador.txt


import sys, os
import argparse

from utils import cargarConfiguraciones

from apiclient1 import *
from capturador import *
from captura import *
#from estadofalla import *


def procesarCapturas():
	parser = argparse.ArgumentParser(prog ="generarRecorridoArtificial.py", description="Generacion de recorridos artificiales con pcds propios")
	parser.add_argument('--arch_salida', metavar='Archivo-Recorrido-Salida',help='Ruta completa del archivo de recorrido de salida')
	parser.add_argument('--path_archivos', nargs='+', metavar='Ruta-Archivo-PCD',help='Ruta del el/los archivo/s .PCD a ser agregados en el recorrido')
	args = parser.parse_args()
	if args.path_archivos is None:
		print "Error no existen .pcd para agregar en la captura!!!"
		try:
			sys.exit(1)
		except Exception as e:
			pass
	diccArgs = vars(args)
	#lista = [elemento for elem in diccArgs.itervalues() for elemento in elem ]
	lista = []
	for e in diccArgs.itervalues():
		print "elemento: %s\n" % e
		if type(e) is list:
			print "armada lista!\n"
			lista = [myelem for myelem in e]
		
	print "lista: %s" % lista
	print "arch_salida: %s\n" % args.arch_salida
	#try:
	#	print "Saliendo...\n"
	#	sys.exit(1)
	#except Exception as e:
	#	pass

	if args.arch_salida is None:
		print "Error no existen un archivo de salida para el recorrido!!!"
		try:
			sys.exit(1)
		except Exception as e:
			pass
	salida = args.arch_salida
	return (lista,salida)


##################################  Main  ###########################################

tupla = procesarCapturas()
colPathPcds = tupla[0]
nombreArchivoRec = tupla[1] 
print "Nombre de colPathPcds: %s\n" % colPathPcds
print "Nombre de archivo de recorrido: %s\n" % nombreArchivoRec


cargarConfiguraciones()
print "colPathPcds -->%s" % colPathPcds

apiClientComun = ApiClientApp()
bdLocalMuestrasComun = BDLocal(fullPathBD = None)
capturador = Capturador(apiClientComun,bdLocalMuestrasComun)
#nombreArchivoRec = "recorrido_artificial.rec"


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


