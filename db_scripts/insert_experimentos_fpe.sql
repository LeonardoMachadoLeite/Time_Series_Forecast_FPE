USE fpe;

INSERT INTO modelo_previsao (dsc_modelo)
VALUES ('Holt-Winters');
INSERT INTO modelo_previsao (dsc_modelo)
VALUES ('SARIMA');

INSERT INTO periodo_previsao (inicio, fim, duracao)
VALUES	('2019-01-31', '2019-01-31', 1),
		('2019-01-31', '2019-06-30', 6),
        ('2019-01-31', '2019-12-31', 12);

COMMIT;