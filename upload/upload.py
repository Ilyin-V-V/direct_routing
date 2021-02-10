#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pip install requests
#pip install beautifulsoup4
import time
import requests
from bs4 import BeautifulSoup
import sys
import os
import re
sys.path.append('../conf/')
sys.path.append('../log/')
sys.path.append('../base/')
import conf
import logger
import postgres

class Upload(object):
 def __init__(self):
  self.name = "Upload"
  self.proxy = conf.Config().proxy
  self.rossvyaz_url = conf.Config().rossvyaz_url
  self.rossvyaz_tag_date = "doc__date small"
  self.rossvyaz_tag_file = "doc__download-list"
  self.rossvyaz_url_download = "https://rossvyaz.gov.ru"+\
    "/upload/gallery/\d*\w*/\d*\w*.csv"

 def get_html(self,url):
  try:
   html = requests.get(
    url,proxies=self.proxy,
    verify=False,timeout=15)
   html.raise_for_status()
   return (html.text," ")
  except requests.exceptions.RequestException as err:
   return (False,"Error:{}".format(err))

 def get_ver_html(self,html):
  search = BeautifulSoup(html,'html.parser')
  return search.find('div',class_=self.rossvyaz_tag_date)

 def get_base_ver(self):
  cur_ver = postgres.Postgres()
  conn,err = cur_ver.connect()
  if conn: t_ver,err = cur_ver.sql('select',conn,\
   "select ver_base from tbl_direct_route_system")
  else: logger.Logger().log_logged(
   'upload','Problem connect postgres '+\
   ' => err '+err); return False
  if len(t_ver) > 0:
   t_ver = t_ver[0]
   return t_ver[0]
  else: return False

 def check_ver(self,html_ver,base_ver):
  if html_ver.find(base_ver) == -1:
    return True
  else: return False

 def get_link_file(self,html):
  search = BeautifulSoup(html,'html.parser')
  div_link = search.findAll('div',class_=self.rossvyaz_tag_file)
  links = re.findall(self.rossvyaz_url_download,str(div_link))
  if not links or len(links) != 4: return False
  return links

 def upload_file(self,links):
  for i,link in enumerate(links):
   name = str(i)+'.csv'
   try:
    res = requests.get(
     link,proxies=self.proxy,
     verify=False,timeout=15)
    res.raise_for_status()
    with open('../download/'+name,'wb') as file:
     file.write(res.content)
    del res
   except requests.exceptions.RequestException as err:
    return (False,"Error:{}".format(err))

 def check_file(self):
  for root,dirs,files in os.walk('../download/',topdown = False):
   for name in files:
    mtime = file_mtime = os.stat('../download/'+name).st_mtime
    if mtime < time.time() - (int(1) * 86400): return False
   return True

 def main(self,run):
  if run != 'upload' and run != 'install':
   return (False,'None')
   print "Not found parameter for running !"
  log = logger.Logger(); upload = Upload()
  html,err = upload.get_html(upload.rossvyaz_url)
  # Get html
  if not html: log.log_logged(
   'upload','Connect '+upload.rossvyaz_url+"=>"+err); return (False,'None');

  # Get tabl ver base
  html_ver = str(upload.get_ver_html(html))
  if html_ver.find("Размещен:") == -1: log.log_logged(
    'upload','Version html not found '+\
    ' => table ver '+str(html_ver)); return (False,'None');

  if run == 'upload':
   base_ver = upload.get_base_ver()
   if not base_ver: log.log_logged(
    'upload','Table base version not found '+\
    ' => table ver '+str(base_ver)); return (False,'None');

  # New ver csv files ?
  if run == 'upload':
   new_ver = upload.check_ver(str(html_ver),str(base_ver))
   if not new_ver: log.log_logged(
    'upload','New version not found '+\
    'current ver '+base_ver+\
    ' => new ver '+html_ver); return (False,'None');

  # Get links files csv
  links = upload.get_link_file(html)
  if not links: log.log_logged(
   'upload','Links files not found '+\
   ' => links '+links); return (False,'None');

  # Upload files csv and check
  upload.upload_file(links)
  test_file = upload.check_file()
  if not test_file: log.log_logged(
   'upload','Files not new download '+\
   ' => Test '+str(test_file)); return (False,'None');
  else: log.log_logged(
   'upload','Files load new download '+\
   ' => Test '+str(test_file));

  html_ver = html_ver.split('\n')
  print "Download files csv"
  html_ver = re.findall('^\s*\D*(.*)',html_ver[1])
  return (True,html_ver[0])

if __name__ == "__main__":
 count_par = len(sys.argv)
 if count_par == 2:
  main = Upload()
  res,ver = main.main(sys.argv[1])
  if not res: print 'Not parameter for running upload ...'
  print res; print ver;
 elif count_par == 1:
  print 'Not parameter for running upload ...'
  print 'Reading Readme !'
