CREATE TABLE thermometerdata.data_entries (
	id INTEGER auto_increment NOT NULL,
	device_id varchar(100) NOT NULL,
	temp FLOAT NOT NULL,
	humidity FLOAT NOT NULL,
	`timestamp` DATETIME NOT NULL,
	CONSTRAINT NewTable_PK PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci;
