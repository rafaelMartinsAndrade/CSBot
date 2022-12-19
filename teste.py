import openpyxl
import math as m
from openpyxl import workbook
from openpyxl import load_workbook

import pandas as pd
import queue as q

qTeste = q.Queue()

qTeste.put(['teste', '1'])
qTeste.put(['teste', '2'])
qTeste.put(['teste', '3'])
qTeste.put(['teste', '4'])
qTeste.put(['teste', '5'])
qTeste.put(['teste', '6'])



excel = pd.ExcelFile("excel.xlsx")
excel = excel.parse('Sheet1', skiprows=1, usecols = ['Nome da empresa'], index_col=None, na_values=['NA'])
arrExcelStartups = excel['Nome da empresa']
arrTemp = arrExcelStartups[1:len(arrExcelStartups)]
