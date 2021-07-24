DELIMITER $

CREATE PROCEDURE obter_cenario_mape( IN V_IDT_MODELO INT, IN V_IDT_PERIODO INT, IN V_PARAMETRO VARCHAR(80), OUT V_MAPE DECIMAL(9,9) )
BEGIN
	SELECT mape INTO v_mape
	FROM cenario_previsao
	WHERE idt_modelo = V_IDT_MODELO
	AND idt_periodo = V_IDT_PERIODO
	AND parametro = V_PARAMETRO;
END;

CREATE PROCEDURE inserir_log_exec( IN V_IDT_EXEC INT, IN V_IDT_MODELO INT, IN V_IDT_PERIODO INT, IN V_PARAMETRO VARCHAR(80), IN V_MAPE DECIMAL(9,9) )

BEGIN
	
    DECLARE V_CENARIO INT;
    
	SELECT idt_cenario INTO V_CENARIO
    FROM cenario_previsao
    WHERE idt_modelo = V_IDT_MODELO
	AND idt_periodo = V_IDT_PERIODO
    AND parametro = V_PARAMETRO;
    
    IF v_cenario IS NULL THEN
		
		INSERT INTO cenario_previsao
        VALUES (V_IDT_MODELO, V_IDT_PERIODO, V_PARAMETRO, V_MAPE);
        
        SELECT idt_cenario INTO V_CENARIO
		FROM cenario_previsao
		WHERE idt_modelo = V_IDT_MODELO
		AND idt_periodo = V_IDT_PERIODO
		AND parametro = V_PARAMETRO;
        
    END IF;
    
    INSERT INTO log_execucao
	VALUES (V_IDT_EXEC, V_CENARIO, sysdate(), V_PARAMETRO, V_MAPE);
    COMMIT;
END;

DELIMETER ;