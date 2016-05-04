#!/usr/bin/python
#coding:utf-8
'''
name   : testHiLo.py
author : ykita
date   : Sun Feb 14 14:08:33 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3
import ROOT
from ROOT import *

h = TH1D('h','',100,0,2500)

conn = sqlite3.connect('out/data.db',isolation_level=None)
cur = conn.cursor()
for i,row in enumerate(cur.execute('''SELECT * FROM nikkei225''')):
    h.Fill(row[2]-row[3])
    print row
cur.close()
conn.close()

c = TCanvas('c','',511,512)
c.Draw()
h.Draw()
c.Update()
raw_input('>')
