<?php
 
class Pcd_upload_model extends CI_Model
{


     public static function generarCsv($dir,$nombre_archivo,$content) {
        $data_array = explode("\n",$content);
        $csv = ""; //String de salida
        foreach ($data_array as $record){
            $csv.= $record."\n"; //Append data to csv
        }           
        $ruta = $_SERVER['DOCUMENT_ROOT']."/repoProyectoBacheo/web/".$dir."/".$nombre_archivo;
        // Se appendea la data al archivo si ya existe en el servidor.
        $csv_handler = fopen ($ruta,'a+');
        $res = fwrite ($csv_handler,$csv);
        fclose ($csv_handler);
        return $res;
    } 



    // Almacena el .csv en la carpeta de la falla,inserta la tupla en Multimedia,
    // y retorna TRUE si se pudo realizar y FALSE en caso contrario.
    
    // NOTA IMPORTANTE: La peticion se debe hacer con el siguiente JSON PARA QUE FUNCIONE:
    // { "id": 8, "nombre_captura": "<CUALQUIER NOMBRE>.csv"}


    // https://www.codeigniter.com/userguide3/libraries/file_uploading.html
    public function subir_falla($id,$nombre_archivo,$contenido_archivo_csv){
        // $firephp = FirePHP::getInstance(True);
        // $firephp->log("");
        $CI = &get_instance();
        $res = FALSE;
        log_message('debug', 'Estoy en subir_falla() ...');

        // TODO: CAMBIAR ESTA RUTA POR LA RUTA DE LA CARPETA.
        // Generar .csv en carpeta de capturas
        $PCD_UPLOAD_FOLDER = "_/dataMultimedia/".$id;
        //Se obtiene la instancia de la falla en el servidor, y se  
        // $falla = Falla::getInstancia($id);
        
        // Leer archivos enviados (desde $_FILES) por POST desde CI -->
        // https://www.codeigniter.com/userguide2/libraries/file_uploading.html
        $config['upload_path'] = $_SERVER['DOCUMENT_ROOT']."/repoProyectoBacheo/web/".$PCD_UPLOAD_FOLDER."/";
        //$config['allowed_types'] = '*';
        $config['allowed_types'] = 'text|txt|csv';
        $config['overwrite'] = FALSE;
        $config['max_size'] = '0';

        // Se inicializa la libreria upload con los valores de configuracion. 
        $this->load->library('upload',$config);
        $this->upload->initialize($config);

        log_message('debug', '$config["upload_path"] construido es ...');
        log_message('debug', $config['upload_path']);
        log_message('debug','Error asociado --> ');

        //Se recorre el array de archivos enviados en $_FILES 
        foreach($_FILES as $nombre_archivo=>$file){
            log_message('debug','$nombre_archivo -->' );
            log_message('debug',$nombre_archivo );

            if ($this->upload->do_upload($nombre_archivo) ) {
                $res = TRUE;
                log_message('debug', 'HECHO EL UPLOAD! ');
            }else{
                $res = FALSE;
                log_message('debug', 'ERROR EN UPLOAD! ');
            }
            log_message('debug', "config.file_name tiene: ");
            log_message('debug',  $this->upload->data()["file_name"]);
            log_message('debug', "config.file_type tiene: ");
            log_message('debug',  $this->upload->data()['file_type'] );
            log_message('debug', "config.file_size (Kb) tiene: ");
            log_message('debug',  $this->upload->data()['file_size'] );

            $datos_multmodelo = array(
                            'idFalla' => $id,
                            'nombreArchivo' => $nombre_archivo,
                             );
            $obj_multmodelo = new stdClass;
            $obj_multmodelo->idFalla = $datos_multmodelo["idFalla"];
            $obj_multmodelo->nombreArchivo = $datos_multmodelo["nombreArchivo"];

            $id_nuevo_mult = $CI->MultimediaModelo->save($obj_multmodelo);
            log_message('debug', 'Despues de guardar objeto MultimediaModelo ...');

            
            $datos_falla_mult = array(
                            'idFalla' => $id,
                            'idMultimedia' => $id_nuevo_mult
                            );

            $obj_fallamult = FallaMultimedia::getInstancia($datos_falla_mult);
            log_message('debug', 'Creado el objeto FallaMultimedia...');
            log_message('debug', 'Tipo de FallaMultimedia: '.gettype($obj_fallamult));

            $obj_fallamult->save();
            log_message('debug', 'Guardado el objeto FallaMultimedia...');
        }
        log_message('debug','fin for');
        
        return $res;
    }

}
?>