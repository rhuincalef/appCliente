<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class DireccionModelo extends MY_Model
	{
		
		function __construct()
		{
			parent::__construct();
			$this->table_name = get_class($this);
		}

		public function save($direccion)
		{
			$this->db->insert($this->table_name,
							array('idCallePrincipal' => $direccion->callePrincipal->id,
								'altura' => $direccion->altura,
								'idCalleSecundariaA' => $direccion->calleSecundariaA->id,
								'idCalleSecundariaB' => $direccion->calleSecundariaB->id,
								'rangoestimado1' => $direccion->rangoestimado1,
								'rangoestimado2' => $direccion->rangoestimado2
								)
							);
			return $this->db->insert_id();
		}

		/**
		 * Fetch a single record based on the array $datos.
		 * $datos array as $column => $value
		 */
		public function get_by($datos)
		{
			$this->utiles->debugger($datos->idCallePrincipal);
		    // foreach ($datos as $column => $value) {
		        // $this->db->like("LOWER($column)", strtolower($value));
	        $query = $this->db->get_where($this->table_name, array('idCallePrincipal' => $datos->idCallePrincipal,
				'altura' => $datos->altura,
				//AGREGADO RODRIGO
				'rangoestimado1' => $datos->rangoEstimado1,
				'rangoestimado2' => $datos->rangoEstimado2,
				'idCalleSecundariaA' => $datos->idCalleSecundariaA,
				'idCalleSecundariaB' => $datos->idCalleSecundariaB
				)
	        );
		    // }
		    // $query = $this->db->get($this->table_name);
		    if (empty($query->result())) {
		        throw new MY_BdExcepcion('Sin resultados');
		    }
		    return $query->result()[0];
		}

	}
 ?>