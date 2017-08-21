<?php 
	class TipoFallaCriticidadModelo extends MY_Model
	{		
		
		function __construct()
		{
			parent::__construct();
			$this->table_name = get_class($this);
		}

		//Retorna un array de ids TipoFalla-Criticidad
		public function getCriticidadesAsociadas($idTipoFalla)
		{
			$query = $this->db->get_where('TipoFallaCriticidadModelo', array('idTipoFalla' => $idTipoFalla));
			if (empty($query->result())) {
			 throw new MY_BdExcepcion('Sin resultados de criticidad');
			}
			return $query->result();
		}

}

?>