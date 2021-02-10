#!/usr/bin/env python
# -*- coding: utf-8 -*-
# yum install postgresql-devel
# yum install python-devel
# yum install gcc
import psycopg2
import sys
sys.path.append('../conf/')
sys.path.append('../log/')
import conf
import logger

class Postgres(object):
 def __init__(self):
  self.name = "Postgres"
  self.host = conf.Config().pg_host
  self.port = conf.Config().pg_port
  self.base = conf.Config().pg_base
  self.user = conf.Config().pg_user
  self.password = conf.Config().pg_password

 def connect(self):
  try:
   conn = psycopg2.connect(
          host = self.host,
          port = self.port,
          dbname = self.base,
          user = self.user,
          password = self.password)
   return (conn,'None')
  except psycopg2.Error as err:
   logger.Logger().log_logged(
   'postgres','Connect postgres '+" => "+str(err));
   return (False,"Error:{}".format(err))

 def sql(self,act,conn,sql_query):
  cur = conn.cursor()
  try:
   cur.execute(sql_query)
   if act == 'select': res = cur.fetchall()
   if act == 'insert' or act == 'update' or act == 'delete':
      res = conn.commit()
   return (res,'None')
  except psycopg2.Error as err:
   logger.Logger().log_logged(
   'postgres','Sql postgres problem '+" => "+str(err));
   return (False,"Error:{}".format(err))
  finally:
    conn.close()

 def main(self):
  log = logger.Logger(); psql = Postgres()
  conn,err = psql.connect()
  if not conn: log.log_logged(
   'load_base','Connect postgres '+" => "+str(err)); return False;
  res,err = psql.sql('select',conn,"select ver_base from tbl_direct_route_system")
  if not res: log.log_logged(
   'load_base','Sql postgres problem '+" => "+str(err)); return False;
  print "Result: "+str(res)+" | Error: "+str(err)

if __name__ == "__main__":
 main = Postgres()
 main.main()
