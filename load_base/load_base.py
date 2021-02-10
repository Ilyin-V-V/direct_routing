#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from time import sleep
from datetime import datetime
sys.path.append('../conf/')
sys.path.append('../log/')
sys.path.append('../base/')
import conf
import logger
import postgres

class Load(object):
 def __init__(self):
  self.name = "Load"
  self.date = datetime.strftime(datetime.now(),
   '%Y-%m-%d')
  self.numeracii = {
   '3xx': ' ',
   '4xx': ' ',
   '8xx': ' ',
   '9xx': ' '
  }
  self.delta = 500 # Delta change tables

 def load_numeracii(self):
  files = os.listdir("../download/")
  if len(files) >= 4:
   for file in files: 
    arr_files = open("../download/"+file,'r')
    lines = arr_files.readlines()
    count = 0
    for line in lines:
     count += 1
     if count == 2:
      res_str = line.strip().split(';')
      if res_str[0].find('3',0,1) == 0:
       self.numeracii['3xx'] = file
      if res_str[0].find('4',0,1) == 0:
       self.numeracii['4xx'] = file
      if res_str[0].find('8',0,1) == 0:
       self.numeracii['8xx'] = file
      if res_str[0].find('9',0,1) == 0:
       self.numeracii['9xx'] = file
      if count == 2: break
   return True
  else: return False

 def check_numeracii(self):
  if self.numeracii['3xx'] == " ": return False
  if self.numeracii['4xx'] == " ": return False
  if self.numeracii['8xx'] == " ": return False
  if self.numeracii['9xx'] == " ": return False
  return True

 def search_active_table(self):
  cur_ver = postgres.Postgres()
  conn,err = cur_ver.connect()
  if conn: t_ver,err = cur_ver.sql('select',conn,\
   "select ver_tables from tbl_direct_route_system")
  else: logger.Logger().log_logged(
   'load_base','Problem connect postgres '+\
   ' => err '+err); return False
  if len(t_ver) > 0:
   t_ver = t_ver[0]
   return t_ver[0]
  else: return False

 def load_base(self,ver):
  if ver == "slave":
   for key,value in conf.Config().pg_slave_tabl.items():
    delete = Load().clear_table_postgres(conf.Config().pg_slave_tabl[key])
    if not delete: return (False,str(key))
    count = Load().check_integrity_tabl_postgres(conf.Config().pg_slave_tabl[key])
    if count != 0: return (False,str(key))
    logger.Logger().log_logged('load_base','Delete table '+\
     '=> '+str(conf.Config().pg_slave_tabl[key]));
    load = Load().load_base_postgres(self.numeracii[key],
     conf.Config().pg_slave_tabl[key])
    if not load: return (False,str(key))
  if ver == "master":
   for key,value in conf.Config().pg_master_tabl.items():
    delete = Load().clear_table_postgres(conf.Config().pg_master_tabl[key])
    if not delete: return (False,str(key))
    count = Load().check_integrity_tabl_postgres(conf.Config().pg_master_tabl[key])
    if count != 0: return (False,str(key))
    logger.Logger().log_logged('load_base','Delete table '+\
     '=> '+str(conf.Config().pg_slave_tabl[key]));
    load = Load().load_base_postgres(self.numeracii[key],
     conf.Config().pg_master_tabl[key])
    if not load: return (False,str(key))
  return (True,'None')

 def check_integrity_tabl(self,ver):
  if ver == "slave":
   for key,value in conf.Config().pg_slave_tabl.items():
    test = Load().check_test_table(
     Load().check_integrity_tabl_postgres(conf.Config().pg_slave_tabl[key]),
     Load().check_integrity_tabl_postgres(conf.Config().pg_master_tabl[key])
    )
    if not test: return (False,str(key))
  if ver == "master":
   for key,value in conf.Config().pg_master_tabl.items():
    test = Load().check_test_table(
     Load().check_integrity_tabl_postgres(conf.Config().pg_master_tabl[key]),
     Load().check_integrity_tabl_postgres(conf.Config().pg_slave_tabl[key])
    )
    if not test: return (False,str(key))
  return (True,'None')

 def clear_table_postgres(self,tabl):
  clear = postgres.Postgres()
  conn,err = clear.connect()
  if conn: res,err = clear.sql('delete',conn,\
   "delete from "+tabl)
  else: logger.Logger().log_logged(
   'load_base','Problem connect postgres '+\
   ' => err '+err); return False
  return True

 def load_base_postgres(self,numeracii,name_tabl):
  count = 0; send = 0; bufer = []; 
  portion = conf.Config().pg_portion;
  col_str = Load().get_col_str_file(numeracii)
  file = open("../download/"+numeracii,'r')
  lines = file.readlines()
  for line in lines:
   count += 1; min_bufer = col_str - portion;
   if count > 1:
    str = line.strip().split(';'); send += 1
    Load().bufer_append(bufer,str[0],str[1],
     str[2],str[3],str[4],str[5])
    if send == portion or count == min_bufer:
     insert = Load().insert_base_postgres(bufer,name_tabl)
     del bufer [:]; send = 0;
     sleep(conf.Config().pg_sleep)
     if not insert: return False
  return True

 def get_col_str_file(self,name_file):
  with open("../download/"+name_file) as file:
   line_count = 0
   for line in file:
    line_count += 1
  return line_count

 def bufer_append(self,bufer,abc,of,
  before,capacity,operator,region):
  bufer.append(
   "("+re.sub(r'"',"",abc)+","+\
   re.sub(r'"',"",of)+","+\
   re.sub(r'"',"",before)+","+\
   re.sub(r'"',"",capacity)+","+\
   '\''+re.sub(r'"',"",operator)+"',"+\
   '\''+re.sub(r'"',"",region)+"')"
  )
  return bufer

 def insert_base_postgres(self,bufer,tabl):
  load_tabl = postgres.Postgres()
  conn,err = load_tabl.connect()
  if conn: load_tabl.sql('insert',conn, 
   "insert into "+tabl+\
   "(abc,of,before,capacity,operator,region) values "+\
   ','.join(bufer)); logger.Logger().log_logged(
   'load_base','Insert data postgres '+\
   'insert string '+','.join(bufer)); return True
  else: logger.Logger().log_logged(
   'load_base','Problem connect postgres '+\
   'insert string '+bufer+\
   ' => err '+err); return False

 def check_integrity_tabl_postgres(self,tabl):
  cur_cou = postgres.Postgres()
  conn,err = cur_cou.connect()
  if conn: t_count,err = cur_cou.sql('select',conn,\
   "select count(*) from "+tabl)
  else: logger.Logger().log_logged(
   'load_base','Problem connect postgres '+\
   ' => err '+err); return False
  if len(t_count) > 0:
   t_count = t_count[0]
   return t_count[0]
  else: return False  

 def check_test_table(self,load,active):
  if load == 0 or active == 0:
   return False
  if load < active - self.delta:
    return False
  return True

 def update_ver_tables(self,ver):
  update_ver = postgres.Postgres()
  conn,err = update_ver.connect()
  if conn: res,err = update_ver.sql('update',conn,\
   "update tbl_direct_route_system set ver_tables = '"+\
   ver+"' where version = 1")
  else: logger.Logger().log_logged(
   'load_base','Problem connect postgres '+\
   ' => err '+err); return False
  return True

 def update_ver_base(self,ver):
  update_ver = postgres.Postgres()
  conn,err = update_ver.connect()
  if conn: res,err = update_ver.sql('update',conn,\
   "update tbl_direct_route_system set ver_base = '"+\
   ver+"', date = '"+self.date+"' where version = 1")
  else: logger.Logger().log_logged(
   'load_base','Problem connect postgres '+\
   ' => err '+err); return False
  return True

 def main(self,run,csv_vers):
  if run != 'load' and run != 'install':
   print "Not found parameter for running !"
   return (False,'None')
  if not csv_vers:
   print "Not found parameter for running !"
   return (False,'None')
  log = logger.Logger(); load = Load()

  # Get data files csv
  set_num = load.load_numeracii()
  if not set_num: log.log_logged(
   'load_base','Files not found in directory download'); return False;
  if not load.check_numeracii(): log.log_logged(
   'load_base','Incomplete csv file directory download'); return False;

  # Get version tables
  if run == 'load':
   tabl_ver = load.search_active_table()
   if not tabl_ver: log.log_logged(
    'load_base','Table version not found '+\
    ' => table ver '+str(tabl_ver)); return False;
  if run == 'install':
   tabl_ver = 'slave'

  # Load csv in tables
  if tabl_ver == 'master':
   load_b,err = load.load_base('slave')
   if not load_b: log.log_logged(
    'load_base','Problem load data in tables slave'+\
    ' err table => '+str(err)); return False;

  if tabl_ver == 'slave':
   load_b,err = load.load_base('master')
   if not load_b: log.log_logged(
    'load_base','Problem load data in tables master'+\
    ' err table => '+str(err)); return False;

  # Test data load tables
  if run == 'load':
   if tabl_ver == 'master':
    test,err = load.check_integrity_tabl('slave')
    if not test: log.log_logged(
     'load_base','Problem test data in tables upload slave'+\
     ' err table => '+str(err)); return False;

   if tabl_ver == 'slave':
    test,err = load.check_integrity_tabl('master')
    if not test: log.log_logged(
     'load_base','Problem test data in tables upload master'+\
     ' err table => '+str(err)); return False;

  # Update column ver_tables tbl_direct_route_system
  if run == 'load':
   if tabl_ver == 'master':
    update_ver = load.update_ver_tables('slave')
    if not update_ver: log.log_logged(
     'load_base','Problem update column ver_tables '+\
     'tbl_direct_route_system in slave'); return False;

   if tabl_ver == 'slave':
    update_ver = load.update_ver_tables('master')
    if not update_ver: log.log_logged(
     'load_base','Problem update column ver_tables '+\
     'tbl_direct_route_system in master'); return False;

  # Update column ver_base tbl_direct_route_system
  if run == 'load':
   if tabl_ver == 'master':
    update_ver = load.update_ver_base(csv_vers)
    if not update_ver: log.log_logged(
     'load_base','Problem update column ver_base '+\
     'tbl_direct_route_system in slave'); return False;

   if tabl_ver == 'slave':
    update_ver = load.update_ver_base(csv_vers)
    if not update_ver: log.log_logged(
     'load_base','Problem update column ver_base '+\
     'tbl_direct_route_system in master'); return False;

  print "Load tables database"; return True;

if __name__ == "__main__":
 count_par = len(sys.argv)
 if count_par == 3:
  main = Load()
  res = main.main(sys.argv[1],sys.argv[2])
  if not res: print 'Not parameter for running load ...'
  print res
 else:
  print 'Not parameter for running load ...'
  print 'Reading Readme !'
