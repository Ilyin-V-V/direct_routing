CREATE TABLE tbl_direct_route_region (
	id	SERIAL,
	region	varchar(100),
	code	varchar(20)
);
GRANT ALL ON tbl_direct_route_region TO postgres;
