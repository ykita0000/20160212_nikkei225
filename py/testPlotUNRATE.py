#!/usr/bin/python
#coding:utf-8
'''
name   : testPlotUNRATE.py
author : ykita
date   : Wed Feb 17 22:30:12 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3
import ROOT
from ROOT import *


date = []
x = []

conn = sqlite3.connect('out/data.db',isolation_level=None)
c = conn.cursor()
for i,row in enumerate(c.execute('''SELECT julianday(date), percent FROM unrate''')):
    date.append(row[0]) 
    x.append(row[1]) 
    # h.Fill(row[1])
c.close()
conn.close()

h = TH1D('h','',40,0,20)
g = TGraph(len(date))
for i,(dd,xx) in enumerate(zip(date,x)):
    g.SetPoint(i,dd,xx)
    h.Fill(xx)

c = TCanvas('c','',512,512)
c.Divide(1,2)
c.cd(1)
gPad.SetGrid(1)
h.Draw()
c.cd(2)
gPad.SetGrid(1)
g.Draw('AL')
c.Update()
raw_input('>')
