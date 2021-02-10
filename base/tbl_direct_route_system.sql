CREATE TABLE tbl_direct_route_system (
	version	int DEFAULT 1,
	date	date,
	ver_base	varchar(100),
	ver_tables	varchar(20) DEFAULT 'master' --master or slave
);
GRANT ALL ON tbl_direct_route_system TO postgres;
