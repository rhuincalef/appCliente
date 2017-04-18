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


    // Recibe por POST un idfalla y el nombre del archivo de captura asociado,
    // a la misma, llama a pcd_upload_model.subir_falla() para que almacene la falla
    // en el servidor y, retorna un JSON con el idfalla, el nombre del archivo subido,
    //  y un mensaje de respuesta(en caso de error).
    public function subir_pcd_post()
    {
        $firephp = FirePHP::getInstance(True);
        // $firephp->log("id con input: ".$this->input->post('id'));

        $contenido_archivo_csv = $this->post('contenido_archivo_captura');
        log_message('debug', 'contenido_archivo_csv tiene: ');
        log_message('debug', $contenido_archivo_csv);
        log_message('debug', "tipo: ".gettype($contenido_archivo_csv));
        log_message('debug', '-------------------------------------------------');


        $this->load->model('pcd_upload_model');
        $result = $this->pcd_upload_model->subir_falla($this->post('id'),
                                                        $this->post('nombre'),
                                                        $this->post('contenido_archivo_captura'));

        $firephp->log("Configurando respuesta en formato json...  ");
        $firephp->log("");        
        $result = TRUE;
        if ($result == TRUE) {
            $message = [
                'id' => $this->post('id'),
                'archivo_captura' => $this->post('nombre'),
                'respuesta' => 'Captura subida correctamente al servidor'
            ];
            $this->response($message,200); //OK (200) being the HTTP response code
        }else{
            $message = [
                'id' => $this->post('id'),
                'archivo_captura' => '',
                'respuesta' => 'Error de subida de archivos al servidor'
            ];
            $this->response($message,500); // 500 ERROR INTERNO DEL SERVIDOR.
        }
    }


    //Obtiene las fallas informadas y las retorna en un array asociativo
    //TODO: Modificar appCliente para que si el codigo de respuesta es 
    // 300, se muestre un mensaje que indique "No existen baches informados en el servidor".

    public function obtener_informados_get(){
        $firephp = FirePHP::getInstance(True);
        $firephp->log("En obtener_informados_get() ...");
        //$firephp->log("id enviado: ".$this->get('id'));
        $firephp->log("calle enviada: ".$this->get('calle'));
        //TODO: Mover este metodo a un rest_model.php que se encargue
        // de la logica de abajo.
        try {
            $fallas = Falla::getAll();
            $codigo = 300;
            $mensaje = "No hay elementos para mostrar";
            $data = array();
            if(count($fallas) != 0)
            {
                $codigo = 200;
                foreach ($fallas as $f) {
                    $array_falla = array();
                   $array_falla["id"] = $f->getId();
                    $array_falla["calle"] = $f->direccion->getNombre();
                    $array_falla["altura"] = $f->direccion->getAltura();
                    $data[$f->getId()] = $array_falla;
                }
            }
            $respuesta = array('codigo' => $codigo, 'datos' => $data);
            echo json_encode($respuesta);
        } catch (MY_BdExcepcion $e) {
            $msg = 'Error Interno de servidor: '.$mensaje;
            echo json_encode(array('codigo' => 400, 'mensaje' =>$msg , 'valor' =>json_encode('')));            
        }
    }

    //Hace uso de la api Geocoder https://github.com/geocoder-php/Geocoder en PHP, y a partir de la latitud y la longitud retorna un dic. asociativo con la calle y altura proporcionada por Google.
    //
    //TODO: TERMINAR DE INSTALAR Y PROBAR Geocoder.
    public function obtener_datos_direccion_get(){
        $lat = $this->get('latitud');
        $long = $this->get('longitud');

        $adapter  = new \Http\Adapter\Guzzle6\Client();
        $geocoder = new \Geocoder\Provider\GoogleMaps($adapter);
        $geocoder->reverse($lat, $long);
        $data = array(
                    'calle' =>$geocoder->getStreetName() ,
                    'altura' =>$geocoder->getStreetNumber() 
                 );
        echo json_encode($data);
    }


    //Da de alta una falla capturada en la calle por medio de appCliente
    public function crear_falla_nueva_get(){

    }


    public function prueba(){
        // require_once("FirePHP.class.php");
        $firephp = FirePHP::getInstance(True);
        $firephp->log("Se ejecuto el metodo de prueba de RESTAPI!");
        $firephp->log("En formato html!!!!");
        $firephp->log("");


    }
 
 
}