CREATE TABLE tbl_direct_route_ABC_8xx_master (
	abc	int,
	of	int,
	before	int,
	capacity	int,
	operator	varchar(300),
	region		varchar(300)
);
GRANT ALL ON tbl_direct_route_ABC_8xx_master TO postgres;