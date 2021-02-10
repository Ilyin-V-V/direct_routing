#!/usr/bin/env python

class Config:
 def __init__(self):
  # Path
  self.path = " "
  self.path_log = " "
  self.path_tmp = " "
  # Http
  self.rossvyaz_url = "https://rossvyaz.gov.ru/"+\
   "deyatelnost/resurs-numeracii/vypiska-iz-reestra"+\
   "-sistemy-i-plana-numeracii"
  self.proxy = {
   "http": "http://ip:port/",
   "https": "http://ip:port/"
  }
  # Postgres
  self.pg_host = "127.0.0.1"
  self.pg_port = "5432"
  self.pg_base = "base"
  self.pg_user = "user"
  self.pg_password = "pass"
  self.pg_portion = 10
  # Stress test sleep 0 load ~ 7 min
  self.pg_sleep = 0.5 # ~10h
  # Name tables
  self.pg_master_tabl = {
   '3xx': 'tbl_direct_route_ABC_3xx_master',
   '4xx': 'tbl_direct_route_ABC_4xx_master',
   '8xx': 'tbl_direct_route_ABC_8xx_master',
   '9xx': 'tbl_direct_route_DEF_9xx_master'
  }
  self.pg_slave_tabl = {
   '3xx': 'tbl_direct_route_ABC_3xx_slave',
   '4xx': 'tbl_direct_route_ABC_4xx_slave',
   '8xx': 'tbl_direct_route_ABC_8xx_slave',
   '9xx': 'tbl_direct_route_DEF_9xx_slave'
  }
