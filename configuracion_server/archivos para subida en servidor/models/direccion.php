<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class Direccion
	{
		
		var $id;
		var $callePrincipal;
		var $altura;
		var $calleSecundariaA;
		var $calleSecundariaB;
		
		
		function __construct()
		{
			switch (count(func_get_args()))
			{
				case 1:
					return call_user_func_array(array($this,'constructor'), func_get_args());
					break;
				default:
					break;
			}
		}

		public function constructor($datos)
		{
			$this->altura = $datos->altura;
			$this->callePrincipal = $datos->callePrincipal;
			$this->calleSecundariaA = $datos->calleSecundariaA;
			$this->calleSecundariaB = $datos->calleSecundariaB;
		}

		private function inicializar($datos){
			$this->id = $datos->id;
			$this->altura = $datos->altura;
			$this->callePrincipal = Calle::getInstancia($datos->idCallePrincipal);
			$this->calleSecundariaA = Calle::getInstancia($datos->idCalleSecundariaA);
			$this->calleSecundariaB = Calle::getInstancia($datos->idCalleSecundariaB);
		}

		static public function getInstancia($id)
		{
			$CI = &get_instance();
			$direccion = new Direccion();
			$datos = $CI->DireccionModelo->get($id);
			$direccion->inicializar($datos);
			return $direccion;
		}

		public function save()
		{
			$CI = &get_instance();
			return $CI->DireccionModelo->save($this);
		}

		/*
		* insertarDireccion
		* Devuelve una Direccion. Si no existe se crea la Direccion.
		* @access	public
		* @param    array => array asociativo con los datos de la direccion
		*					 array('callePrincipal' =>, 'altura' =>,'calleSecundariaA' =>, 'calleSecundariaB'=>)
		*/
		static public function insertarDireccion($datosDireccion)
		{
			$CI = &get_instance();
			// Calle::buscarCalle -> Si no existe se crea la calle
			$callePrincipal = Calle::buscarCalle($datosDireccion->callePrincipal);
			$calleSecundariaA = Calle::buscarCalle($datosDireccion->calleSecundariaA);
			$calleSecundariaB = Calle::buscarCalle($datosDireccion->calleSecundariaB);
			$direccion = new Direccion();
			try {
				$buscar = new stdClass();
				$buscar->idCallePrincipal = $callePrincipal->id;
				$buscar->idCalleSecundariaA = $calleSecundariaA->id;
				$buscar->idCalleSecundariaB = $calleSecundariaB->id;
				$buscar->altura = $datosDireccion->altura;
				$datos = $CI->DireccionModelo->get_by($buscar);
				$direccion->inicializar($datos);
			} catch (MY_BdExcepcion $e) {
				$direccion->altura = $datosDireccion->altura;
				$direccion->callePrincipal = $callePrincipal;
				$direccion->calleSecundariaA = $calleSecundariaA;
				$direccion->calleSecundariaB = $calleSecundariaB;
				$direccion->id = $direccion->save();
			}finally{
				return $direccion;
			}

		}

		public function getNombre()
		{
			return $this->callePrincipal->getNombre();
		}

		public function getAltura()
		{
			return $this->altura;
		}

 

	}
 ?>