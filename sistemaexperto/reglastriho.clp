;; Regla principal
(defrule enfermedades-matching
	(declare (salience 1))
	(enfermedad (ID ?ID) (name ?name) (planta ?planta) (sintoma-aa ?sintomaAAA) (sintoma-bb ?sibb)			   
			(sintoma-cc ?sintomacc)
			(stars ?stars))
	(analisis (planta "?"|?planta)
			(sintoma-aa "?"|?sintomaAAA)
			(sintoma-bb "?"|?sibb)
			(sintoma-cc "?"|?sintomacc))
=>
	(printout t ?ID "," ?planta "," ?sintomaAAA "," ?sibb ","  
		?sintomacc "," ?stars "---")
)

;; Reglas para calcular el rating de las calificaciones de las enfermedades
(defrule enfermedads-rating
	(declare (salience 2))
	?d <- (enfermedad (ID ?id) (stars ?s&:(= ?s -1)))
=>
	(bind ?count 0)
	(bind ?sum 0)
	(do-for-all-facts
		((?r review))
		(= ?r:enfermedad-id ?id)
		(bind ?count (+ ?count 1))
		(bind ?sum (+ ?sum ?r:stars)))
	(if (> ?count 0)
		then
	(modify ?d (stars (/ ?sum ?count)))
		else
	(modify ?d (stars 0)))
)
