#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
sys.path.append('../conf/')
sys.path.append('../log/')
sys.path.append('../base/')
import conf
import logger
import postgres

class Route(object):
 def __init__(self):
  self.name = "Route"

 def number_split(self,number):
  return (number[1:4],number[4:11])

 def get_active_table(self):
  cur_ver = postgres.Postgres()
  conn,err = cur_ver.connect()
  if conn: t_ver,err = cur_ver.sql('select',conn,\
   "select ver_tables from tbl_direct_route_system")
  else: logger.Logger().log_logged(
   'route','Problem connect postgres '+\
   ' => err '+err); return False
  if len(t_ver) > 0:
   t_ver = t_ver[0]
   return t_ver[0]
  else: return False

 def find_table_numeracii(self,code,ver):
  if ver == "slave":
   for key,value in conf.Config().pg_slave_tabl.items():
    if key[0:1] == code: return value;
  if ver == "master":
   for key,value in conf.Config().pg_master_tabl.items():
    if key[0:1]	== code: return value;
  return False

 def search_region(self,cod,number,table):
  conn,err = postgres.Postgres().connect()
  if conn: region,err = postgres.Postgres().sql(
   'select',conn,'select region from '+table+\
   ' where abc = '+cod+' and of <= '+number+\
   ' and before >= '+number)
  else: logger.Logger().log_logged(
   'route','Problem connect postgres '+\
   ' => err '+err); return False
  if len(region) > 0:
   region = region[0]
   return region[0]
  else: return False

 def search_filial(self,region):
  conn,err = postgres.Postgres().connect()
  if conn: filial,err = postgres.Postgres().sql(
   'select',conn,'select region,code from tbl_direct_route_region')
  else: logger.Logger().log_logged(
   'route','Problem connect postgres '+\
   ' => err '+err); return False
  if len(filial) > 0:
   for item in filial:
    if len(re.findall(item[0],region)) != 0 or \
       len(re.findall(region,item[0])):
     return item[1]
  else: return False

 def main(self,number):
  if not re.match('^\d\d\d\d\d\d\d\d\d\d\d',number):
   print "Not found parameter for running !"
   logger.Logger().log_logged('route','| Phone number => '+\
    str(number)+' | Does not match regex |');
   return False
  log = logger.Logger(); route = Route()

  # Get code and number
  code,number = route.number_split(number)
  if not code or not number: log.log_logged(
   'route','| Phone number => '+\
   str(number)+' | Code or number not found | '+\
   str(code)+' | Code |'+str(number)+' | Number |'); print False; return False;

  # Get version tables
  tabl_ver = route.get_active_table()
  if not tabl_ver: log.log_logged(
   'route','| Phone number => '+\
   str(code)+str(number)+' | Table version not found | '+\
   str(tabl_ver)+' | Tabl ver |'); print False; return False;

  # Find table numeracii
  tabl_name = route.find_table_numeracii(code[0:1],tabl_ver)
  if not tabl_name: log.log_logged(
   'route','| Phone number => '+\
   str(code)+str(number)+' | Table numeracii not found | '+\
   str(tabl_name)+' | Tabl numeracii |'); print False; return False;
  
  # Find region
  region = route.search_region(code,number,tabl_name)
  if not region: log.log_logged(
   'route','| Phone number => '+\
   str(code)+str(number)+' | Phone not found in databases | '+\
   str(region)+' | Region |'); print False; return False;

  # Find filial
  filial = route.search_filial(region)
  if not filial: log.log_logged(
   'route','| Phone number => '+\
   str(code)+str(number)+' | Not filial in regions | '+\
   str(region)+' | Filial |'); print False; return False;
  else: log.log_logged(
   'route','| Phone number => '+\
   str(code)+str(number)+' | Filial in regions | '+\
   str(region)+' | Filial |'); print filial; return filial;

if __name__ == "__main__":
 count_par = len(sys.argv)
 if count_par == 2:
  main = Route()
  region = main.main(sys.argv[1])
 else:
  logger.Logger().log_logged('route','| Phone number => '+\
   'not found |');
  print 'Not parameter for running route ...'
  print 'Reading Readme !'
