<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');
/*
| -------------------------------------------------------------------------
| URI ROUTING
| -------------------------------------------------------------------------
| This file lets you re-map URI requests to specific controller functions.
|
| Typically there is a one-to-one relationship between a URL string
| and its corresponding controller class/method. The segments in a
| URL normally follow this pattern:
|
|	example.com/class/method/id/
|
| In some instances, however, you may want to remap this relationship
| so that a different class/function is called than the one
| corresponding to the URL.
|
| Please see the user guide for complete details:
|
|	http://codeigniter.com/user_guide/general/routing.html
|
| -------------------------------------------------------------------------
| RESERVED ROUTES
| -------------------------------------------------------------------------
|
| There area two reserved routes:
|
|	$route['default_controller'] = 'welcome';
|
| This route indicates which controller class should be loaded if the
| URI contains no data. In the above example, the "welcome" class
| would be loaded.
|
|	$route['404_override'] = 'errors/page_missing';
|
| This route will tell the Router what URI segments to use if those provided
| in the URL cannot be matched to a valid route.
|
*/

$route['default_controller'] = "publico";
$route['404_override'] = 'errori/error_404';
$route['get(TiposEstado|Niveles|TiposRotura|TiposDeMateriales)'] = 'publico/get$1';
$route['get(Falla|Observaciones|Multimedia|Estado|Estados)/(\d+)'] = 'publico/get$1/$2';

$route['get[^(Falla|Observaciones|Multimedia|Estado|Estados)]'] = 'error/error_404';
$route['login'] = 'publico/login_via_ajax';
$route['logout'] = 'publico/logout';
$route['creacionTipoFalla'] = 'publico/creacionTipoFalla';

$route['get(TiposDeMateriales)'] = 'privado/get$1';
// $route['get(TipoDeMaterial|TipoDeReparacion)/(\d+)'] = 'privado/get$1/$2';
$route['get(TipoMaterial|TipoDeReparacion)/(\d+)'] = 'publico/get$1/$2';

/*{3,6}     Between 3 and 6 of characters, tener en cuenta*/
$route['crearTipoAtributo/(\d+)/([\w]+)/([\w]+)'] = 'publico/crearTipoAtributo/$1/$2/$3';
$route['getCriticidades'] = 'publico/getCriticidades';
$route['getLazyTiposFalla/(\d+)'] = 'publico/getLazyTiposFalla/$1';

// Restringir a los necesarios
$route['get/(TipoReparacion|Criticidad|TipoMaterial)/(\d+)'] = 'publico/get/$1/$2';
//$route['getAll/(TipoReparacion|Criticidad|TipoMaterial)'] = 'publico/getAll/$1';
$route['getAll/(TipoReparacion|Criticidad|TipoMaterial|TipoEstado)'] = 'publico/getAll/$1';
$route['crear/(TipoReparacion|TipoFalla|TipoMaterial|Falla)'] = 'publico/crear/$1';



// $route['crearFallaAnonima'] = 'invitado/crearFallaAnonima/$1';
$route['crearFallaAnonima'] = 'publico/crearFallaAnonima/$1';


$route['getTiposFalla/(\d+)'] = 'publico/getTiposFalla/$1';

$route['getFallasPorCalle'] = 'publico/getFallasPorCalle';

$route['getAlly/(TipoMaterial)'] = 'publico/getAlly/$1';
$route['gety/(TipoFalla)/(\d+)'] = 'publico/gety/$1/$2';

$route['getTiposReparacionPorIDs'] = 'publico/getPorIds/TipoReparacion';
$route['getTiposFallaPorIDs'] = 'publico/getTiposFallaPorIDs';
// $route['getCriticidadesPorIDs'] = 'publico/getCriticidadesPorIDs';
$route['getBaches'] = 'publico/getBaches';
$route['inicio/getBache/id/(\d+)'] = 'publico/getFalla/$1';

$route['obtenerObservaciones/(\d+)'] = 'publico/obtenerObservaciones/$1';
$route['asociarObservacion'] = 'publico/asociarObservacion';
$route['inicio/cambiarEstadoBache'] = 'publico/modificarEstado';


$route['registrarUsuario'] = 'publico/registrarUsuario';
$route['create_user'] = 'publico/create_user';


// Ruta para el metodo que genera los datos para el thumbnail.
$route['obtenerDatosVisualizacion/(\d+)'] = "publico/obtenerDatosVisualizacion/$1";


// Ruta REST para la subida de archivos desde la appCliente
// $route['restapi/upload_pcd'] = "publico/prueba";
// $route['restapi/upload_pcd/id/(\d+)/nombre/(:any)'] = "publico/subir_pcd/id/$1/nombre/$2/format/json";
$route['restapi/verificar_falla'] = "publico/verificar_falla/format/json";
$route['restapi/upload_pcd'] = "publico/subir_pcd/format/json";

$route['restapi/obtener_informados/calle/(:any)'] = "publico/obtener_informados/calle/$1/format/json";

//$route['restapi/obtener_informados/calle/([\w]+)'] = "publico/obtener_informados/calle/$1/format/json";


$route['restapi/obtener_datos_direccion/latitud/(:any)/longitud/(:any)'] = "publico/obtener_datos_direccion/latitud/$1/longitud/$2/format/json";


$route['restapi/es_calle_valida/latitud/(:any)/longitud/(:any)'] = "publico/es_calle_valida/latitud/$1/longitud/$2/format/json";

$route['restapi/prueba'] = "publico/prueba/";

$route['restapi/obtener_interseccion/latitud/(:any)/longitud/(:any)'] = "publico/obtener_interseccion/latitud/$1/longitud/$2/format/json";


$route['restapi/obtener_info_adicional'] = "publico/obtener_info_adicional/format/json";



$route['restapi/obtener_props_confirmadas'] = "publico/obtener_props_confirmadas/format/json";


$route['restapi/almacenar_alumno'] = "publico/almacenar_alumno/format/json";



#AGREGADO PARA AUTCOMPLETADO DE appCliente
$route['restapi/obtener_sugerencias_calle/calle/(:any)/cantmaxsugerencias/(:any)'] = "publico/obtener_sugerencias_calle/calle/$1/cantmaxsugerencias/$2/format/json";

//$route['restapi/obtener_datos_direccion/latitud/(\d+).(\d+)/longitud/(\d+).(\d+)'] = 
//	"publico/prueba";



// Utilizacion
//"application/helpers/generar_csv_php/generar_csv.php?idFalla="+idFalla+"&raizTmp="+json_estado.raiz_tmp
// Ruta que genera el csv con una descripcion.
// $route['generarDescripcion/(\d+)/(\s+)'] = "publico/generarDescripcion/$1/$2";





/* End of file routes.php */
/* Location: ./application/config/routes.php */

?>