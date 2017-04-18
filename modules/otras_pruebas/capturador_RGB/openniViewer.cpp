// Original code by Geoffrey Biggs, taken from the PCL tutorial in
// http://pointclouds.org/documentation/tutorials/pcl_visualizer.php

// Simple OpenNI viewer that also allows to write the current scene to a .pcd
// when pressing SPACE.

// 1. Librerias a instalar para probar openniViewer
//		-sudo apt-get install libopenni2-0 libopenni2-dev
// 2. Agregar la siguiente linea a CMakeLists.txt file: 
// 		-list(REMOVE_ITEM PCL_LIBRARIES "vtkproj4")


// Ejecucion del script: 
// ./openniViewer pepito5.pcd

#include <stdlib.h> 

#include <pcl/io/openni_grabber.h>
#include <pcl/io/pcd_io.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/console/parse.h>

#include <iostream>

using namespace std;
using namespace pcl;

//PointCloud<PointXYZRGBA>::Ptr cloudptr(new PointCloud<PointXYZRGBA>); // A cloud that will store color info.
//PointCloud<PointXYZ>::Ptr fallbackCloud(new PointCloud<PointXYZ>);    // A fallback cloud with just depth data.
Grabber* openniGrabber;                                               // OpenNI grabber that takes data from the device.
string filename;

// This function is called every time the device has new data.
//void grabberCallback(const PointCloud<PointXYZRGBA>::ConstPtr& cloud)
int grabberCallback(const PointCloud<PointXYZRGBA>::ConstPtr& cloud)
{

	try { // start a try block
		std::cout << "Entre en grabberCallback() ..." << std::endl;	
		//stringstream stream;
		//string filename = stream.str();
		std::cout << "Abierto el stream para el filename" << std::endl;
		std::cout << "filename: " << filename << std::endl;
		//if (io::savePCDFileASCII(filename, *cloud) == 0)
		if (io::savePCDFile(filename, *cloud,false) == 0)
		{
			cout << "Guardado correctamente " << filename << "." << endl;
		}
		else PCL_ERROR("Problema al guardar el archivo de nube de puntos %s.\n", filename.c_str());
		std::cout << "Despues del if" << std::endl;
		//Se detiene el opennigrabber
		openniGrabber->stop();
		std::cout << "Se detuvo openniGrabber! " << std::endl;
		exit(0);
		
	}catch (pcl::IOException ex) { // catch an error
		std::cout << "Excepcion en grabberCallback()" << std::endl;
		return -1;
	}
}


int
main(int argc, char** argv)
{
	/*if (console::find_argument(argc, argv, "-h") >= 0)
	{
		std::cout << "Error en los argumentos del script. " << std::endl;
		return -1;
	}*/
	std::cout << "Entre en main!" << std::endl;
	if (argc != 2)
	{
		std::cout << "Error en los argumentos del script. " << std::endl;
		std::cout << "-Ejecucion: [" << argv[0] << "]" << " " << "FILE.pcd" << std::endl;
		return -1;
	}
	filename = argv[1];
	std::cout << "filename enviado: " << filename << std::endl;


	try{
		// Se crea el openniGrabber y se registra el callback 
		// que obtiene la pointcloud en RGBA mostrada por el sensor.
		openniGrabber = new OpenNIGrabber();
		std::cout << "Creado openniGrabber " << std::endl;		
		if (openniGrabber == 0){
			std::cout << "ERROR al crear opennigrabber" << std::endl;
			return -1;
		}
		std::cout << "Creado opennigrabber" << std::endl;
		boost::function<void (const PointCloud<PointXYZRGBA>::ConstPtr&)> f =
			boost::bind(&grabberCallback, _1);
		openniGrabber->registerCallback(f);
		std::cout << "registrada callback!" << std::endl;
		openniGrabber->start();
		std::cout << "Iniciado openniGrabber..." << std::endl;
		boost::this_thread::sleep(boost::posix_time::seconds(1.5));
		abort();
		return 0;
	}catch (pcl::IOException ex) { // catch an error
		std::cout << "Excepcion en main()" << std::endl;
		return -1;
	}
	
}