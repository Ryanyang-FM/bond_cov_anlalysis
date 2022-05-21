# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:10:01 2022

@author: RyanPC
"""

import akshare as ak
import pandas as pd
import numpy as np
import tushare as ts
import datetime
from openpyxl import load_workbook
from scipy.stats import rankdata
import baostock as bs
import math

bond_cov_comparison_df = ak.bond_cov_comparison()
bond_cov_comparison_df = bond_cov_comparison_df.set_index('正股代码')
bond_cov_comparison_df = bond_cov_comparison_df[bond_cov_comparison_df['转债最新价']!='-']
bond_cov_comparison_df = bond_cov_comparison_df[bond_cov_comparison_df['转债最新价']<130]
bond_cov_comparison_df = bond_cov_comparison_df[bond_cov_comparison_df['转股溢价率']<30]
bond_cov_comparison_df['PE'] = 0
bond_cov_comparison_df['Net_Salesgrowth'] = 0
bond_cov_comparison_df['peg'] =np.zeros(bond_cov_comparison_df.shape[0])
a = np.nan
#获取正股相关信息
for stock in bond_cov_comparison_df.index:
    stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol=stock)
    stock_financial_analysis_indicator_df =stock_financial_analysis_indicator_df[stock_financial_analysis_indicator_df['净利润增长率(%)']!= '--']
    stock_a_lg_indicator_df = ak.stock_a_lg_indicator(symbol=stock)
    stock_a_lg_indicator_df = stock_a_lg_indicator_df[stock_a_lg_indicator_df['pe']>0]
    pe = stock_a_lg_indicator_df['pe'].iloc[0]
    Net_Salesgrowth = float(stock_financial_analysis_indicator_df['净利润增长率(%)'].iloc[0])
    peg = float(pe / Net_Salesgrowth)
    bond_cov_comparison_df['PE'][stock] = pe
    bond_cov_comparison_df['Net_Salesgrowth'][stock] = Net_Salesgrowth
    bond_cov_comparison_df['peg'][stock] = peg
    print(stock,pe,Net_Salesgrowth,peg)