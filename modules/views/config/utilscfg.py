# Funciones para la carga de la configuracion
#import configparser,collections
import ConfigParser as configparser
import collections

# Convierte los datos unicode leidos del archivo de configuracion a  
# un json con strings o int
def convert_unicode(dict_unicode):
    if isinstance(dict_unicode, basestring):
        return str(dict_unicode)
    elif isinstance(dict_unicode, collections.Mapping):
        return dict(map(convert_unicode, dict_unicode.iteritems()))
    elif isinstance(dict_unicode, collections.Iterable):
        return type(dict_unicode)(map(convert_unicode, dict_unicode))
    else:
        return dict_unicode

def leer_configuracion(archivo_configuracion):
	config = configparser.ConfigParser()
	config.read(archivo_configuracion)
	dictionary = {}
	for section in config.sections():
	    dictionary[section] = {}
	    for option in config.options(section):
	        dictionary[section][option] = config.get(section, option)

	my_dict_string = convert_unicode(dictionary)
	return my_dict_string

# conf = leer_configuracion('confViews.cfg')

