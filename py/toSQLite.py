#!/usr/bin/python
#coding:utf-8
'''
name   : toSQLite.py
author : ykita
date   : Sat Feb 13 01:29:38 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3

conn = sqlite3.connect('out/nikkei225.db',isolation_level=None)
c = conn.cursor()
try: 
    c.execute('''CREATE TABLE nikkei225 
           (date text,op real,hi real,lo real,cl real,vol real,adjclo real)''')
except:
    sys.stderr.write('table nikkei225 already exists\n')

for i,line in enumerate(open('data/table.csv','r')):
    if i == 0: continue
    list = line.rstrip().split(",")
    q = """INSERT INTO nikkei225 VALUES ('{}',{},{},{},{},{},{})""".format(
            list[0].encode('utf-8'),
            list[1],
            list[2],
            list[3],
            list[4],
            list[5],
            list[6]
            )
    c.execute(q)

c.close()
conn.close()

