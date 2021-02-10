#!/usr/bin/env python
from datetime import datetime
import sys
sys.path.append('../conf/')
import conf

class Logger():
 def __init__(self):
  self.name = 'Logger'
  self.date = datetime.strftime(datetime.now(),
   '%d:%m:%Y-%H:%M:%S')

 def log_logged(self,action,data):
  obj_log = conf.Config()
  if action == 'upload':
   file_path = obj_log.path_log+'/upload.log'
  if action == 'load_base':
   file_path = obj_log.path_log+'/load_base.log'
  if action == 'route':
   file_path = obj_log.path_log+'/route.log'
  if action == 'postgres':
   file_path = obj_log.path_log+'/postgres.log'
  file = open(file_path, 'a')
  data = self.date+' '+data
  file.write(data +"\n")
  file.close()

 def tmp_file(self,data):
  obj_log = conf.Config()
  file_path = obj_log.path_tmp+'/numeracii.tmp'
  file = open(file_path, 'w')
  file.write(str(data) +"\n")
  file.close()

