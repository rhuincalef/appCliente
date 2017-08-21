<?php

defined('BASEPATH') OR exit('No direct script access allowed');
// Link de ejemplo completo -->
// https://code.tutsplus.com/tutorials/working-with-restful-services-in-codeigniter--net-8814
// https://www.uno-de-piera.com/crear-una-api-rest-en-codeigniter/

// Controlador para la subida de archivos de la appCliente.
require(APPPATH.'libraries/REST_Controller.php');
 
class Api_rest extends REST_Controller {
 
    function __construct()
    {
        // Construct the parent class
        parent::__construct();

        // Configure limits on our controller methods
        // Ensure you have created the 'limits' table and enabled 'limits' within application/config/rest.php
        // $this->methods['subir_pcd']['limit'] = 500; // 500 requests per hour per user/key
        // $this->methods['users_post']['limit'] = 100; // 100 requests per hour per user/key
        // $this->methods['users_delete']['limit'] = 50; // 50 requests per hour per user/key
    }



    // Este metodo se encarga de llamar a FallaMultimedia para comprobar si existe la falla, 
    // o crear una nueva entrada en la BD sino.
    // TODO: TERMINAR!!!
    public function verificar_falla_post(){
        // // Si no existe el idfalla en FallaModelo se da de alta la nueva falla
        // // Si existe, se insertan los datos en la tabla MultimediaModelo y FalllaMultimediaModelo
        // //
        // $falla = Falla::getInstancia($id);
        // if (!$falla->existe()) {
        // }else{
        //     $CI->MultimediaModelo->save($data);
        // }        
        $result =$message = [
                'id' => $this->post('id'),
                'respuesta' => 'Falla encontrada'
            ];
        $this->response($message,200); //OK (200) being the HTTP response code 
    }


    // Recibe por POST un idfalla y el nombre del archivo de captura asociadoa la misma,
    // llama a pcd_upload_model.subir_falla() para que almacene la falla
    // en el servidor y, retorna un JSON con:
    //      -el idfalla,
    //      -el nombre del archivo subido,
    //      -y un mensaje de respuesta(en caso de error).
    //
    public function subir_pcd_post()
    {
        $contenido_archivo_csv = $this->post('contenido_archivo_captura');
        log_message('debug', 'contenido_archivo_csv tiene: ');
        log_message('debug', $contenido_archivo_csv);
        log_message('debug', "tipo: ".gettype($contenido_archivo_csv));
        log_message('debug', '-------------------------------------------------');

        $this->load->model('pcd_upload_model');
        //Se envia el array asociativo de valores enviados en la peticion (guardados en $_POST)
        log_message('debug', 'Los campos enviados en $_POST desde la appCliente son ');
        log_message('debug',$this->post());
        log_message('debug', '-------------------------------------------------');

        $estadoPeticion = $this->pcd_upload_model->subir_falla($this->post());
        
        /* Se retorna una 

        */
        if ($estadoPeticion["estado"] = DIRECCION_PHP_FALLA_REGISTRADA_OK) {
            $message = [
                'id' => $this->post('id'),
                'archivo_captura' => $this->post('nombre'),
                'respuesta' => $estadoPeticion["infolog"],
                'estadoGeocoding' => $estadoPeticion["estadoGeocoding"]
            ];
            $this->response($message,PETICION_REST_OK); 
        }else{
            $message = [
                'id' => $this->post('id'),
                'archivo_captura' => '',
                'respuesta' => $estadoPeticion["infolog"],
                'estadoGeocoding' => $estadoPeticion["estadoGeocoding"]
            ];
            $this->response($message,PETICION_REST_FALLO);
        }

    }


    //Obtiene las fallas informadas y las retorna en un array asociativo
    //TODO: Modificar appCliente para que si el codigo de respuesta es 
    // 300, se muestre un mensaje que indique "No existen baches informados en el servidor".
    //
    public function obtener_informados_get(){
        
        //"calle enviada: ".$this->get('calle')
        $calle = $this->get('calle');
        $this->load->model('pcd_upload_model');
        try {
            $respuesta = $this->pcd_upload_model->obtener_informados($calle);
            echo json_encode($respuesta);
        } catch (MY_BdExcepcion $e) {
            $msg = 'Error Interno de servidor.';
            echo json_encode(array('codigo' => 400, 'mensaje' =>$msg ,'valor' =>json_encode('')));
        }
    }

    //Hace uso de la api Geocoder https://github.com/geocoder-php/Geocoder en PHP, y a partir de la latitud y la longitud retorna un dic. asociativo con la calle y altura proporcionada por Google.
    //Link de prueba Calle belgrano al 2400 -->
    // http://localhost/repoProyectoBacheo/web/restapi/obtener_datos_direccion/latitud/-43.269823/longitud/-65.287003

    //Formato de la respuesta en JSON -->
    // {
    //        "estado":0,"calle":"Belgrano","rangoEstimado1":"2300","rangoEstimado2":"2448","calleSecundariaA":"Belgrano","calleSecundariaB":"Cangallo"
    // }
    //
    public function obtener_datos_direccion_get(){
        require_once('CustomLogger.php');
        CustomLogger::log('EN obtener_datos_direccion()...');
        CustomLogger::log('Con latitud'.$this->get('latitud'));
        CustomLogger::log('Con longitud'.$this->get('longitud'));
        $respuesta = Direccion::obtener_datos_direccion_v2($this->get('latitud'),$this->get('longitud'));
        CustomLogger::log("Despues de cargar el modelo Direccion ...");
        echo json_encode($respuesta);
    }


    //Prueba con Belgrano -->
    // http://localhost/repoProyectoBacheo/web/restapi/obtener_interseccion/latitud/-43.269823/longitud/-65.287003
    //
    // Respuesta -->
    //{"estado":0,"mensaje":"OK","datos":{"calle1":"Belgrano","calle2":"E. Owen","distancia":40}}
    
    public function obtener_interseccion_get(){
        require_once('CustomLogger.php');
        CustomLogger::log('EN obtener_interseccion()...');
        $data = Direccion::obtenerIntersecCercana($this->get('latitud'),
                                            $this->get('longitud'));
        CustomLogger::log('Fin obtener_interseccion...');
        echo json_encode($data);
    }

    public function prueba_get(){
        require_once('CustomLogger.php');
        CustomLogger::log('Dentro de prueba_get()...');
        CustomLogger::log($_SERVER);
    }

    // http://localhost/repoProyectoBacheo/web/restapi/es_calle_valida/latitud/-43.2613433/longitud/-65.2985527

    public function es_calle_valida_get(){
        require_once('CustomLogger.php');
        CustomLogger::log('Dentro de es_calle_valida_get()...');
        $esValida = Direccion::estaCalleEnCiudad($this->get('latitud'),$this->get('longitud'));
        CustomLogger::log('Retorne esValida: '.$esValida);
    }

    //TODO: TERMINAR DE PROBAR ESTE METODO!!! 
    // Metodo tentativo para obtener la informacion necesaria(TipoFalla y TipoMaterial) para dar de alta una fallanueva en el sistema.
    public function obtener_info_adicional_get(){
        require_once('CustomLogger.php');
        CustomLogger::log('Dentro de obtener_tipos_falla_get()...');
        $data = TipoMaterial::getTiposMaterialYCriticidad();
        echo json_encode($data);
    }


    # URL DE PRUEBA-->
    # http://localhost/repoProyectoBacheo/web/restapi/obtener_props_confirmadas 
    public function obtener_props_confirmadas_get(){
        require_once('CustomLogger.php');
        CustomLogger::log('En de obtener_props_confirmadas()...');
        $data = TipoFalla::getTiposAsociados();
        echo json_encode($data);
    }

    public function almacenar_alumno_post(){
        require_once('CustomLogger.php');
        CustomLogger::log('En almacenarAlumno()...');
        $nombre = $this->post('nombre');
        $apellido = $this->post('apellido');
        log_message("En almacenarAlumno()");
        log_message("NOMBRE DEL ALUMNO -->");
        log_message($nombre);
        log_message("APELLIDO DEL ALUMNO -->");
        log_message($apellido);
        log_message("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
        log_message("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
        log_message("---------------------------------------------------------");
        $data= array(
                    'servidor' => "DATA OK ENVIADA",
                    'nombre' => $nombre,
                    'apellido' => $apellido);

        echo json_encode($data);
    }


    #AGREGADO PARA AUTCOMPLETADO DE appCliente
    public function obtener_sugerencias_calle_get(){
        require_once('CustomLogger.php');
        log_message('debug', 'Dentro de obtener_sugerencias_calle_get()..... ');
        $calle = $this->get('calle');
        $cantMaxSugerencias = $this->get('cantmaxsugerencias');
        $sugerencias = Calle::buscarSugerenciasCalles($calle,$cantMaxSugerencias);
        echo json_encode($sugerencias);
    }



}