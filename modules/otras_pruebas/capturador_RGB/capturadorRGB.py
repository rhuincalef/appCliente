#Prueba Con libreria PyPCL
#https://github.com/dimatura/pypcd

import pypcd
import numpy as np
import random
import freenect
from calibkinect import xyz_complete_matrix

## Prueba a realizar ejecutar en este orden:
# 0.freenect.sync_get_video() --> Se obtiene el arreglo RGB de aca sin empaquetar de PCL.
# 1. pypcd.encode_rgb_for_pcl?? -->Output is Nx1 float32 array with bit-packed RGB, for PCL.
# 2. pypcd.make_xyz_rgb_point_cloud?? -->Se toma el arreglo de RGB empaquetado del metodo anterior con las coordenadas.

#Funciones auxiliares -->

#-Se empaqueta cada una de las 480 filas individualmente y obtienen los
# 640 valores codificados, para cada pixel en la imagen.



#Main
rgbSinCod = freenect.sync_get_video()[0]
rgbConCod = list()
for x in xrange(0,len(rgbSinCod)):
	filaRgbEmpaquetado = pypcd.encode_rgb_for_pcl(rgbSinCod[x])
	rgbConCod.append(filaRgbEmpaquetado)

npRgbConCod = np.asarray(rgbConCod,dtype=np.float32)

depth = freenect.sync_get_depth()[0]
#Se extraen todas las coordenadsa con todas las coordenadas en eje Z
xyzCoords = xyz_complete_matrix(depth)
npXyzCoords = np.asarray(xyzCoords,dtype=np.float32)



#Se une el rgb empaquetado con cada coordenada x,y,z
dataNube = np.empty((480*640,4),dtype=np.float32)
rgbAplanado = npRgbConCod.flatten()
for index in xrange(0,len(rgbAplanado)-1):
	print "INdex = %s\n" % index
	dataNube[index,:] = np.append(npXyzCoords[index],rgbAplanado[index])



#nubeFinal = dataNube.reshape((480,640,4))
print "LLENADA dataNube! tipo: %s \n" % dataNube.dtype

#Combinar las coordenadas xyz con los valores rgb empaquetados
#pc_rgb = pypcd.make_xyz_rgb_point_cloud(dataNube)
#pc_rgb.save_pcd('bar_rgb.pcd')

#Se elmina el elemento Z (indice 2) que es menor a cero(Incluido en la funcion
#original depth2xyzuv que hace el filtrado de los elementos que estan detras de la camara). 
dataNube2 = np.asarray([x for x in dataNube if x[2]<0 ],dtype=np.float32)
pc_rgb2 = pypcd.make_xyz_rgb_point_cloud(dataNube2)
pc_rgb2.save_pcd('bar_rgb_v2.pcd')

