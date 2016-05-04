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

hOp = TH1D('hOp','',100,0,50000)
hHi = TH1D('hHi','',100,0,50000)
hLo = TH1D('hLo','',100,0,50000)
hCl = TH1D('hCl','',100,0,50000)

conn = sqlite3.connect('out/data.db',isolation_level=None)
c = conn.cursor()
for i,row in enumerate(c.execute('''SELECT datetime(date),op,hi,lo,cl,vol,adjclo FROM nikkei225 where date>='2000-01-01' ''')):
    hOp.Fill(row[1])
    hHi.Fill(row[2])
    hLo.Fill(row[3])
    hCl.Fill(row[4])
c.close()
conn.close()

hOp.Draw()
hHi.Draw('SAME')
hLo.Draw('SAME')
hCl.Draw('SAME')
raw_input('>')
