<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class TipoFalla
	{
		
		var $id;
		var $nombre;
		var $influencia;
		// Agregadas
		var $material;
		var $atributos;
		var $criticidades;
		var $reparaciones;
		var $multimedia;
		
		function __construct()
		{
			
		}

		
		public function getId(){
			return $this->id;
		}
		
		public function getNombre(){
			return $this->nombre;
		}

		private function inicializar($datos)
		{
			$this->id = $datos->id;
			$this->nombre = $datos->nombre;
			$this->influencia = $datos->influencia;
			$this->idMultimedia = $datos->idMultimedia;
		}


		static public function getInstancia($id)
		{
			$CI = &get_instance();
			$tipoFalla = new TipoFalla();
			$datos = $CI->TipoFallaModelo->get($id);
			$tipoFalla->inicializar($datos);
			$idMaterial = $CI->TipoFallaModelo->getMaterial($id);
			$tipoFalla->material = TipoMaterial::getInstancia($idMaterial);
			return $tipoFalla;
		}

		// Utilizarlo en caso de ser necesario ahorrar costo.
		static public function get($id)
		{
			$CI = &get_instance();
			$datos = $CI->TipoFallaModelo->get($id);
			$tipoFalla = new TipoFalla();
			$tipoFalla->inicializar($datos);
			$tipoFalla->material = $CI->TipoFallaModelo->getMaterial($id);
			return $tipoFalla;
		}

		static public function getTiposFalla()
		{
			$CI = &get_instance();
			$tiposRotura= array();
			try {
				$datos = $CI->TipoFallaModelo->getTiposFalla();
    			foreach ($datos as $row) {
    				$tipoFalla = new TipoFalla();
    				$tipoFalla->inicializar($row);
    				array_push($tiposRotura, $tipoFalla);		
    			}
			}	
			catch (MY_BdExcepcion $e) {
				echo 'Excepcion capturada: ',  $e->getMessage(), "\n";
			}
			return $tiposRotura;
		}

		public function save()
		{
			$CI = &get_instance();
			return $CI->TipoFallaModelo->save($this);
		}

		static public function crear($datos)
		{
			$CI = &get_instance();
			$CI->utiles->debugger($datos);
			$tipoFalla = new TipoFalla();
			$tipoFalla->nombre = $datos->general->nombre;
			$tipoFalla->influencia = $datos->general->influencia;
			// 
			$tipoFalla->agregarMultimedia($datos->multimedia);
			$tipoFalla->id = $tipoFalla->save();
			// 
			$CI->utiles->debugger($tipoFalla);
			if ($datos->material->id != "")
				$tipoFalla->material = TipoMaterial::getInstancia($datos->material->id);
			else
				$tipoFalla->material = TipoMaterial::crear($datos->material);
			$datos->atributos = array_map(function($atributo) use ($tipoFalla)
			{
				$atributo->falla = $tipoFalla->id;
				return $atributo;
			}, $datos->atributos);
			$CI->utiles->debugger($datos->atributos);
			$tipoFalla->atributos = $tipoFalla->cargar('TipoAtributo', $datos->atributos);
			$CI->utiles->debugger($tipoFalla->atributos);
			$tipoFalla->criticidades = $tipoFalla->cargar('Criticidad', $datos->criticidades);
			$tipoFalla->reparaciones = $tipoFalla->cargar('TipoReparacion', $datos->reparaciones);
			$tipoFalla->asociar();
			
			
			return $tipoFalla;
		}

		public function cargar($tipo, $datos)
		{
			return array_map(function($object) use ($tipo)
			{
				if (isset($object->id))
					$nuevo = call_user_func(array($tipo, 'getInstancia'), $object->id);
				else
					$nuevo = call_user_func(array($tipo, 'crear'), $object);
				return $nuevo;
			}, $datos);
		}

		public function asociar()
		{
			$CI = &get_instance();
			$CI->utiles->debugger($this);
			$idTipoFalla = $this->id;
			$this->material->asociar($idTipoFalla);
			array_map(function($criticidad) use (&$idTipoFalla)
			{
				$criticidad->asociar($idTipoFalla);
			}, $this->criticidades);
			array_map(function($tipoReparacion) use (&$idTipoFalla)
			{
				$tipoReparacion->asociar($idTipoFalla);
			}, $this->reparaciones);
		}

		public function getMaterial()
		{
			return $this->material;
		}

		public function agregarMultimedia($datos)
		{
			/* 
			Tener en cuenta....
			sudo chown -R www-data:www-data web/
			sudo chmod -R 777 web/
			sudo apt-get install php5-gd && sudo service apache2 restart

			Idea.... 
			Multimedia sabe como recortar imagen
			Configurar un directorio y jerarquia para guardar los objetos multimedia
			$multimedia = new ImagenMultimedia();
			$multimedia->falla = $tipoFalla;
			$multimedia->setNombreArchivo($tipoFalla->nombre);
			$multimedia->save();
			$this->multimedia = $multimedia;
			$this->multimedia->recortar($datos);
			$CI->utiles->debugger($multimedia);

			*/
			
			$CI = &get_instance();
			$this->multimedia = new ImagenMultimedia($datos);
			$this->multimedia->setNombreArchivo($this->nombre);
			$this->multimedia->save();
			$CI->utiles->debugger($this->multimedia);
		}

		// deprecated
		static public function datosCrearValidos($datos)
		{
			$datos_validar_tipo_falla = array(
					'general' => array('nombre' => array('string', '\w'), 'influencia' => array('integer', '\w')),
					'material' => array('nombre' => array('string', '\w')),
					'atributos' => array('nombre' => array('string', '\w'), 'unidadMedida' => array('string', '\w')),
					'criticidades' => array('nombre' => array('string', '\w'), 'descripcion' => array('string', '\w'), 'ponderacion' => array('integer', '\w')),
					'reparaciones' => array('nombre' => array('string', '\w'), 'costo' => array('double', '\w'), 'descripcion' => array('string', '\w')),
					// 'multimedia' => array('coordenadas', 'imagen')
					);
			$CI = &get_instance();
			foreach ($datos_validar_tipo_falla as $clave => $valor)
			{
				if (!is_array($datos->$clave)) {
					foreach ($valor as $key => $value) {
						if (!property_exists($datos->$clave, $key) || !isset($datos->$clave->$key))
						{
							return FALSE;
						}
					}
				}else{
					foreach($datos->$clave as $c => $v)
					{
						foreach ($valor as $key => $value)
						{
							if (!property_exists($v, $key) || !isset($v->$key))
							{
								return FALSE;
							}
						}
					}
				}
			}
			return TRUE;
		}

		static public function validarDatos($datos)
		{
			$CI = &get_instance();
			$CI->utiles->debugger("validarDatos");
			// Creando arbol para TipoFalla
			$terminal1 = new StringTerminalExpression("nombre", "", "true");
			// $terminal2 = new NumericTerminalExpression("influencia", "integer", "true");
			// TODO: hablar sobre como tratar esto?????
			$terminal2 = new NumericTerminalExpression("influencia", "int", "true");
			$noTerminal1 = new AndExpression(array($terminal1, $terminal2), "general");

			$terminal1 = new StringTerminalExpression("nombre", "", "true");
			$noTerminal2 = new AndExpression(array($terminal1), "material");

			$terminal1 = new StringTerminalExpression("nombre", "", "true");
			$terminal2 = new StringTerminalExpression("unidadMedida", "", "true");
			$noTerminal3 = new AndExpression(array($terminal1, $terminal2), "atributos");

			$terminal1 = new StringTerminalExpression("nombre", "", "true");
			$terminal2 = new NumericTerminalExpression("ponderacion", "double", "true");
			$terminal3 = new StringTerminalExpression("descripcion", "", "true");
			$noTerminal4 = new AndExpression(array($terminal1, $terminal2, $terminal3), "criticidades");

			$terminal1 = new StringTerminalExpression("nombre", "", "true");
			$terminal2 = new NumericTerminalExpression("costo", "double", "true");
			$terminal3 = new StringTerminalExpression("descripcion", "", "true");
			$noTerminal5 = new AndExpression(array($terminal1, $terminal2, $terminal3), "reparaciones");

			$terminal1 = new NumericTerminalExpression("x", "double", "true");
			$terminal2 = new NumericTerminalExpression("y", "double", "true");
			$terminal3 = new NumericTerminalExpression("ancho", "double", "true");
			$terminal4 = new NumericTerminalExpression("alto", "double", "true");
			$noTerminal6 = new AndExpression(array($terminal1, $terminal2, $terminal3, $terminal4), "coordenadas");
			$terminal1 = new StringTerminalExpression("imagen", "", "true");
			$noTerminal7 = new AndExpression(array($terminal1, $noTerminal6), "multimedia");
			
			$validator = new AndExpression(array($noTerminal1, $noTerminal2, $noTerminal3, $noTerminal4, $noTerminal5, $noTerminal7), "datos");
			return $validator->interpret($datos);
		}

		static public function getTiposFallaPorMaterial($idMaterial)
		{
			$CI = &get_instance();
			$arrayTiposFallaId =  $CI->TipoFallaModelo->getTiposFallaMaterial($idMaterial);
			$arrayTiposFalla = array();
			foreach ($arrayTiposFallaId as $key => $value) {
				$falla = self::get($value->idTipoFalla);
				$falla->reparaciones = TipoReparacion::getReparacionesPorTipoFalla($falla->id);
				array_push($arrayTiposFalla, $falla);
			}
			return $arrayTiposFalla;
		}

		// Utilizarlo para la vista de crear Falla.
		static public function gety($id)
		{
			$CI = &get_instance();
			$tipoFalla = self::get($id);
			$tipoFalla->reparaciones = TipoReparacion::getReparacionesPorTipoFalla($tipoFalla->id);
			// TipoAtributo::getAtributosPorTipoFalla
			$tipoFalla->atributos = TipoAtributo::getAtributosPorTipoFalla($tipoFalla->id);
			// TipoCriticidad::getCriticidadesPorTipoFalla
			$tipoFalla->criticidades = Criticidad::getCriticidadesPorTipoFalla($tipoFalla->id);
			// $CI->utiles->debugger($tipoFalla->criticidades);
			return $tipoFalla;
		}

		//AGREGADO RODRIGO
		public static function getTipoFallaPorNombre($nombre){
			$CI = &get_instance();
			$datos = $CI->TipoFallaModelo->get_by(array('nombre' => $nombre));
			$tipoFalla = new TipoFalla();
			$tipoFalla->inicializar($datos);
			return $tipoFalla;
		}


		//Retorna el tipo de reparacion y el tipo de material
		//asociado con un tipo de falla.
		// FORMATO DEL JSON RETORNADO -->
#listadoTiposFalla = [
# 	{
# 	"clave": "tipoFalla",
# 	"valor": "Bache",
# 	"colPropsAsociadas": [
#			 		{"clave": "tipoReparacion", "valor":"Sellado"},
#			 		{"clave": "tipoReparacion", "valor":"Cementado"},
#			 		{"clave": "tipoMaterial", "valor":"Pavimento asfaltico"]},
#			 		{"clave": "tipoMaterial", "valor":"Cemento"},
#			 		...
#					]
#	},
# 	...	
#]
		//NOTA IMPORTANTE: Antes de emplear esta funcionalidad, agregar informacion en la tabla de la BD "TipoFallaCriticidadModelo", relacionando un grupo de criticidades para cada tipo de falla. Idem con "TipoMaterialTipoFallaModelo".
		// 
		public static function getTiposAsociados(){
			require_once('CustomLogger.php');
        	//CustomLogger::log('Obtenidos todos los tipos de fallas...');
        	//CustomLogger::log($tiposFalla);
			$data = array();
			$tiposFalla = TipoFalla::getTiposFalla();
			log_message('debug','Obtenidos todos los tipos de fallas...');
        	try {
				foreach ($tiposFalla as $tFalla) {
						log_message('debug','Iterando el tipoFalla con id: ');
						log_message('debug',$tFalla->id);
						log_message('debug','dsakdmksamdkasmdk');
						//Este array es donde se acumulan las propiedades para un tipo de falla						
						$propsTipoFalla = array();
						
						//Se obtienen los tipos de criticidad segun el id del tipo de falla 
						$criticidadesAsociadas =TipoFallaCriticidad::obtenerCriticidadesAsociadas($tFalla->id);
						log_message('debug','Leidas las criticidades para la falla: ');
						log_message('debug',$tFalla->id);
						TipoFalla::asociarPropiedades($propsTipoFalla,$criticidadesAsociadas,'criticidad');

						//Se obtienen los tipos de material segun el id del tipo de falla 
						$materialesAsociados =TipoMaterialTipoFalla::obtenerMaterialesAsociados($tFalla->id);
						log_message('debug','Leidos los materiales para la falla: ');
						log_message('debug',$tFalla->id);
						TipoFalla::asociarPropiedades($propsTipoFalla,$materialesAsociados,'tipoMaterial');

						$tipoFallaActual = array(
										'id' => $tFalla->id,
										'clave' => "tipoFalla",
										'valor' => $tFalla->nombre,
										'colPropsAsociadas' => $propsTipoFalla,
									 );
						array_push($data,$tipoFallaActual);
	        			
				} //Fin foreach
			} catch (MY_BdExcepcion $e) {
				CustomLogger::log('Error MY_BdExcepcion ocurrida: ');
				CustomLogger::log($e);						
			}finally {
				return $data;
			}
		}

		# Genera en el formato requerido las propiedades que se encuentran asociadas a  la falla.
		public static function asociarPropiedades(&$data,$arreglo,$nombreClave){
			log_message('debug','En asociarPropiedades()');
			foreach ($arreglo as $elem) {
				log_message('debug','Iterando elemento: ');
				$aux = print_r($elem,true);
				log_message('debug',$aux);
				log_message('debug','------------------------------ ');

				$valorProp = $elem->nombre;
				if (isset($elem->descripcion)) {
					$valorProp = $valorProp. ': '.$elem->descripcion;
				}
				log_message('debug','valorProp final tiene: ');
				log_message('debug',$valorProp);

				$ponderacion = array();
				if (isset($elem->ponderacion)) {
					$pond = array(
									'clave' => 'ponderacion',
									'valor' => $elem->ponderacion
									 );
					array_push($ponderacion, $pond);
				}

				$a = array(
							'id' => $elem->id,
							'clave' => $nombreClave,
							'valor' => $valorProp,
							'colPropsAsociadas' => $ponderacion 
					 ); 
				array_push($data, $a);
			}
			log_message('debug','data tiene:');
			$aux1 = print_r($data,true);
			log_message('debug',$aux1);
			log_message('debug','Fin de asociarPropiedades');
		}


		


//BACKUP! VERSION ANTERIOR!
/*
		public static function getTiposAsociados(){
			require_once('CustomLogger.php');
			$data = array();
			$tiposFalla = TipoFalla::getTiposFalla();
        	CustomLogger::log('Obtenidos todos los tipos de fallas...');
        	CustomLogger::log($tiposFalla);
        	try {
				foreach ($tiposFalla as $tFalla) {
						CustomLogger::log('Iterando el tipoFalla con id: ');
	        			CustomLogger::log($tFalla->id);
						$propsTipoFalla = array();
						 
						$getIdsReparacion = array(
												'clase' =>'TipoFallaTipoReparacion' ,
												'metodo' => 'getIdsReparacion' ,
												'nombreId' => 'idTipoReparacion',
												'args' => array($tFalla->id)
												 );


						$getInstanciaReparacion = array(
												'clase' =>'TipoReparacion' ,
												'metodo' => 'getTipoDeReparacion'
												 );
						
						$tiposReparacionAsociados = TipoFalla::getObjectArrayById($getIdsReparacion,$getInstanciaReparacion);

						TipoFalla::asociarPropiedades($propsTipoFalla,$tiposReparacionAsociados,'tipoReparacion');

						CustomLogger::log('tiposReparacionAsociados es: ');
						CustomLogger::log($propsTipoFalla);
						CustomLogger::log('++++++++++++++++++++++++++++++++');

						

						CustomLogger::log('propsTipoFalla despues de obtener datos tipoReparacion es: ');
						CustomLogger::log($propsTipoFalla);

						$getIdsTipoMaterial = array(
												'clase' =>'TipoMaterialTipoFalla' ,
												'metodo' => 'getIdsMaterial' ,
												'nombreId' => 'idTipoMaterial',
												'args' => array($tFalla->id)
												 );


						$getInstanciaMaterial = array(
												'clase' =>'TipoMaterial' ,
												'metodo' => 'getTipoMaterial'
												 );

						
						$tipoMaterialAsociados = TipoFalla::getObjectArrayById($getIdsTipoMaterial,$getInstanciaMaterial);

						TipoFalla::asociarPropiedades($propsTipoFalla,$tipoMaterialAsociados,'tipoMaterial');

						$elem1 = array(
									'clave' => 'tipoFalla',
									'valor' => $tFalla->nombre,
									'colPropsAsociadas' => $propsTipoFalla
							 );
						array_push($data,$elem1);
	        		
				} //Fin foreach
			} catch (MY_BdExcepcion $e) {
				CustomLogger::log('Error MY_BdExcepcion ocurrida: ');
				CustomLogger::log($e);						
			}finally {
				return $data;
			}
		}

		public static function asociarPropiedades(&$data,$arreglo,$nombreClave){
			CustomLogger::log('En asociarPropiedades()');
			CustomLogger::log('arreglo tiene:');
			CustomLogger::log($arreglo);

			foreach ($arreglo as $elem) {
				CustomLogger::log('Iterando elemento: ');
				CustomLogger::log($elem);
				CustomLogger::log('------------------------------ ');
				$a = array(
							'clave' => $nombreClave,
							'valor' => $elem->nombre
					 ); 
				array_push($data, $a);
			}
			CustomLogger::log('data tiene:');
			CustomLogger::log($data);
			CustomLogger::log('Fin de asociarPropiedades');
		}


		//Obtiene un array de objetos dada una funcion enviada por parametro
		public static function getObjectArrayById($getIds,$getInstancia){
			CustomLogger::log('En getObjectArrayById()....');
			
			$objs = array();
			if (is_callable($getIds["clase"], $getIds["metodo"])) {
		        $objs = call_user_func_array(array($getIds["clase"], $getIds["metodo"]), $getIds["args"]);
		        
				CustomLogger::log('los objs leidos son');
				CustomLogger::log($objs);
				CustomLogger::log('.......................');
				CustomLogger::log($objs[1]->{$getIds["nombreId"]});
				CustomLogger::log('----------------------------');
		    }else {
		        throw new Exception('Error en tipoFalla.getIdsArray - ' . $getIds["clase"] . '::' . $getIds["metodo"]);
		    }

			$tiposAsociados = array();		    
			foreach ($objs as $obj) {
				CustomLogger::log('Dentro del foreach ids ...');
				if (is_callable($getInstancia["clase"], $getInstancia["metodo"])) {
		        	$tipoObjeto = call_user_func_array(
		        								array($getInstancia["clase"], $getInstancia["metodo"]),
		        										array(
		        											$obj->{$getIds["nombreId"]}
		        											)

		        									);

		        	CustomLogger::log('Instanciado objeto: ');
		        	CustomLogger::log($tipoObjeto);
					array_push($tiposAsociados, $tipoObjeto);
				}else {
		        throw new Exception('Error en tipoFalla.getIdsArray - ' . $getInstancia["clase"] . '::' . $getInstancia["metodo"]);
		    	}
			} //Fin de foreach 
			CustomLogger::log('Fin de getObjectArrayById()....');
			return $tiposAsociados;
		}
*/		


	}
 ?>