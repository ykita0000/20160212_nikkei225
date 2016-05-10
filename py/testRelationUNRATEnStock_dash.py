#!/usr/bin/python
#coding:utf-8
'''
name   : testRelateionUNRATEnStock.py
author : ykita
date   : Wed May  4 16:18:46 JST 2016
memo   :  
'''
import os, os.path
import sys
import sqlite3
import ROOT
from ROOT import *
import numpy as np
import math
from datetime import datetime
import time
ROOT_TIME_OFFSET = 788918400

conn = sqlite3.connect('out/data.db',isolation_level=None)
cur = conn.cursor()
date_from = '1999-01-01'
while True:
    ### initialize data 
    dt = []
    stock_price = []
    unrate = []
    q = '''
    SELECT
        datetime(nikkei225.date),nikkei225.op,nikkei225.hi,nikkei225.lo,nikkei225.cl,nikkei225.vol,nikkei225.adjclo,unrate.percent
    FROM
        unrate
    INNER JOIN
        nikkei225 ON datetime(unrate.date)==datetime(nikkei225.date)
    WHERE
        datetime(unrate.date)>='%s'
    ORDER BY
        datetime(unrate.date) ASC
    '''%date_from
    print 'query'
    print q
    for i,row in enumerate(cur.execute(q)):
        print row
        tm = int(time.mktime(datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S').timetuple()))
        dt.append(tm-ROOT_TIME_OFFSET)
        stock_price.append([row[1],row[2],row[3],row[4]])
        unrate.append(row[7])
    
    stock_price = np.array(stock_price)
    unrate = np.array(unrate)
    
    ### time series same canvas
    nXBins = len(stock_price)
    # hOp = TH1D('hOp','',nXBins,0,nXBins)
    gOp = TGraph(nXBins)
    gOp.SetLineColor(2)
    gHi = TGraph(nXBins)
    gHi.SetLineColor(3)
    gLo = TGraph(nXBins)
    gLo.SetLineColor(4)
    gCl = TGraph(nXBins)
    gCl.SetLineColor(6)
    gUNRATE = TGraph(nXBins) 
    gUNRATE.GetXaxis().SetTitle('date')
    gUNRATE.GetYaxis().SetTitle('UNRATE [%]')
    gUNRATE.SetLineColor(1)
    for i in xrange(nXBins):
        gOp.SetPoint(i,dt[i],stock_price[i][0])
        gHi.SetPoint(i,dt[i],stock_price[i][1])
        gLo.SetPoint(i,dt[i],stock_price[i][2])
        gCl.SetPoint(i,dt[i],stock_price[i][3])
        gUNRATE.SetPoint(i,dt[i],unrate[i])
    
    ### unrate vs stock price
    gUnOp = TGraph(nXBins)
    gUnOp.SetMarkerStyle(2)
    gUnOp.SetMarkerColor(2)
    gUnHi = TGraph(nXBins)
    gUnHi.SetMarkerStyle(2)
    gUnHi.SetMarkerColor(3)
    gUnLo = TGraph(nXBins)
    gUnLo.SetMarkerStyle(2)
    gUnLo.SetMarkerColor(4)
    gUnCl = TGraph(nXBins)
    gUnCl.SetMarkerStyle(2)
    gUnCl.SetMarkerColor(6)
    for i in xrange(nXBins):
        gUnOp.SetPoint(i,unrate[i],math.log(stock_price[i][0],10))
        gUnHi.SetPoint(i,unrate[i],math.log(stock_price[i][1],10))
        gUnLo.SetPoint(i,unrate[i],math.log(stock_price[i][2],10))
        gUnCl.SetPoint(i,unrate[i],math.log(stock_price[i][3],10))
    
    c = TCanvas('c','Plot',512*2,512*2)
    c.Draw()
    c.Divide(1,3)
    c.cd(1)
    # gStyle.SetTimeOffset(-788918400)
    gStyle.SetNdivisions(515)
    gOp.GetXaxis().SetTimeDisplay(1)
    gOp.GetXaxis().SetTimeFormat('%Y-%m-%d')
    gPad.SetGrid(1)
    gOp.Draw('AL')
    gHi.Draw('Lsame')
    gLo.Draw('Lsame')
    gCl.Draw('Lsame')
    c.cd(2)
    gPad.SetGrid(1)
    # gStyle.SetTimeOffset(-788918400);
    gStyle.SetNdivisions(515)
    gUNRATE.GetXaxis().SetTimeDisplay(1)
    gUNRATE.GetXaxis().SetTimeFormat('%Y-%m-%d')

    # right_max = 1.1*hUNRATE.GetMaximum()
    # scale = gPad.GetUymax()/right_max
    # hUNRATE.Scale(scale)
    gUNRATE.Draw('AL')
    
    gPad.Update()
    
    c.cd(3)
    gPad.SetGrid(1)
    gUnOp.Draw('AP')
    gUnHi.Draw('P')
    gUnLo.Draw('P')
    gUnCl.Draw('P')
    
    gPad.Update()

    c1 = TCanvas('c1','Fitting',512,512)
    c1.Draw()
    gPad.SetGrid(1)
    gUnOp.Fit('expo')
    gUnOp.Draw('AP')
    c1.Update()

    input = raw_input('press q to quit or input span (format YYYY-MM-DD) > ')
    if input=='Q' or input=='q' or input=='':
        break
    # list = input.split('-')
    # print list
    # print len(list)
    # if len(list)!=3:
    #     continue
    # if int(list[0]) or int(list[1]) or int(list[2]):
    #     continue
    date_from = input
    gDirectory.Delete('c;1')
    gDirectory.Delete('hOp;1')
    gDirectory.Delete('hHi;1')
    gDirectory.Delete('hLo;1')
    gDirectory.Delete('hCl;1')
    gDirectory.Delete('hUNRATE;1')

cur.close()
conn.close()
