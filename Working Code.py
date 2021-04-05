# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:00:41 2021

@author: Kyle Kullander
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 10:44:31 2021

@author: Kyle Kullander
"""

# old fashion example
## import Python packages
from io import BytesIO
import os
from os import path
from zipfile import ZipFile
import pandas as pd
import numpy as np
import requests
import sqlite3
from sqlite3 import Error
import urllib3


#Set up working folder
WorkingDir="c:\\Edgar\\"

#%% download the crawler.Inx from Edgar
## 1. feed crawler.Idx URL
master_url="https://www.sec.gov/Archives/edgar/full-index/2021/QTR1/master.idx"
master=pd.read_csv(master_url, skiprows=10, names=['CIK', 'Company Name', 'Form Type', 'Date Filed', 'Filename'], sep='|', engine='python', parse_dates=True)
print(master.head())


#%% 2. take care of the error
master = master[-master['CIK'].str.contains("---")]
print(master.head())
#%%
## 3. drop rows with missing value
master = master.dropna(axis=0,subset=['CIK','Form Type','Filename'])

#%% #1. Filter out the NCSR/4 forms for MFs and Insider Transactions
NCSR=master[master['Form Type'].str.fullmatch('N-CSR')]
NCSR.reset_index(inplace=True,drop=True)
print(NCSR.head())

#%% 4. Save the N-CSR list file as excel
outfile=WorkingDir+"data\\NCSR_2021_QTR1.xlsx"
NCSR.to_excel(outfile,sheet_name='N-CSR',index=False)

#%% Form 4
form=master[master['Form Type'].str.fullmatch('4')]
form.reset_index(inplace=True,drop=True)
print(form.head())

#%% 4. Save the Insider list file as excel
outfile=WorkingDir+"data\\Form4_2021_QTR1.xlsx"
form.to_excel(outfile,sheet_name='Form 4',index=False)#%%
