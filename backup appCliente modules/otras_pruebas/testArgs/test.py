

GPS_TIPO = 'fakegps'
TIPO_CAPTURA = 'xyz_rgb'


import argparse
def validarArgs():
	parser = argparse.ArgumentParser(prog ="main.py", description="Modulo principal de la aplicacion cliente para captura de fallas.")
	parser.add_argument('--gps', metavar='TIPO-GPS',help='Tipo de gps a emplear en la aplicacion. Opciones: fakegps | realgps.Default: fakegps.')
	parser.add_argument('--tipoCaptura', metavar='MODO-CAPTURADOR',help='Tipo de archivos de captura.Opciones: RGB | NO-RGB. Default: RGB.')
	args = parser.parse_args()
	if args.gps is None:
		args.gps = GPS_TIPO 
	if args.tipoCaptura is None:
		args.tipoCaptura =TIPO_CAPTURA
	#parser.print_help()
	return args


args = validarArgs()
print "HOLA MUNDO!!!\n"
print "Los argumentos obtenidos son: --gps= %s ; --tipoCaptura= %s\n" %\
	(args.gps,args.tipoCaptura)
