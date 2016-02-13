#!/usr/bin/python
#coding:utf-8
'''
name   : testPlot.py
author : ykita
date   : Sat Feb 13 12:27:58 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3
import ROOT
from ROOT import *

conn = sqlite3.connect('out/nikkei225.db',isolation_level=None)
c = conn.cursor()
hOpen = TH1D('hOpen','',100,0,50000)

for i,row in enumerate(c.execute('''SELECT * FROM nikkei225''')):
    hOpen.Fill(row[1])

c.close()
conn.close()

hOpen.Draw()
raw_input('>')
