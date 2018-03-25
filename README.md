# Instrucciones de instalación de applicación de captura

1. Instalar las librerías necesarias para el funcionamiento  de la aplicación ejecutando los siguientes pasos, probados en Ubuntu 16.05 LTS:

	1.1 Instalar kivy, kivy-garden y dentro de kivy-garden instalar la extensión garden.xpopup:
		sudo apt-get install python-kivy
		s

	1.2 Instalar OpenCV:
		sudo apt-get install python-opencv


	1.3 Instalar cython y python-distutils:
		sudo pip install cython
		sudo apt-get install python-distutils-extra

	1.4 Instalar libusb-1.0-0 libusb-1.0-0-dev de 32bits con:
		sudo apt-get install libusb-1.0-0:i386 libusb-1.0-0-dev:i386

	1.5 Instalar requests y requests-toolbelt: 

		sudo pip install requests requests-toolbelt

	1.6 Instalar Pypcd desde el repositorio https://github.com/dimatura/pypcd:
		
		python setup.py install

	1.7 Instalar Tinydb, ZEO y ZODB:

		pip install tinydb zodb zeo 

		Y adicionalmente, se instalan los modulos de testing de zope con:

		pip install zope.testing zope.interface

2. Instalar los drivers de configuración necesarios para la comunicación con el dispositivo Kinect:

	2.1 Instalar freenect desde https://github.com/OpenKinect/libfreenect con las instrucciones de configuración ahi detalladas.

3. Descargar y descomprimir el código fuente de la aplicación de captura adjunto el cd incluido con la aplicación o disponible en https://github.com/rhuincalef/appCliente.

4. Una vez configurada la aplicación web, modificar en constantes.py el valor de la constante URL_SERVIDOR_LOCAL con la dirección base donde se encuentra configurada la aplicación web y es accesible por los usuarios. Por defecto, se encontrará configurada localmente en http://localhost/web/.

5. Conectar el dispositivo Microsoft Kinect y comprobar la correcta detección de la cámara y el sensor de profundidad con el comando:

   lsusb | grep Kinect 

Si se ejecuta la aplicación antes de conectar el sensor Kinect, se podrá acceder únicamente a funcionalidad de lectura de recorridos desde disco (capturados previamente) y al envío de éstos a la aplicación web. 

6. Ejecutar la aplicación con las instrucciones definidas al final del archivo main.py. Si se desea ejecutar ésta con un ubicaciones reales obtenídas desde un dispositivo GPS incorporado en un smartphone o tablet, se deben seguir las instrucciones definidas en el capítulo 5 en la sección "Conexión vía USB", antes de iniciar la aplicación.
