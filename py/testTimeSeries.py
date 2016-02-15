#!/usr/bin/python
#coding:utf-8
'''
name   : testTimeSeries.py
author : ykita
date   : Sun Feb 14 14:38:36 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3
import ROOT
from ROOT import *

Date = []
Op = []
Hi = []
Lo = []
Cl = []

conn = sqlite3.connect('out/nikkei225.db',isolation_level=None)
c = conn.cursor()
q = '''SELECT julianday(date), op, hi, lo, cl FROM nikkei225 where date>="2000-01-01"'''
for i,row in enumerate(c.execute(q)):
    Date.append(row[0])
    Op.append(row[1])
    Hi.append(row[2])
    Lo.append(row[3])
    Cl.append(row[4])
c.close()
conn.close()

gOp = TGraph(len(Date))
gOp.SetLineColor(2)
gHi = TGraph(len(Date))
gLo = TGraph(len(Date))
gCl = TGraph(len(Date))
gCl.SetLineColor(4)
for i,(d,(o,(h,(l,c)))) in enumerate(zip(Date,zip(Op,zip(Hi,zip(Lo,Cl))))):
    gOp.SetPoint(i,d,o)
    gHi.SetPoint(i,d,h)
    gLo.SetPoint(i,d,l)
    gCl.SetPoint(i,d,c)

c = TCanvas("c","",512*2,512)
gPad.SetGrid(1)
gOp.Draw('AL')
gHi.Draw('ALSAME')
gLo.Draw('ALSAME')
gCl.Draw('ALSAME')
raw_input('>')

