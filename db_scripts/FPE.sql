CREATE TABLE `MODELO_PREVISAO` (
  `IDT_MODELO` INT PRIMARY KEY,
  `DSC_MODELO` VARCHAR(40)
);

CREATE TABLE `PERIODO_PREVISAO` (
  `IDT_PERIODO` INT PRIMARY KEY,
  `INICIO` DATE,
  `FIM` DATE,
  `DURACAO` DECIMAL(4,0)
);

CREATE TABLE `CENARIO_PREVISAO` (
  `IDT_CENARIO` INT PRIMARY KEY,
  `IDT_MODELO` INTEGER,
  `IDT_PERIODO` INTEGER,
  `PARAMETRO` VARCHAR(80),
  `MAPE` DECIMAL(9,9)
);

CREATE TABLE `LOG_EXECUCAO` (
  `IDT_EXEC` VARCHAR(40),
  `IDT_CENARIO` INT,
  `DAT_HORA` DATETIME,
  `PARAMETRO` VARCHAR(80),
  `MAPE` DECIMAL(9,9)
);

ALTER TABLE `CENARIO_PREVISAO` ADD FOREIGN KEY (`IDT_MODELO`) REFERENCES `MODELO_PREVISAO` (`IDT_MODELO`);

ALTER TABLE `CENARIO_PREVISAO` ADD FOREIGN KEY (`IDT_PERIODO`) REFERENCES `PERIODO_PREVISAO` (`IDT_PERIODO`);
