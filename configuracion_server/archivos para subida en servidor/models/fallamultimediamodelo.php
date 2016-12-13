<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class FallaMultimediaModelo extends MY_Model
	{
		
		function __construct()
		{
			parent::__construct();
			$this->table_name = get_class($this);
		}

		public function save($falla)
		{
			log_message('debug', 'Estoy en save() guardando el objeto falla');
			log_message('debug', 'La tabla tiene: ');
			log_message('debug', $this->table_name);
			log_message('debug', '============================================');
			$this->db->insert($this->table_name,
							 array( 
							 		'idFalla' => $falla->idFalla,
                        			'idMultimedia' => $falla->idMultimedia
							 		)
							 );
			return $this->db->insert_id();
		}
	}

?>