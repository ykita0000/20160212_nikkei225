#!/usr/bin/python
#coding:utf-8
'''
name   : testSQLite.py
author : ykita
date   : Sat Feb 13 12:27:58 JST 2016
memo   : test sqlite date and time function 
'''
import os, os.path
import sys
import sqlite3
import ROOT
from ROOT import *

conn = sqlite3.connect('out/nikkei225.db',isolation_level=None)
c = conn.cursor()
q = '''SELECT julianday(date), date, op, hi, lo, cl FROM nikkei225 where date>="2000-01-01"'''
for i,row in enumerate(c.execute(q)):
    print row
c.close()
conn.close()
