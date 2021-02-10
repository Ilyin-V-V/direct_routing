CREATE TABLE tbl_direct_route_ABC_3xx_slave (
	abc	int,
	of	int,
	before	int,
	capacity	int,
	operator	varchar(300),
	region		varchar(300)
);
GRANT ALL ON tbl_direct_route_ABC_3xx_slave TO postgres;
