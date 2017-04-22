import ZODB, ZODB.FileStorage
import time
import BTrees.OOBTree

from capturador import * #Definicion de itemFalla
from estadofalla import * #Definicion de Estado
import transaction
from zc.lockfile import LockError

#Interfaz para la creacion de procesos
from multiprocessing import Process, Pipe, Queue



#Almacena una coleccion de itemfalla en una BDOO 
#def almacenarRecorrido(connection,colItemFalla,clave='recorridoInformados'):
	#Se crea la BD con un prefijo predefinido + fecha actual
#	root = connection.root
	#Se crea la estructura por la cual se accedera a la colCapturas, 
	#definiendo un espacio de nombres "recorrido".
#	if clave == 'recorridoInformados':
#		root.recorridoInformados = BTrees.OOBTree.BTree()
#	else:
#		root.recorridoConfirmados = BTrees.OOBTree.BTree()

#	for falla in colItemFalla:
#		if clave == 'recorridoInformados':
#			root.recorridoInformados[colItemFalla.index(falla)] = falla 
#		else:
#			root.recorridoConfirmados[colItemFalla.index(falla)] = falla 
		#root.recorrido[colItemFalla.index(falla)] = falla
	#Se asientan los cambios en la BD
#	transaction.commit()
	


def almacenarRecorrido(connection,colItemFalla,clave='recorridoInformados'):
	#Se crea la BD con un prefijo predefinido + fecha actual
	root = connection.root
	#Se crea la estructura por la cual se accedera a la colCapturas, 
	#definiendo un espacio de nombres "recorrido".
	root.recorridoInformados = BTrees.OOBTree.BTree()
	root.recorridoConfirmados = BTrees.OOBTree.BTree()

	for falla in colItemFalla:
		if isinstance(falla.getEstado(),Informado):
			root.recorridoInformados[colItemFalla.index(falla)] = falla 
		else:
			root.recorridoConfirmados[colItemFalla.index(falla)] = falla 
		#root.recorrido[colItemFalla.index(falla)] = falla
	#Se asientan los cambios en la BD
	transaction.commit()

#Retorna una coleccion de itemFalla de la BD, pertenecientes a un recorrido
def obtenerRecorrido(conn,clave):
	print "En obtenerRecorrido...\n"
	raiz = conn.root()
	colElems = list()
	for index in raiz[clave]:
	 	colElems.append(raiz[clave][index])
	return colElems


#Retorna la conexion  abierta a la DBOO
def abrirConexion(nombre):
	storage = ZODB.FileStorage.FileStorage(nombre)
	db = ZODB.DB(storage)
	connection = db.open()
	return connection

def cerrarConexion(connection):
	connection.close()
	print "Cerrando conexion!\n"
	
#Almacena la coleccion actual de capturas en disco
def almacenarCapturasEnDisco(pipeConn,name_db):
	#Se forkea el proceso debido a que ZODB no permite el acceso
	# desde el mismo proceso a una falla	
	print "Inicio con name_db: %s\n" % name_db
	conn = abrirConexion(name_db)
	almacenarRecorrido(conn,colItems)
	#transaction.commit()
	cerrarConexion(conn)
	#Se envia el estado al pipe
	pipeConn.send('OK')
	#pipeConn.close()


#Lee las capturas que estan informadas y confirmadas
def leerCapturasDesdeDisco(pipeConn,name_db):
	#Se obtiene el recorrido
	print "Obteniendo recorrido...\n"
	conn1 = abrirConexion(name_db)
	dicElems = {}
	dicElems["informados"] = obtenerRecorrido(conn1,'recorridoInformados') 
	dicElems["confirmados"] = obtenerRecorrido(conn1,'recorridoConfirmados') 
	print "Obtenido el recorrido con las capturas!\n"
	pipeConn.send(dicElems)
	pipeConn.close()
	cerrarConexion(conn1)



#Se crea una coleccion de prueba
colItems = list()

item1 = ItemFalla()
est = Informado(1,"Belgrano",1100)
item1.setEstado(est)
cap1 = Captura("rodrigo1.pcd")
item1.agregarCap(cap1)
cap2 = Captura("rodrigo2.pcd")
item1.agregarCap(cap2)
cap3 = Captura("rodrigo3.pcd")
item1.agregarCap(cap3)

colItems.append(item1)

item1 = ItemFalla()
est = Confirmado(-33432122,44212112)
item1.setEstado(est)
cap1 = Captura("guillermo1.pcd")
item1.agregarCap(cap1)
cap2 = Captura("guillermo2.pcd")
item1.agregarCap(cap2)
cap3 = Captura("guillermo3.pcd")
item1.agregarCap(cap3)

colItems.append(item1)

#Se guarda el recorrido
name_db = 'recorrido-%s.db' % time.strftime("%d-%m-%Y")

print "Iniciando el guardado...\n"
parent_conn1, childAlmacenarCaps = Pipe()
p = Process(target=almacenarCapturasEnDisco, args=(childAlmacenarCaps,name_db))
p.start()

#Se bloquea el proceso padre hasta que se lea algo desde el PIPE 
status = parent_conn1.recv()
print "Status: %s\n" % status
print "Iniciada la lectura de datos almacenados..\n"


#q = Queue()
#p = Process(target=leerCapturasDesdeDisco, args=(q,name_db,))
#p.start()
#print "Esperando el envio de datos desde el subproceso...\n"
#Se bloquea el proceso padre hasta que se lea algo desde el PIPE 
#colElems = q.get()

parent_conn2, childLeerCaps = Pipe()
p = Process(target=leerCapturasDesdeDisco, args=(childLeerCaps,name_db,))
p.start()
print "Esperando el envio de datos desde el subproceso...\n"
#Se bloquea el proceso padre hasta que se lea algo desde el PIPE 
dicElems = parent_conn2.recv()
colElems = dicElems["informados"] + dicElems["confirmados"]

print "Mostrando los elementos enviados desde el proceso: \n"
for e in colElems:
	print "%s\n" % e
