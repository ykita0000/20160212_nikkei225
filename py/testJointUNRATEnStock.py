#!/usr/bin/python
#coding:utf-8
'''
name   : testJointUNRATEnStock.py
author : ykita
date   : Tue May 10 14:53:59 JST 2016
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
date_from = '1999-01'
while True:
    ### initialize data 
    dt = []
    stock_price_op = []
    stock_price_hi = []
    stock_price_lo = []
    stock_price_cl = []
    unrate = []
    q = '''
    SELECT
        strftime("%Y-%m",unrate.date),
        avg(nikkei225.op),min(nikkei225.op),max(nikkei225.op),
        avg(nikkei225.hi),min(nikkei225.hi),max(nikkei225.hi),
        avg(nikkei225.lo),min(nikkei225.lo),max(nikkei225.lo),
        avg(nikkei225.cl),min(nikkei225.cl),max(nikkei225.cl),
        nikkei225.vol,nikkei225.adjclo,unrate.percent
    FROM
        unrate
    INNER JOIN
        nikkei225 ON strftime("%Y-%m",unrate.date)==strftime("%Y-%m",nikkei225.date)
    WHERE
        strftime("%Y-%m",unrate.date)>="{}"
    GROUP BY
        strftime("%Y-%m",nikkei225.date)
    ORDER BY
        date(unrate.date) ASC, date(nikkei225.date) ASC
    '''.format(date_from)
    print 'query'
    print q
    for i,row in enumerate(cur.execute(q)):
        print row
        tm = int(time.mktime(datetime.strptime(row[0],'%Y-%m').timetuple()))
        dt.append(tm-ROOT_TIME_OFFSET)
        stock_price_op.append([row[1],row[1]-row[2],row[3]-row[1]])
        stock_price_hi.append([row[4],row[4]-row[5],row[6]-row[4]])
        stock_price_lo.append([row[7],row[7]-row[8],row[9]-row[7]])
        stock_price_cl.append([row[10],row[10]-row[11],row[12]-row[10]])
        unrate.append(row[15])

    nXBins = len(unrate)
    stock_price_op_v = [ TVectorD(nXBins), TVectorD(nXBins), TVectorD(nXBins) ]
    stock_price_lo_v = [ TVectorD(nXBins), TVectorD(nXBins), TVectorD(nXBins) ]
    stock_price_hi_v = [ TVectorD(nXBins), TVectorD(nXBins), TVectorD(nXBins) ]
    stock_price_cl_v = [ TVectorD(nXBins), TVectorD(nXBins), TVectorD(nXBins) ]
    unrate_v = [ TVectorD(nXBins), TVectorD(nXBins), TVectorD(nXBins) ]

    for i in xrange(nXBins):
        stock_price_op_v[0][i] = stock_price_op[i][0]
        stock_price_op_v[1][i] = stock_price_op[i][1]
        stock_price_op_v[2][i] = stock_price_op[i][2]
        stock_price_lo_v[0][i] = stock_price_lo[i][0]
        stock_price_lo_v[1][i] = stock_price_lo[i][1]
        stock_price_lo_v[2][i] = stock_price_lo[i][2]
        stock_price_hi_v[0][i] = stock_price_hi[i][0]
        stock_price_hi_v[1][i] = stock_price_hi[i][1]
        stock_price_hi_v[2][i] = stock_price_hi[i][2]
        stock_price_cl_v[0][i] = stock_price_cl[i][0]
        stock_price_cl_v[1][i] = stock_price_cl[i][1]
        stock_price_cl_v[2][i] = stock_price_cl[i][2]
        unrate_v[0][i] = unrate[i]

    ### unrate vs stock price
    gUnOp = TGraphAsymmErrors(unrate_v[0],stock_price_op_v[0],unrate_v[1],unrate_v[2],stock_price_op_v[1],stock_price_op_v[2])
    gUnLo = TGraphAsymmErrors(unrate_v[0],stock_price_lo_v[0],unrate_v[1],unrate_v[2],stock_price_lo_v[1],stock_price_lo_v[2])
    gUnHi = TGraphAsymmErrors(unrate_v[0],stock_price_hi_v[0],unrate_v[1],unrate_v[2],stock_price_hi_v[1],stock_price_hi_v[2])
    gUnCl = TGraphAsymmErrors(unrate_v[0],stock_price_cl_v[0],unrate_v[1],unrate_v[2],stock_price_cl_v[1],stock_price_cl_v[2])


    c = TCanvas('c','Plot',512*2,512*2)
    c.Divide(2,2)
    c.Draw()
    c.cd(1)
    gPad.SetGrid(1)
    gUnOp.SetTitle('open')
    gUnOp.SetMarkerStyle(24)
    gUnOp.Draw('APE')
    gPad.Update()

    c.cd(2)
    gPad.SetGrid(1)
    gUnLo.SetTitle('low')
    gUnLo.SetMarkerStyle(24)
    gUnLo.Draw('APE')
    gPad.Update()

    c.cd(3)
    gPad.SetGrid(1)
    gUnHi.SetTitle('high')
    gUnHi.SetMarkerStyle(24)
    gUnHi.Draw('APE')
    gPad.Update()

    c.cd(4)
    gPad.SetGrid(1)
    gUnCl.SetTitle('Close')
    gUnCl.SetMarkerStyle(24)
    gUnCl.Draw('APE')
    gPad.Update()

    input = raw_input('press q to quit or input span (format YYYY-MM) > ')
    if input=='Q' or input=='q' or input=='':
        break
    date_from = input

cur.close()
conn.close()
