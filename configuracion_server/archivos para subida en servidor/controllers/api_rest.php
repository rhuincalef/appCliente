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


    // BACKUP DEL GET RESTFUL!
    // public function subir_pcd_get()
    //     {
    //         $firephp = FirePHP::getInstance(True);
    //         $firephp->log("En subir_pcd()  ");
    //         $firephp->log("id con input: ".$this->input->get('id'));
    //         $firephp->log("nombre con input: ".$this->input->get('nombre'));
    //         $firephp->log("archivo_captura_1 con input: ".$this->input->get('archivo_captura_1'));
            
    //         // Se carga el modelo de subida de archivos.
    //         $this->load->model('pcd_upload_model');
    //         $result = $this->pcd_upload_model->subir_falla($this->post('id'),
    //                                                         $this->post('nombre'),
    //                                                         $this->post('archivo_captura_1') );
    //         $firephp->log("Configurando respuesta en formato json...  ");
    //         $firephp->log("");

    //         $this->load->library("input");
            
    //         $result = FALSE;
    //         if ($result == FALSE) {
    //             $message = [
    //                 'id' => $this->input->get('id'),
    //                 'nombre' => $this->input->get('nombre'),
    //                 'archivo_captura_1' => $this->input->get('archivo_captura_1'),
    //                 'respuesta' => 'Subida captura correctamente al servidor'
    //             ];
    //             $firephp->log($message);
    //             $this->response($message,200); //OK (200) being the HTTP response code
    //         }else{
    //             $message = [
    //                 'respuesta' => 'Error de subida de archivos al servidor'
    //             ];
    //             $firephp->log($message);
    //             $this->response($message,500); // 500 ERROR INTERNO DEL SERVIDOR.
    //         }
    //     }


    public function prueba(){
        // require_once("FirePHP.class.php");
        $firephp = FirePHP::getInstance(True);
        $firephp->log("Se ejecuto el metodo de prueba de RESTAPI!");
        $firephp->log("En formato html!!!!");
        $firephp->log("");


    }
 
 
}