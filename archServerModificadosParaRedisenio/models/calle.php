
<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class Calle
	{
		
		var $id;
		var $nombre;
		
		
		function __construct()
		{
			
		}

		private function inicializar($datos)
		{
			$this->id = $datos->id;		
			$this->nombre = $datos->nombre;
		}

		static public function getInstancia($id)
		{

			$CI = &get_instance();
			
			$calle = new Calle();
			try {
				$datos = $CI->CalleModelo->get($id);
				$calle->inicializar($datos);		
			}	
			catch (MY_BdExcepcion $e) {
				echo 'Excepcion capturada: ',  $e->getMessage(), "\n";
			}
			return $calle;
		}

		static public function buscarCalle($nombre)
		{
			$CI = &get_instance();
			$calle = new Calle();
			try {
				$datos = $CI->CalleModelo->get_by(array('nombre' => $nombre));
				$calle->inicializar($datos);
			} catch (MY_BdExcepcion $e) {
				$calle->nombre = $nombre;
				$calle->id = $calle->save();
			}finally{
				return $calle;
			}
		}

		public function save()
		{
			$CI = &get_instance();
			return $CI->CalleModelo->save($this);
		}

		public function getNombre()
		{
			return $this->nombre;
		}

		public function esCalle($calle)
		{
			return !strcmp($this->nombre, $calle);
		}

		#AGREGADO PARA AUTOCOMPLETADO CON appCliente		
		static public function getAll()
		{
    		require_once('CustomLogger.php');
        	CustomLogger::log('EN direccion.getAll()...');
			$CI = &get_instance();
			$calles = array();
			try {
				$datos = $CI->CalleModelo->get_all();
				//NOTA: Tira "Excepcion capturada: Sin resultados" si la falla no tiene los campos obligatorios usados en los metodos de inicializacion
    			foreach ($datos as $row)
    			{
        			CustomLogger::log('Instanciando $row: ');
        			CustomLogger::log($row);
        			CustomLogger::log('------------------------ ');
    				$calle = new Calle();
    				$calle->inicializar($row);
    				array_push($calles, $calle);
    			
    			}
			}	
			catch (MY_BdExcepcion $e) {
				echo 'Excepcion capturada: ',  $e->getMessage(), "\n";
			}
			return $calles;
		}



		#AGREGADO PARA AUTOCOMPLETAR DE appCliente.
		public function concuerdaConPatron($patronCalle){
			$result = False;
			//La "i" despues del  delimitador de patron indica una busqueda sin tener
			// en cuenta las mayusculas y minusculas.
			$regexPatron = '/'.$patronCalle.'/i';
			$res  = preg_match($regexPatron, $this->nombre);
			/*log_message("debug",'resultado: '.$regexPatron. ' -- '. $this->nombre. ' --->');
			log_message("debug", $res);
			log_message("debug", ""); */
			//Se verifica que el patron concuerde y la calle no sea el nombre que se le asigna a las calles que no se pudieron calcular.
			if (preg_match($regexPatron, $this->nombre) and strcmp($this->nombre,CALLE_NO_OBTENIDA) ) {   
				$result = True;
	        }
	        return $result;
		}


		#AGREGADO PARA AUTOCOMPLETAR DE appCliente.
		#Este metodo recibe como parametro el nombre de la calle y la cantidad 
		# maxima de sugerencias que puede retornar. Luego con eso consulta la BD
		# para obtener una lista de calles que contengan la expresion del nombre de la calle y filtrarlas.
		static public function buscarSugerenciasCalles($patronCalle,$cantMaxSugerencias){
			log_message("debug","dentro de calle::buscarSugerenciasCalles");
			
			$calles = Calle::getAll();
			//$c = print_r($calles,true);
			//log_message("debug","Calles obtenidas -->");
			//log_message("debug",$c);
			
			$cantActualSugerencias = 0;
			$colSugerencias = array();
			foreach ($calles as $calle) {
				log_message("debug","llamando a concuerdaConPatron con calle: ");
				log_message("debug",$calle->nombre);
				if ($calle->concuerdaConPatron($patronCalle)) {
					if ($cantActualSugerencias < $cantMaxSugerencias ) {
						array_push($colSugerencias,$calle->nombre);
						$cantActualSugerencias = $cantActualSugerencias + 1;
					}
				}				
			}
			return $colSugerencias;
		}


	}
?>