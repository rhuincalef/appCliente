<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class Criticidad
	{
		
		var $id;
		var $nombre;
		var $descripcion;
		var $ponderacion;
		
		function __construct()
		{
			switch (func_get_args()) {
				case 3:
					return call_user_func_array(array($this,'constructor'), func_get_args());
					break;
				default:
					break;
			}
		}

		public function constructor($args)
		{
			$this->nombre = $args[0];
			$this->descripcion = $args[1];
			$this->ponderacion = $args[2];

		}

		private function inicializar($datos)
		{
			$this->id = $datos->id;		
			$this->nombre = $datos->nombre;
			$this->descripcion = $datos->descripcion;
			$this->ponderacion = $datos->ponderacion;
		}

		static public function getInstancia($id)
		{

			$CI = &get_instance();
			$criticidad = new Criticidad();
			$datos = $CI->CriticidadModelo->get($id);
			$criticidad->inicializar($datos);		
			return $criticidad;

		}

		// static public function getCriticidades()
		static public function getAll()
		{
			$CI = &get_instance();
			$criticidades = array();
			try {
				// $datos = $CI->CriticidadModelo->getCriticidades();
				$datos = $CI->CriticidadModelo->get_all();
    			foreach ($datos as $row)
    			{
    				$criticidad = new Criticidad();
    				$criticidad->inicializar($row);
    				array_push($criticidades, $criticidad);		
    			}
			}	
			catch (MY_BdExcepcion $e) {
				echo 'Excepcion capturada: ',  $e->getMessage(), "\n";
			}
			return $criticidades;
		}
		
		public function toJson() {
    		return ['id'=> $this->id,'nombre' => $this->nombre,'descripcion' => $this->descripcion];
		}

		static public function getCriticidadPorNombre($nombre)
		{
			$CI = &get_instance();
			// $datos = $CI->CriticidadModelo->getCriticidadPorNombre($nombre);
			$datos = $CI->CriticidadModelo->get_by(array('nombre' => $nombre));
			$criticidad = new Criticidad();
			$criticidad->inicializar($datos);
			return $criticidad;
		}

		public function save()
		{
			$CI = &get_instance();
			return $CI->CriticidadModelo->save($this);
		}

		static public function crear($datos)
		{
			$CI = &get_instance();
			$CI->utiles->debugger($datos);
			$criticidad = new Criticidad();
			$criticidad->nombre = $datos->nombre;
			$criticidad->descripcion = $datos->descripcion;
			$criticidad->ponderacion = $datos->ponderacion;
			$criticidad->id = $criticidad->save();
			$CI->utiles->debugger($criticidad);
			return $criticidad;
		}

		public function asociar($idTipoFalla)
		{
			$CI = &get_instance();
			$CI->CriticidadModelo->asociar($this->id, $idTipoFalla);
		}

		static public function getCriticidadesPorTipoFalla($idTipoFalla)
		{
			$CI = &get_instance();
			$arrayCriticidadesId = $CI->CriticidadModelo->getCriticidadesPorTipoFalla($idTipoFalla);
			$arrayCriticidades = array();
			foreach ($arrayCriticidadesId as $key => $value) {
				array_push($arrayCriticidades, $value->idCriticidad);
			}
			return $arrayCriticidades;
		}
	}
 ?>