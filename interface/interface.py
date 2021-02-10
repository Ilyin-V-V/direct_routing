#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sys
import time
sys.path.append('../conf/')
sys.path.append('../log/')
sys.path.append('../upload/')
sys.path.append('../load_base/')
sys.path.append('../routing/')
sys.path.append('../base/')
import conf
import logger
import load_base
import routing
import postgres

class Interface(object):
 def __init__(self):
  self.name = "Interface"
  self.date = datetime.strftime(datetime.now(),
   '%Y-%m-%d')

 def install(self):
  if load_base.Load().search_active_table():
   print "The script has already been installed. "+\
         "To reinstall, clear tables."
   return
  obj_upload = upload.Upload()
  load_csv,ver_csv = obj_upload.main('install')
  if not load_csv and not ver_csv:
   print "The problem of downloading csv files. "+\
         "To solve a problem ./upload/upload.py update."
  print "Load csv in tables ..."
  import_csv_base = load_base.Load().main('install','None')
  if not import_csv_base:
   print "The problem load csv in tables. "+\
         "To solve a problem ./upload/load_base.py update."
  ins_system = postgres.Postgres()
  conn,err = ins_system.connect()
  if conn: ins_system.sql('insert',conn,
   "insert into tbl_direct_route_system "+\
   "(version,date,ver_base,ver_tables) values "+\
   "(1,\'"+self.date+"\',\'"+ver_csv+"\','master')");
  else:
   print "Problem insert data tables tbl_direct_route_system."
  return True

 def base_download(self):
  obj_upload = upload.Upload()
  return obj_upload.main('upload')

 def base_load(self,ver):
  obj_load = load_base.Load()
  return obj_load.main('load',ver)

 def route(self,number):
  obj_route = routing.Route()
  return obj_route.main(number)

 def get_filial(self,number):
  try:
   return routing.Route().main(str(number))
  except Exception as error:
   logger.Logger().log_logged(
    'route','| Phone number => '+\
    str(number)+' | Problem exec functuon get_filial | '+\
    str(error)+' | Error | '); return False;

if __name__ == "__main__":
 log = logger.Logger()
 interface = Interface()
 count_par = len(sys.argv)
 if count_par == 2 or count_par == 3:

  if sys.argv[1] == 'install':
   if interface.install():
    print "Installation was successful !"

  if sys.argv[1] == 'upload':
   upload = interface.base_download()
   print upload

  if sys.argv[1] == 'load':
   if len(sys.argv) == 3:
    load = interface.base_load(sys.argv[2])
    print load
   else:
    print 'Not full parameter interface ...'

  if sys.argv[1] == 'update':
   import upload
   upload,ver = interface.base_download()
   if ver != 'None':
    print 'New find version '+' => '+ver
    print 'Load database ...'
    load = interface.base_load(ver)
    if load == True:
     print str(load)+' => '+'Load base successful !'
     logger.Logger().tmp_file('1')
    else:
     print str(load)+' => '+'Problem load base ...!'
     logger.Logger().tmp_file('0')
   else:
    print 'New verison not found ...!'

  if sys.argv[1] == 'route':
   if len(sys.argv) == 3:
    region = interface.route(sys.argv[2])
   else:
     print 'Not full parameter interface ...'

 else:
  print 'Not parameter for running interface ...'
  print 'Reading Readme !'
