#!/usr/bin/python
#coding:utf-8
'''
name   : toSQLiteUNRATE.py
author : ykita
date   : Sat Feb 13 01:29:38 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3

conn = sqlite3.connect('out/data.db',isolation_level=None)
c = conn.cursor()
try: 
    c.execute('''CREATE TABLE unrate 
           (date text,percent real)''')
except:
    sys.stderr.write('table unrate already exists\n')

for i,line in enumerate(open('data/UNRATE.csv','r')):
    if i == 0: continue
    list = line.rstrip().split(",")
    q = """INSERT INTO unrate VALUES ('{}',{})""".format(
            list[0].encode('utf-8'),
            list[1]
            )
    c.execute(q)

c.close()
conn.close()

