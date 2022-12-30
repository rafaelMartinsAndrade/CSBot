from collections import defaultdict
import urllib.parse
import openpyxl
import math as m
from openpyxl import workbook
from openpyxl import load_workbook

import pandas as pd
import queue as q

qTeste = q.Queue()
qTeste.put("+Mu")
print(qTeste.get())