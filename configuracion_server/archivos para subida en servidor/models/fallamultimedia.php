<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
	class FallaMultimedia
	{
		
		var $idFalla;
		var $idMultimedia;

		function __construct()
		{
			
		}

		// Retorna una nueva instancia siempre de una fallaMultiemdia
		static public function getInstancia($datos)
		{
			$CI = &get_instance();
			$fallaMultimedia = new FallaMultimedia();
			$fallaMultimedia->idFalla = $datos["idFalla"];
			$fallaMultimedia->idMultimedia = $datos["idMultimedia"];
			return $fallaMultimedia;
		}


		public function save()
		{
			$CI = &get_instance();
			log_message('debug', 'En FallaMultimedia.save()...');
			log_message('debug', 'tipo de fallaMultimedia: '.gettype($this));
			log_message('debug', 'tipo de FallaMultimediaModelo: '.gettype($CI->FallaMultimediaModelo));
			return $CI->FallaMultimediaModelo->save($this);
		}

	}

		
?>