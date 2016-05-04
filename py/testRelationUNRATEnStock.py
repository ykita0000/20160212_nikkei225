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
        nikkei225
    INNER JOIN
        unrate ON datetime(nikkei225.date)=datetime(unrate.date)
    WHERE
        datetime(nikkei225.date)>='%s'
    '''%date_from
    print 'query'
    print q
    for i,row in enumerate(cur.execute(q)):
        # print row
        dt.append(row[0])
        stock_price.append([row[1],row[2],row[3],row[4]])
        unrate.append(row[7])
    
    stock_price = np.array(stock_price)
    unrate = np.array(unrate)
    
    ### time series same canvas
    nXBins = len(stock_price)
    hOp = TH1D('hOp','',nXBins,0,nXBins)
    hOp.SetLineColor(2)
    hHi = TH1D('hHi','',nXBins,0,nXBins)
    hHi.SetLineColor(3)
    hLo = TH1D('hLo','',nXBins,0,nXBins)
    hLo.SetLineColor(4)
    hCl = TH1D('hCl','',nXBins,0,nXBins)
    hCl.SetLineColor(6)
    hUNRATE = TH1D('hUNRATE','',nXBins,0,nXBins) 
    hUNRATE.SetLineColor(1)
    for i in xrange(nXBins):
        hOp.SetBinContent(i+1,stock_price[i][0])
        hHi.SetBinContent(i+1,stock_price[i][1])
        hLo.SetBinContent(i+1,stock_price[i][2])
        hCl.SetBinContent(i+1,stock_price[i][3])
        hUNRATE.SetBinContent(i+1,unrate[i])
    
    ### unrate vs stock plice
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
        gUnOp.SetPoint(i,unrate[i],stock_price[i][0])
        gUnHi.SetPoint(i,unrate[i],stock_price[i][1])
        gUnLo.SetPoint(i,unrate[i],stock_price[i][2])
        gUnCl.SetPoint(i,unrate[i],stock_price[i][3])

    
    c = TCanvas('c','Plot',512,512)
    c.Draw()
    c.Divide(1,3)
    c.cd(1)
    gPad.SetGrid(1)
    hOp.Draw()
    hHi.Draw('same')
    hLo.Draw('same')
    hCl.Draw('same')
    c.cd(2)
    gPad.SetGrid(1)

    # right_max = 1.1*hUNRATE.GetMaximum()
    # scale = gPad.GetUymax()/right_max
    # hUNRATE.Scale(scale)
    hUNRATE.Draw()
    
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
    if input=='q':
        break
    elif input=='':
        break
    elif input:
        date_from = input
    gDirectory.Delete('c;1')
    gDirectory.Delete('hOp;1')
    gDirectory.Delete('hHi;1')
    gDirectory.Delete('hLo;1')
    gDirectory.Delete('hCl;1')
    gDirectory.Delete('hUNRATE;1')



cur.close()
conn.close()
