#Prueba Con libreria PyPCL
#https://github.com/dimatura/pypcd

import pypcd
import numpy as np
import random
import frame_convert2
import freenect

#Mismo modulo de views/fallanueva/calibkinect.py
from calibkinect import depth2xyzuv


####################################################################
############################# PRUEBA 4 #############################
#  -Almacenamiento de un .pcd con datos RGB y DEPTHS mapeadas
# desde el sensor.
####################################################################



def get_video():
    return freenect.sync_get_video()[0]


def get_video2():
	return frame_convert2.video_cv(freenect.sync_get_video()[0])

#def get_depth():
    #return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])
    #return freenect.sync_get_depth()[0]

def get_depth():
    array,_ = freenect.sync_get_depth()
    return array

def getDatosSensorXYZ():
	xyz, uv = depth2xyzuv(get_depth())
	data = xyz.astype(np.float32)
	return data
	#return xyz


#def getMatrixUV():
#	xyz, uv = depth2xyzuv(get_depth())
#	data = xyz.astype(np.float32)
#	return uv


#uv = getMatrixUV()



dataRGB = get_video()

#Codificacion de RGB para obtener un valor para pypcd
myArr = np.reshape(dataRGB,(480*640,3))
arrFinal = pypcd.encode_rgb_for_pcl(myArr)
arrFinal.shape

#Se obtiene el arreglo de coordenadas x,y,z del sensor Kinect 
dataXYZSensor = getDatosSensorXYZ().tolist()
#"index" es incremental a lo largo de toda la matriz de elementos
for index, elem in enumerate(dataXYZSensor):
	#print "index actual: %s\n" % index
	elem.append(arrFinal[index])

dataXYZRGBSensor = np.asarray(dataXYZSensor,dtype=np.float32)


#pc_xyz = pypcd.make_xyz_point_cloud(dataXYZSensor)
pc_xyz_rgb = pypcd.make_xyz_rgb_point_cloud(dataXYZRGBSensor)



#Guardar .pcd en ASCII
pypcd.save_point_cloud(pc_xyz_rgb,"bar-ascii-sensor.pcd")
#pypcd.save_point_cloud(pc_xyz,"bar-ascii-sensor.pcd")



####################################################################
############################# PRUEBA 3 #############################
# -FUNCIONA OK! Almacenamiento de un .pcd sin datos RGB
####################################################################

def get_video():
    return freenect.sync_get_video()[0]

def get_depth():
    array,_ = freenect.sync_get_depth()
    return array

def getDatosSensorXYZ():
	xyz, uv = depth2xyzuv(get_depth())
	data = xyz.astype(np.float32)
	return data



#Se obtiene el arreglo de coordenadas x,y,z del sensor Kinect 
dataXYZSensor = getDatosSensorXYZ().tolist()
dataXYZRGBSensor = np.asarray(dataXYZSensor,dtype=np.float32)
pc = pypcd.make_xyz_point_cloud(dataXYZSensor)

#Guardar .pcd en ASCII
#pypcd.save_point_cloud(pc,"bar-ascii-sensor.pcd")
#pc.save_pcd("test.pcd")
pc.save_pcd("test.pcd")



####################################################################
############################# PRUEBA 2 #############################
#	-FUNCIONA OK LA CAPTURA DE DATOS XYZ CON RGB(ALEATORIO) CON EL SENSOR.
#
####################################################################

def get_video():
    return freenect.sync_get_video()[0]


def get_video2():
	return frame_convert2.video_cv(freenect.sync_get_video()[0])

#def get_depth():
    #return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])
    #return freenect.sync_get_depth()[0]

def get_depth():
    array,_ = freenect.sync_get_depth()
    return array

def getDatosSensorXYZ():
	xyz, uv = depth2xyzuv(get_depth())
	data = xyz.astype(np.float32)
	return data
	#return xyz


#def getMatrixUV():
	#xyz, uv = depth2xyzuv(get_depth())
	#data = xyz.astype(np.float32)
	#return data
	#return uv


#Se crea un array de prueba con los campos x,y,z,rgb (este ultimo combinado
#en un numero)

#print "VID TIENE: %s\n" % vid
#arrRand_rgb = np.asarray(vid, dtype = np.uint8)

dataRGB = get_video()

#Codificacion de RGB para obtener un valor para pypcd
myArr = np.reshape(dataRGB,(480*640,3))
arrFinal = pypcd.encode_rgb_for_pcl(myArr)
arrFinal.shape

#Se obtiene el arreglo de coordenadas x,y,z del sensor Kinect 
dataXYZSensor = getDatosSensorXYZ().tolist()
for index, elem in enumerate(dataXYZSensor):
	elem.append(arrFinal[index])
dataXYZRGBSensor = np.asarray(dataXYZSensor,dtype=np.float32)
dataXYZRGBSensor = np.asarray(dataXYZSensor,dtype=np.float32)


#pc_xyz = pypcd.make_xyz_point_cloud(dataXYZSensor)
pc_xyz_rgb = pypcd.make_xyz_rgb_point_cloud(dataXYZRGBSensor)



#Guardar .pcd en ASCII
pypcd.save_point_cloud(pc_xyz_rgb,"bar-ascii-sensor.pcd")
#pypcd.save_point_cloud(pc_xyz,"bar-ascii-sensor.pcd")



####################################################################
############################# PRUEBA 1 #############################
####################################################################

#Se crea un array de prueba con los campos x,y,z,rgb (este ultimo combinado
#en un numero)
#arrRand = np.random.rand(40000,4)*255
#arrRand_rgb = np.asarray(arrRand,dtype=np.float32)
#
#pc = pypcd.make_xyz_rgb_point_cloud(arrRand_rgb)

#Guardar .pcd en binary_compressed
#pc.save_pcd('bar.pcd')

#Guardar .pcd en ASCII
#pypcd.save_point_cloud(pc,"bar-ascii.pcd")

