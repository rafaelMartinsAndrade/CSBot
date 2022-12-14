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
		print('Não foi possível pesquisar as startup\'s!')
		sessao.quit()
		return False

def processarJson():
	try:
		element = WebDriverWait(sessao, 5).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/pre"))
		)
		preStartupsTemp = sessao.find_element("xpath", "/html/body/pre")
		jsonStartupsTemp = json.loads(preStartupsTemp.text)

		print('Total de startup\'s para pesquisa: {0}'.format(jsonStartupsTemp['total']))
		sessao.get("https://startupscanner.com/startups-data?per_page={0}&page=1".format(jsonStartupsTemp['total']))
		element = WebDriverWait(sessao, 120).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/pre"))
		)
		preStartups = sessao.find_element("xpath", "/html/body/pre")

		global arrStartups
		arrStartups = json.loads(preStartups.text)
		sessao.quit()
		print('As startups foram carregadas!')
		verificarExcel()
	except TimeoutException:
		print('Ocorreu um erro na requisição!')
		return False

def verificarExcel():
	excel = pd.read_excel(r"excel.xlsx",'Sheet1',header=1)
	excelStartups = excel["Nome da empresa"]
	excelLinkedin = excel["Linkedin"]

	global qStartups
	qStartups = queue.Queue()

	for arrStartup in arrStartups['data']:
		if not excelStartups.str.contains(arrStartup['name'],regex=False).any():
			qStartups.put(arrStartup)

	print('As startups foram verificadas no excel!')
	
	nOldThreads = threading.active_count()
	global pesquisandoStartups
	pesquisandoStartups = True

	global qStartupsExcel
	qStartupsExcel = queue.Queue()

	while not qStartups.empty():
		nThreads = threading.active_count()
		if nThreads < nOldThreads+5:
			threadPesquisarLinkedin = threading.Thread(target=pesquisarLinkedin, args=(), daemon=True)
			threadPesquisarLinkedin.start()
		time.sleep(0.5)
	
	while pesquisandoStartups:
		time.sleep(0.5)

	print('As startups foram pesquisadas no linkedin!')

	inserirExcel()

def pesquisarLinkedin():
	try:
		arrStartup = qStartups.get()
		#Variáveis de configuração da sessao
		driver_path = 'chromedriver'
		download_dir = "D:\\selenium"
		options = Options()
		# options.add_argument("--headless")
		options.add_argument('--no-sandbox')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.add_argument("--window-size=1400,800")
		options.add_argument('--allow-running-insecure-content')
		options.add_argument('--ignore-certificate-errors')
		# options.add_argument(r"user-data-dir={0}".format(ProfilePath))
		location = ''
		if arrStartup['country'][list(arrStartup['country'])[0]] != '':
			location = arrStartup['country'][list(arrStartup['country'])[0]]
		url = "https://www.linkedin.com/jobs/search/?keywords={0}&location={1}".format(urllib.parse.quote_plus(arrStartup['name']), urllib.parse.quote_plus(location))
		#Chama a função que abre a sessão com as configurações e o driver já pré-definidos
		sessaoTemp = webdriver.Chrome(options=options, executable_path=driver_path)
		#Redireciona a sessão para a url
		sessaoTemp.get(url)
	except:
		print('Ocorreu um erro ao configurar/iniciar a sessao')
	try:
		element = WebDriverWait(sessaoTemp, 30).until(
			EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/nav/div/a[2]"))
		)
		btnLogin = sessaoTemp.find_element("xpath", "/html/body/div[1]/header/nav/div/a[2]")
		btnLogin.click()
		element = WebDriverWait(sessaoTemp, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='username']"))
		)
		inputEmail = sessaoTemp.find_element("xpath", "//*[@id='username']")
		inputEmail.send_keys('rafaelmartinsdandrade@gmail.com')
		inputSenha = sessaoTemp.find_element("xpath", "//*[@id='password']")
		inputSenha.send_keys('tardele11')
		btnLogin = sessaoTemp.find_element("xpath", "//*[@id='organic-div']/form/div[3]/button")
		btnLogin.click()
		element = WebDriverWait(sessaoTemp, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='search-reusables__filters-bar']/div/div/button"))
		)
		btnFiltros = sessaoTemp.find_element("xpath", "//*[@id='search-reusables__filters-bar']/div/div/button")
		btnFiltros.click()
		element = WebDriverWait(sessaoTemp, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//span/div/button"))
		)
		btnTipoFiltro = sessaoTemp.find_element("xpath", "//span/div/button")
		btnTipoFiltro.click()
		element = WebDriverWait(sessaoTemp, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//div/div/ul/li[@class='search-vertical-filter__dropdown-list-item'][4]"))
		)
		liEmpresas = sessaoTemp.find_element("xpath", "//div/div/ul/li[@class='search-vertical-filter__dropdown-list-item'][4]")
		liEmpresas.click()
		spanPesquisar = sessaoTemp.find_element("xpath", "//div/div/button[@class='reusable-search-filters-buttons search-reusables__secondary-filters-show-results-button artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
		spanPesquisar.click()
		strUrlLinkedin = ''
		try:
			element = WebDriverWait(sessaoTemp, 10).until(
				EC.element_to_be_clickable((By.XPATH, "//ul[@class='reusable-search__entity-result-list list-style-none']/li[1]/div/div/div[2]/div[1]/div[1]/div/span/span/a"))
			)
			linkedinStartup = sessaoTemp.find_element("xpath", "//ul[@class='reusable-search__entity-result-list list-style-none']/li[1]/div/div/div[2]/div[1]/div[1]/div/span/span/a")
			strUrlLinkedin = linkedinStartup.get_attribute("href")
			print([arrStartup['name'],strUrlLinkedin])
			linkedinStartup.click()
			try:
				element = WebDriverWait(sessaoTemp, 10).until(
					EC.element_to_be_clickable((By.XPATH, "//a[@class='ember-view']/span"))
				)
				linkedinStartup = sessaoTemp.find_element("xpath", "//a[@class='ember-view']/span")
				funcionariosStartup = linkedinStartup.text
				if int(funcionariosStartup.split(' ')[3]) >= 10:
					qStartupsExcel.put([arrStartup['name'],strUrlLinkedin])
					print('A startup {0} tem mais de 10 funcionarios'.format(arrStartup['name']))
				else:
					qStartupsExcel.put([arrStartup['name'],'-'])
					print('A startup {0} tem menos de 10 funcionarios'.format(arrStartup['name']))
			except TimeoutException:
			qStartupsExcel.put([arrStartup['name'],'-'])
			print('Não achou a quantidade de funcionarios da startup {0}'.format(arrStartup['name']))
		except TimeoutException:
			qStartupsExcel.put([arrStartup['name'],'-'])
			print('Não achou a startup {0}'.format(arrStartup['name']))
	except:
		qStartups.put(arrStartup)
		print("Ocorreu um erro ao pesquisar a Startup {0}".format(arrStartup['name']))
	if qStartups.empty():
		pesquisandoStartups = False
	return True

def inserirExcel():
	while not qStartupsExcel.empty():
		arrStartup = qStartupsExcel.get()
		print(arrStartup)

if __name__ == '__main__':
	iniciarSessao()