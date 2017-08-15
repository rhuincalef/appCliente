<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');

/*
|--------------------------------------------------------------------------
| File and Directory Modes
|--------------------------------------------------------------------------
|
| These prefs are used when checking and setting modes when working
| with the file system.  The defaults are fine on servers with proper
| security, but you may wish (or even need) to change the values in
| certain environments (Apache running a separate process for each
| user, PHP under CGI with Apache suEXEC, etc.).  Octal values should
| always be used to set the mode correctly.
|
*/
define('FILE_READ_MODE', 0644);
define('FILE_WRITE_MODE', 0666);
define('DIR_READ_MODE', 0755);
define('DIR_WRITE_MODE', 0777);

/*
|--------------------------------------------------------------------------
| File Stream Modes
|--------------------------------------------------------------------------
|
| These modes are used when working with fopen()/popen()
|
*/

define('FOPEN_READ',							'rb');
define('FOPEN_READ_WRITE',						'r+b');
define('FOPEN_WRITE_CREATE_DESTRUCTIVE',		'wb'); // truncates existing file data, use with care
define('FOPEN_READ_WRITE_CREATE_DESTRUCTIVE',	'w+b'); // truncates existing file data, use with care
define('FOPEN_WRITE_CREATE',					'ab');
define('FOPEN_READ_WRITE_CREATE',				'a+b');
define('FOPEN_WRITE_CREATE_STRICT',				'xb');
define('FOPEN_READ_WRITE_CREATE_STRICT',		'x+b');

/*
|--------------------------------------------------------------------------
| Custom Constants - Change these as appropriate
|--------------------------------------------------------------------------
*/

define('WEBSITE_NAME', 'Your website name');
define('SLOGAN', "Your slogan");

define('TWITTER_ACCOUNT', ''); // e.g. ollierattue
define('FACEBOOK_URL', ''); // e.g. http://facebook.com/crashouts

define('BLOG_RSS_URL', '');
define('TWITTER_RSS_URL', 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name='.TWITTER_ACCOUNT);

define('SUPPORT_EMAIL', ''); // Displayed to users
define('DEVELOPER_EMAIL', ''); // Notifications / Errors sent to this address
define("SYSTEM_EMAIL", "system@${_SERVER['HTTP_HOST']}"); // From email for amnesia, autoresponder, error logs etc


//API-KEY de GoogleMaps
define('API_KEY_GOOGLE_MAPS','AIzaSyDrSwzqn60EgqwOk7a9U68PlLHqT8LtsBI');

//Constante para la autenticacion de geonames.org
define('APP_CLIENTE_ID', 'appclientetw'); // Displayed to users

//Constantes para el uso de Composer
define('AUTO_LOAD_NAME_COMPOSER','vendor/autoload.php');

//Constantes de geonames
define('GEONAMES_BASE_PATH',$_SERVER['DOCUMENT_ROOT']."/repoProyectoBacheo/web/geonames-api/");
define('MODULE_GEONAMES_PATH','src/Geonames.php');
define('MODULE_RESPONSE_PATH','src/Response.php');

//Constantes para geocoderPhp
define('GEOCODER_PHP_BASE_PATH',$_SERVER['DOCUMENT_ROOT']."/repoProyectoBacheo/web/geocoderPhp/");
define('MODELS_PATH',$_SERVER['DOCUMENT_ROOT']."/repoProyectoBacheo/web/application/models/");

define('MODULE_CURL_ADAPTER_HTTP','vendor/egeloen/http-adapter/src/CurlHttpAdapter.php');
define('MODULE_EXCEPCION_LAT_LONG','ExcepcionLatLng.php');
define('EXCEPCION_HTTP_ADAPTER','vendor/egeloen/http-adapter/src/HttpAdapterException.php');




//Constantes para la Latitud y long
define('REGEX_LAT_LONG','/([0-9.-]+).+?([0-9.-]+)/');

//Nombre de la ciudad actual.
define('NOMBRE_LOCALIDAD','Trelew');




// Constantes para los estados relacionados a las peticiones de direcciones
// NOTA: Se define DIRECCION_PHP que significa direccion.php (modulo donde se retorna) y PETICION_GEOCODING_OK lo que significa ese valor.

define('DIRECCION_PHP_FALLA_REGISTRADA_OK',10);

//Peticiones locales a la rest_api del servidor.
define('PETICION_REST_OK',200);
define('PETICION_REST_FALLO',500);

define('FALLA_ANONIMA_INICIALIZADA_OK',20);



define('DIRECCION_PHP_PETICION_GEOCODING_OK',0);
define('DIRECCION_PHP_DIRECCION_NO_RETORNADA',-1);
define('DIRECCION_PHP_PETICION_SIN_RESULTADOS',-2);
define('DIRECCION_PHP_QUOTA_EXCEDIDA',-3);
define('DIRECCION_PHP_OPERACION_GEOCODING_NO_SOPORTADA',-4);
define('DIRECCION_PHP_API_KEY_INVALIDA',-5);
define('DIRECCION_PHP_LAT_LONG_NO_VALIDAS',-6);

define('DIRECCION_PHP_HTTP_ADAPTER_TIMEOUT_EXCEDIDO',-7);
define('DIRECCION_PHP_EXCEPCION_GENERICA',-8);


define('DIRECCION_PHP_PETICION_INTERSECCION_FALLIDA',-9);
define('DIRECCION_PHP_INTERSECCION_TIMEOUT_EXCEDIDO',-10);
define('FALLA_PHP_CALLE_NO_DISPONIBLE',-11);
define('DIRECCION_PHP_LAT_LONG_FUERA_CIUDAD',-12);


define('FALLA_INVALIDA',-13);


//Constantes para el comentario por default que se inserta en la BD
define('NOMBRE_EMPLEADO_VIAL_DEFAULT','Empleado vial');
define('EMAIL_EMPLEADO_VIAL_DEFAULT','municipalidad.tw@gmail.com');
define('CALLE_NO_OBTENIDA','Calle no calculada');






/* End of file constants.php */
/* Location: ./application/config/constants.php */