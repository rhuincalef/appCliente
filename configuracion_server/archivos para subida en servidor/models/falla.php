<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class Falla implements JsonSerializable
	// class Falla
	{
		var $id;
		var $latitud;
		var $longitud;
		var $criticidad;
		var $direccion;
		var $tipoMaterial;
		var $tipoFalla;
		var $tipoReparacion;
		var $influencia;
		var $factorArea;
		// var $estados;
		
		function __construct()
		{
			
		}

		private function inicializar($datos)
		{
			$CI = &get_instance();
			// $CI->utiles->debugger($datos);
			$this->id = $datos->id;
			$this->latitud = $datos->latitud;
			$this->longitud = $datos->longitud;
			$this->direccion = Direccion::getInstancia($datos->idDireccion);
			$this->tipoMaterial = tipoMaterial::getInstancia($datos->idTipoMaterial);
			$this->tipoFalla = TipoFalla::getInstancia($datos->idTipoFalla);
			$this->estado = Estado::getEstadoActual($this->id);
			// El estado de la conoce los demás atributos que se deben inicializar 
			$this->estado->inicializarFalla($this, $datos);
			$this->estado->falla = $this;
			// $this->estado->falla = $this;
			// $CI->utiles->debugger($this);
		}



		public function getId(){
			return $this->id;
		}
		
		static public function getInstancia($id)
		{
			$CI = &get_instance();
			$falla = new Falla();
			$datos = $CI->FallaModelo->get($id);
			$falla->inicializar($datos);
			return $falla;
		}

		public function save()
		{
			$CI = &get_instance();
			return $CI->FallaModelo->save($this);
		}

		/*
		- Petición para crear una nueva falla en el estado Confirmado.
		$.post('crear/Falla', 
		{"clase": "Falla",
		"datos": JSON.stringify(
		  { "falla": {"latitud": -43.251741078254454, "longitud": -65.32084465026855, "influencia":2, "factorArea": .2},
		   "observacion": {"comentario": "comentario falla", "nombreObservador": "Pepe", "emailObservador": "pepe@pepe.com"},
		   "tipoFalla": {"id": 5},
		   "criticidad": {"id": 9},
       	   "reparacion": {"id": 6},
           "atributos": [{"id": 9, "valor": parseFloat('5')},{"id": 10,"valor": parseFloat('4')}],
		   "direccion": {"altura": 50,"callePrincipal": "Edison Norte", "calleSecundariaA": "calleSA", "calleSecundariaB": "calleSB"}
		  })
		})
		- Petición para crear definitivamente la falla, pasa del estado Informado al Confirmado.
		$.post('crear/Falla', 
		{"clase": "Falla",
		"datos": JSON.stringify(
		  { "falla": {"id": 20, "latitud": -43.251741078254454, "longitud": -65.32084465026855, "influencia":2, "factorArea": .2},
		   "observacion": {"comentario": "comentario falla", "nombreObservador": "Pepe", "emailObservador": "pepe@pepe.com"},
		   "tipoFalla": {"id": 1},
		   "criticidad": {"id": 2},
       	   "reparacion": {"id": 1},
       	   "atributos": [{"id": 1, "valor": 5},{"id": 2,"valor": 4}, {"id":3, "valor":'3'}],
		   "direccion": {"altura": 50,"callePrincipal": "Edison Norte", "calleSecundariaA": "calleSA", "calleSecundariaB": "calleSB"}
		  })
		})
		*/
		static public function crear($datos)
		{
			$CI = &get_instance();
			/*
			Si la falla viene con id debe pasar del estado Informado a Confirmado.
			Sino se debe crear la falla directamente en el estado Confirmado.
			*/
			if (!property_exists($datos->falla, 'id'))
			{
				return self::crearFallaEnConfirmado($datos);
			}
			return self::crearFalla($datos);
		}

		public function insertarDireccion($datosDireccion)
		{
			// Direccion::insertarDireccion -> Si no existe se crea la calle
			return Direccion::insertarDireccion($datosDireccion);
		}

		static public function validarDatos($datos)
		{
			$valor = $datos->clase;
			$CI = &get_instance();
			switch ($valor) {
				case 'Falla':
					return self::validarDatosFalla($datos);
					// break;
				case 'FallaAnonima':
					return self::validarDatosFallaAnonima($datos);
					// break;
				default:
					return false;
					// break;
			}
		}
/*
		static public function validarDatosFalla($datos)
		{
			return true;
		}
*/
		/*
		{ "falla": {"latitud": -43.251741078254454, "longitud": -65.32084465026855, "influencia":2, "factorArea": .2},
		"observacion": {"comentario": "comentario falla"},
		"tipoFalla": {"id": 5},
		"criticidad": {"id": 9},
		   "reparacion": {"id": 6},
		"atributos": [{"id": 9, "valor": '5'},{"id": 10,"valor": '4'}],
		"direccion": {"altura": 50,"callePrincipal": "Edison Norte", "calleSecundariaA": "calleSA", "calleSecundariaB": "calleSB"}
		}
		*/

		static public function validarDatosFalla($datos)
		{
			$CI = &get_instance();
			$CI->utiles->debugger("validarDatosFalla");
			// Creando arbol para validar los datos de Falla
			$terminal1 = new NumericTerminalExpression("latitud", 'double', true);
			$terminal2 = new NumericTerminalExpression("longitud", 'double', true);
			$terminal3 = new NumericTerminalExpression("factorArea", 'double', true);
			$terminal4 = new NumericTerminalExpression("id", 'int', false);
			$noTerminalFalla = new AndExpression(array($terminal1, $terminal2, $terminal3, $terminal4), "falla");

			$terminal1 = new StringTerminalExpression("comentario", "", true);
			$noTerminalObservacion = new AndExpression(array($terminal1), "observacion");

			$terminal1 = new NumericTerminalExpression("id", 'int', true);
			$noTerminaTipoFalla = new AndExpression(array($terminal1), "tipoFalla");

			$terminal1 = new NumericTerminalExpression("id", 'int', true);
			$noTerminalCriticidad = new AndExpression(array($terminal1), "criticidad");

			$terminal1 = new NumericTerminalExpression("id", 'int', true);
			$noTerminalReparacion = new AndExpression(array($terminal1), "reparacion");

			$terminal1 = new NumericTerminalExpression("id", 'int', true);
			$terminal2 = new NumericTerminalExpression("valor", 'double', true);
			$noTerminalAtributo = new AndExpression(array($terminal1, $terminal2), "atributos");

			$terminal1 = new NumericTerminalExpression("altura", 'int', true);
			$terminal2 = new StringTerminalExpression("callePrincipal", "", true);
			$terminal3 = new StringTerminalExpression("calleSecundariaA", "", true);
			$terminal4 = new StringTerminalExpression("calleSecundariaB", "", true);
			$noTerminalDireccion = new AndExpression(array($terminal1, $terminal2, $terminal3, $terminal4), "direccion");
/*
			$validator = new AndExpression(array($noTerminalFalla, $noTerminalObservacion, $noTerminalDireccion, $noTerminaTipolFalla, $noTerminaCriticidad, $noTerminalAtributo), "datos");
*/
			$validator = new AndExpression(array($noTerminalFalla, $noTerminalObservacion, $noTerminaTipoFalla, $noTerminalCriticidad, $noTerminalDireccion, $noTerminalReparacion, $noTerminalAtributo), "datos");
			return $validator->interpret($datos);
		}

		static public function validarDatosFallaAnonima($datos)
		{
			$CI = &get_instance();
			$CI->utiles->debugger("validarDatosFallaAnonima");
			// Creando arbol para validar los datos de FallaAnonima
			$terminal1 = new NumericTerminalExpression("latitud", "double", "true");
			$terminal2 = new NumericTerminalExpression("longitud", "double", "true");
			$noTerminalFalla = new AndExpression(array($terminal1, $terminal2), "falla");

			$terminal1 = new StringTerminalExpression("comentario", "", "true");
			$terminal2 = new StringTerminalExpression("nombreObservador", "", "true");
			$terminal3 = new StringTerminalExpression("emailObservador", "", "true");
			$noTerminalObservacion = new AndExpression(array($terminal1, $terminal2, $terminal3), "observacion");

			$terminal1 = new NumericTerminalExpression("id", "int", "true");
			$noTerminaTipolFalla = new AndExpression(array($terminal1), "tipoFalla");

			$terminal1 = new NumericTerminalExpression("altura", "int", "true");
			$terminal2 = new StringTerminalExpression("callePrincipal", "", "true");
			$terminal3 = new StringTerminalExpression("calleSecundariaA", "", "true");
			$terminal4 = new StringTerminalExpression("calleSecundariaB", "", "true");
			$noTerminalDireccion = new AndExpression(array($terminal1, $terminal2, $terminal3, $terminal4), "direccion");

			$validator = new AndExpression(array($noTerminalFalla, $noTerminalObservacion, $noTerminalDireccion, $noTerminaTipolFalla), "datos");
			return $validator->interpret($datos);
		}

		public function obtenerImagenes()
		{
			/*$imagenes = Multimedia::getAll($this->id);
			return $imagenes;*/
		}

		// Metodo llamado por el formulario de twitter para obtener los comentarios de un bache.
		public function obtenerObservacionesTw($hashtag)
		{
			# code...
		}

		/*
		No se tienen en cuenta
			$falla->influencia = $datos->falla->influencia;
			$falla->factorArea = $datos->falla->factorArea;
		No se carga el tipo de reparacion ni la criticidad
		Se crea en el estado Informado
		saveAnonimo()
		asociar FallaEstadoModelo
		*/
		static public function crearFallaAnonima($datos)
		{
			$CI = &get_instance();
			$CI->utiles->debugger("crearFallaAnonima");
			
			$falla = new Falla();
			$falla->latitud = $datos->falla->latitud;
			$falla->longitud = $datos->falla->longitud;
			// TipoFalla viene con id. getInstancia
			$falla->tipoFalla = TipoFalla::getInstancia($datos->tipoFalla->id);
			// TipoMaterial se obtiene a traves del Tipo de Falla
			$falla->tipoMaterial = $falla->tipoFalla->getMaterial();
			$falla->direccion = $falla->insertarDireccion($datos->direccion);
			// A partir de aca cambia
			$falla->id = $falla->saveAnonimo();
			$observacion = new Observacion($datos->observacion, date("Y-m-d H:i:s"));
			$observacion->falla = $falla;
			$observacion->save();
			$falla->estado = new Informado();
			$falla->estado->falla = $falla;
			$falla->estado->id = $falla->estado->save();
			$falla->asociarEstado();
			// TODO: Falta asociar la observacion
			// TODO: realizar los save's dependientes en save Falla
			$CI->utiles->debugger($falla);
			return $falla;
		}

		public function saveAnonimo()
		{
			$CI = &get_instance();
			return $CI->FallaModelo->saveAnonimo($this);
		}

		public function asociarEstado()
		{
			$CI = &get_instance();
			return $CI->FallaModelo->asociarEstado($this);
		}

		/*
		Falla no informada
		Se crea en el estado Confirmado
		save()
		asociar FallaEstadoModelo
		*/
		static public function crearFallaEnConfirmado($datos)
		{
			$CI = &get_instance();
			$falla = new Falla();
			$falla->latitud = $datos->falla->latitud;
			$falla->longitud = $datos->falla->longitud;
			// la influencia se obtiene a través del tipo de falla
			// $falla->influencia = $datos->falla->influencia;
			$falla->factorArea = $datos->falla->factorArea;
			// TipoFalla viene con id. getInstancia
			$falla->tipoFalla = TipoFalla::getInstancia($datos->tipoFalla->id);
			$falla->influencia = $falla->tipoFalla->influencia;
			// TipoMaterial se obtiene a traves del Tipo de Falla
			$falla->tipoMaterial = $falla->tipoFalla->getMaterial();
			// TipoReparacion se obtiene a traves del Tipo de Falla
			// Se establece más tarde en el próximo estado
			$falla->direccion = $falla->insertarDireccion($datos->direccion);
			// $falla->criticidad = Criticidad::getInstancia($datos->criticidad->id);
			$falla->tipoReparacion = TipoReparacion::getInstancia($datos->reparacion->id);
			$falla->criticidad = Criticidad::getInstancia($datos->criticidad->id);
			$falla->observaciones = array();
			// TODO: Ver donde acomodarlo mejor
			$user = $CI->ion_auth->user()->row();
			$datos->observacion->nombreObservador = $user->username;
			$datos->observacion->emailObservador = $user->email;
			// 
			$observacion = new Observacion($datos->observacion, date("Y-m-d H:i:s"));
			array_push($falla->observaciones, $observacion);
			$falla->direccion = $falla->insertarDireccion($datos->direccion);
			$falla->id = $falla->save();
			$observacion->falla = $falla;
			$observacion->save();
			// TipoAtributo
			$falla->atributos = array_map(function ($atributo)
			{
				$tipoAtributo = TipoAtributo::getInstancia($atributo->id);
				$tipoAtributo->valor = $atributo->valor;
				return $tipoAtributo;
			}, $datos->atributos);
			// Por cada tipo de atributo se establece una entrada en la tabla FallaTipoAtributoModelo
			$falla->asociarAtributos();
			// 
			$falla->estado = new Confirmado();
			$falla->estado->setUsuario();
			$falla->estado->falla = $falla;
			$falla->estado->id = $falla->estado->save();
			$falla->asociarEstado();
			$CI->utiles->debugger($falla);
			return $falla;
		}

		/*
		Falla en estado Informado
		Se realiza el cambio de estado de Informado->Confirmado
		*/
		static public function crearFalla($datos)
		{
			$CI = &get_instance();
			$falla = self::getInstancia($datos->falla->id);
			// $falla->influencia = $datos->falla->influencia;
			$falla->factorArea = $datos->falla->factorArea;
			// TipoFalla viene con id. getInstancia
			$falla->tipoFalla = TipoFalla::getInstancia($datos->tipoFalla->id);
			$falla->influencia = $falla->tipoFalla->influencia;
			// TipoMaterial se obtiene a traves del Tipo de Falla
			$falla->tipoMaterial = $falla->tipoFalla->getMaterial();
			// TipoReparacion se obtiene a traves del Tipo de Falla
			$falla->tipoReparacion = TipoReparacion::getInstancia($datos->reparacion->id);
			$falla->criticidad = Criticidad::getInstancia($datos->criticidad->id);
			// Observacion
			$falla->observaciones = array();
			// TODO: Ver donde acomodarlo mejor
			$user = $CI->ion_auth->user()->row();
			$datos->observacion->nombreObservador = $user->username;
			$datos->observacion->emailObservador = $user->email;
			// 
			$observacion = new Observacion($datos->observacion, date("Y-m-d H:i:s"));
			$observacion->falla = $falla;
			$observacion->save();
			array_push($falla->observaciones, $observacion);
			// TipoAtributo
			$falla->atributos = array_map(function ($atributo)
			{
				$tipoAtributo = TipoAtributo::getInstancia($atributo->id);
				$tipoAtributo->valor = $atributo->valor;
				return $tipoAtributo;
			}, $datos->atributos);
			// Por cada tipo de atributo se establece una entrada en la tabla FallaTipoAtributoModelo
			$falla->asociarAtributos();
			// 
			$usuario = new stdClass();
			$usuario->id = $user->id;
			$usuario->nombre = $user->username;
			$usuario->email = $user->email;

			$falla->estado = Estado::getEstadoActual($falla->id);
			$falla->estado = $falla->estado->cambiar($falla, $datos, $usuario);
			$falla->actualizar();
			$falla->asociarEstado();
			$CI->utiles->debugger($falla);
			return $falla;
		}

		public function actualizar()
		{
			$CI = &get_instance();
			return $CI->FallaModelo->actualizar($this);
		}

		static public function getAll()
		{
			$CI = &get_instance();
			$fallas = array();
			try {
				$datos = $CI->FallaModelo->get_all();
    			foreach ($datos as $row)
    			{
    				$falla = new Falla();
    				$falla->inicializar($row);
    				array_push($fallas, $falla);
    			}
			}	
			catch (MY_BdExcepcion $e) {
				echo 'Excepcion capturada: ',  $e->getMessage(), "\n";
			}
			return $fallas;
		}

		public function asociarAtributos()
		{
			$CI = &get_instance();
			return $CI->FallaModelo->asociarAtributos($this);
		}

		public function to_array()
		{
			$datos = $this->estado->to_array($this);
			return $datos;
		}

		static public function obtenerObservaciones($idBache)
		{
			$observaciones = Observacion::getAll($idBache);
			// Por cada observacion se arma un array fijado para no romper la view.
			return array_map(function($elemento)
			{
	            return array(
	                'fecha' => $elemento->fecha,
	                'texto' => $elemento->comentario,
	                'usuario' => $elemento->nombreObservador
	            );
        	}, $observaciones);
		}

		public function asociarObservacionAnonima($datos)
		{
			$observacion = new Observacion();
			$observacion->comentario = $datos->comentario;
			$observacion->nombreObservador = $datos->nombreObservador;
			$observacion->emailObservador = $datos->emailObservador;
			$falla = new self();
			$falla->id = $datos->idFalla;
			$observacion->falla = $falla;
			$observacion->save();
		}

		public function cambiarEstado($datos, $usuario)
		{
			$CI = &get_instance();
			$nuevoEstado = $this->estado->cambiar($this, $datos, $usuario);
			$this->estado = $nuevoEstado;
			$CI->utiles->debugger($nuevoEstado);
			// $this->asociarEstado();
		}

		public function jsonSerialize() {
			// Estado conoce los datos que debe mostrar
	        // return array('id' => $this->id, );
	        return $this->estado->toJsonSerialize();
	    }

	}
 ?>