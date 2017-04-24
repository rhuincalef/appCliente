--Script para agregar las direcciones estimadas
ALTER TABLE public."DireccionModelo"
	ADD COLUMN rangoEstimado1 integer;
ALTER TABLE public."DireccionModelo"
	ADD COLUMN rangoEstimado2 integer;
