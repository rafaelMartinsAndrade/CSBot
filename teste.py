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

# excel = pd.read_excel(r"excel.xlsx",'Sheet1',header=1)

# # for linha in excel:
# for arrEmpresas in excel['Nome da empresa']:
# 	print(arrEmpresas)

# wb = openpyxl.load_workbook("excel.xlsx")
# ws = wb.active
# while not qTeste.empty():
# 	arrTeste = qTeste.get()
# 	ws.append(arrTeste)
# 	wb.save('excel.xlsx')

# wb = load_workbook(r"NF's2.xlsx")
# sheets = wb.sheetnames
# sheet1 = wb[sheets[0]]
# j = i+2
# sheet1.cell(row = j, column = 19).value = "Cancelada"
# wb.save("excel.xlsx")

# empresa = excel["Linkedin"]