
import gui

#Imports necessários
import time
import threading
import queue
import os
import json
import urllib.parse
from datetime import datetime

# Imports do xlsx
import pandas as pd
import numpy as np
from openpyxl import workbook
from openpyxl import load_workbook


# import keyboard
# import random
# import win32api, win32con

#Imports do selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException

from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

global ProfilePath
ProfilePath = Path(__file__).parent / Path("./SeleniumProfile")

def iniciarSessao():
	global inicioScrapper
	inicioScrapper = datetime.now()
	inicioScrapper = inicioScrapper.strftime("%H:%M:%S")
	print('Inicio: {0}, Fim: -'.format(inicioScrapper))

	#Variáveis de configuração da sessao
	driver_path = 'chromedriver'
	download_dir = "D:\\selenium"
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("--window-size=1000,800")
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument(r"user-data-dir={0}".format(ProfilePath))
	global sessao
	#Chama a função que abre a sessão com as configurações e o driver já prédefinidos
	sessao = webdriver.Chrome(options=options, executable_path=driver_path)
	#Redireciona a sessão para a url
	sessao.get(r"https://startupscanner.com/startups-data?per_page=1&page=1")

	logar()

	global fimScrapper
	fimScrapper = datetime.now()
	fimScrapper = fimScrapper.strftime("%H:%M:%S")
	print('Inicio: {0}, Fim: {1}'.format(inicioScrapper, fimScrapper))

def logar():
	try:
		gui.atualizarLog('Verificando a quantidade de startup\'s!')
		element = WebDriverWait(sessao, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='emailInput']"))
		)
		inputEmail = sessao.find_element("xpath", "//*[@id='emailInput']")
		inputEmail.send_keys('rafaelmartinsdandrade@gmail.com')
		inputSenha = sessao.find_element("xpath", "//*[@id='passwordInput']")
		inputSenha.send_keys('senhaStartupScanner')
		btnLogin = sessao.find_element("xpath", "//*[@id='login-button']")
		btnLogin.click()
		processarJson()
	except TimeoutException:
		processarJson()
	except NoSuchElementException:
		gui.atualizarLog('Não foi possível pesquisar as startup\'s!')
		sessao.quit()
		return False

def processarJson():
	try:
		element = WebDriverWait(sessao, 5).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/pre"))
		)
		preStartupsTemp = sessao.find_element("xpath", "/html/body/pre")
		jsonStartupsTemp = json.loads(preStartupsTemp.text)

		gui.atualizarLog('Pesquisando {0} startup\'s!'.format(jsonStartupsTemp['total']))
		sessao.get("https://startupscanner.com/startups-data?per_page={0}&page=1".format(jsonStartupsTemp['total']))
		element = WebDriverWait(sessao, 120).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/pre"))
		)
		preStartups = sessao.find_element("xpath", "/html/body/pre")

		global arrStartups
		arrStartups = json.loads(preStartups.text)
		sessao.quit()
		gui.atualizarLog('As startup\'s foram carregadas!')
		verificarExcel()
	except TimeoutException:
		gui.atualizarLog('Ocorreu um erro na requisição!')
		return False

def verificarExcel():
	excel = pd.read_excel(r"excel.xlsx",'Sheet1',header=1)
	excelStartups = excel["Nome da empresa"]
	excelLinkedin = excel["Linkedin"]

	global qStartupsExcel
	qStartupsExcel = queue.Queue()

	gui.atualizarLog('Verificando 1 de {0}'.format(arrStartups['total']))

	iStartupsExcel = 0
	for arrStartup in arrStartups['data']:
		if not excelStartups.str.contains(arrStartup['name'],regex=False).any():
			qStartups.put(arrStartup)
		iStartupsExcel += 1
		gui.atualizarLog('Verificando {0} de {1}'.format(iStartupsExcel, arrStartups['total']))


	gui.atualizarLog('As startup\'s foram verificadas no excel!')
	
	global inserindoStartups
	inserindoStartups = True

	inserirExcel()

	while inserindoStartups:
		time.sleep(0.5)

	gui.atualizarLog('{0} startup\'s foram inseridas no excel!'.format(arrStartups['total']))

def inserirExcel():
	global pesquisandoStartups

	while not qStartupsExcel.empty() or pesquisandoStartups:
		if qStartupsExcel.empty():
			time.sleep(1)
		else:
			arrStartup = qStartupsExcel.get()
			try:
				excel = pd.ExcelFile("excel.xlsx")
				excel = excel.parse('Sheet1', skiprows=1, index_col=None, na_values=['NA'])
				arrStartups = excel['Nome da empresa']
				i = 0
				for startup in arrStartups:
					try:
						m.isnan(float(startup))
						break
					except:
						i += 1

				wb = load_workbook("excel.xlsx")
				sheets = wb.sheetnames
				sheet1 = wb[sheets[0]]
				j = i+3
				sheet1.cell(row = j, column = 1).value = arrStartup[0]
				wb.save("excel.xlsx")
			except:
				qStartupsExcel.put(arrStartup)
	inserindoStartups = False

if __name__ == '__main__':
	iniciarSessao()