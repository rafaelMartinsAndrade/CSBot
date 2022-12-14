#Imports necessários
import time
import threading
import pandas
import queue
import os
import json
from datetime import datetime

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
	# options.add_argument("--headless")
	# options.add_argument('--no-sandbox')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("--window-size=1400,800")
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--ignore-certificate-errors')
	# options.add_argument(r"user-data-dir={0}".format(ProfilePath))
	global sessao
	#Chama a função que abre a sessão com as configurações e o driver já prédefinidos
	sessao = webdriver.Chrome(options=options, executable_path=driver_path)
	#Redireciona a sessão para a url
	sessao.get(r"https://startupscanner.com/startups-data?per_page=1&page=1")
	logar()
	return True

	try:
		logar()
	except NoSuchWindowException:
		print('A sessão foi encerrada!')
		return False

	global fimScrapper
	fimScrapper = datetime.now()
	fimScrapper = fimScrapper.strftime("%H:%M:%S")
	print(inicioScrapper)
	print(fimScrapper)

	print('Inicio: {0}, Fim: {1}'.format(inicioScrapper, fimScrapper))

def logar():
	try:
		element = WebDriverWait(sessao, 1).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='btn-login'][contains(@class, 'btnPink')]"))
		)
		btnMenuLogin = sessao.find_element("xpath", "//*[@id='btn-login'][contains(@class, 'btnPink')]")
		btnMenuLogin.click()
		element = WebDriverWait(sessao, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='emailInput']"))
		)
		inputEmail = sessao.find_element("xpath", "//*[@id='emailInput']")
		inputEmail.send_keys('rafaelmartinsdandrade@gmail.com')
		inputSenha = sessao.find_element("xpath", "//*[@id='passwordInput']")
		inputSenha.send_keys('senhaStartupScanner')
		btnLogin = sessao.find_element("xpath", "//*[@id='login-button']")
		btnLogin.click()
		acessarMapas()
	except TimeoutException:
		try:
			element = WebDriverWait(sessao, 3).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='user-dropdown']/img"))
			)
			acessarMapas()
		except TimeoutException:
			print('Ocorreu um erro ao tentar logar no site!')
			sessao.quit()
			return False
	except NoSuchElementException:
		print('Não foi possível acessar os mapas de startup\'s!')
		sessao.quit()
		return False

def acessarMapas():
	try:
		element = WebDriverWait(sessao, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)
		element = WebDriverWait(sessao, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)

		while True:
			try:
				linkMenuMapa = sessao.find_element("xpath", "//*[@id='navbarMenu']/ul/li[2]/a")
				linkMenuMapa.click()
				break
			except (ElementClickInterceptedException, StaleElementReferenceException):
				time.sleep(0.5)

		element = WebDriverWait(sessao, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)
		processarDados()
	except TimeoutException:
		print('Não foi possível acessar os mapas de categorias\'s! ERR: 00001')
		sessao.quit()
	except NoSuchElementException:
		print('Não foi possível acessar os mapas de categorias\'s! ERR: 00002')
		sessao.quit()

def processarDados():
	try:
		element = WebDriverWait(sessao, 5).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/section[1]/div/div/div/div/h1"))
		)
		sessao.execute_script("window.scrollBy(0,1000);")
		time.sleep(1)
		element = WebDriverWait(sessao, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[1]/a"))
		)
		sessao.execute_script("window.scrollBy(0,1000);")
		element = WebDriverWait(sessao, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[13]/a"))
		)
	except TimeoutException:
		print("Nenhuma categoria foi encontrada!")
		sessao.quit()
		return False

	global qCategorias
	qCategorias = queue.Queue()
	processandoCategorias = True;
	i = 1

	print('Processando Categorias')
	while processandoCategorias:
		try:
			linkCategoria = sessao.find_element("xpath", "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[{0}]/a".format(i))
			href = linkCategoria.get_attribute("href")
			nomeCategoria = sessao.find_element("xpath", "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[{0}]/a/div/h5".format(i))
			nome = nomeCategoria.text
			qCategorias.put([nome, href])
		except NoSuchElementException:
			processandoCategorias = False
		i += 1

	sessao.quit()

	global arrSessoes
	global qSubCategorias
	arrSessoes = []
	qSubCategorias = queue.Queue()
	nOldThreads = threading.active_count()

	print('Processando SubCategorias')

	while not qCategorias.empty():
		nThreads = threading.active_count()
		if nThreads < nOldThreads+5:
			threadListarSubCategoria = threading.Thread(target=listarSubCategorias, args=(), daemon=True)
			threadListarSubCategoria.start()
		time.sleep(0.5)

	while True:
		nThreads = threading.active_count()
		if nThreads > nOldThreads:
			time.sleep(0.5)
		else:
			break

	print('Processando Startup\'s')

	global qStartups
	qStartups = queue.Queue()

	qStartups = queue.Queue()
	nOldThreads = threading.active_count()

	while not qSubCategorias.empty():
		nThreads = threading.active_count()
		if nThreads < nOldThreads+10:
			threadListarSubCategoria = threading.Thread(target=processarStartups, args=(), daemon=True)
			threadListarSubCategoria.start()
		time.sleep(0.5)

	print('Terminou')

def listarSubCategorias():
	arrCategoria = qCategorias.get()
	#Variáveis de configuração da sessao
	driver_path = 'chromedriver'
	download_dir = "D:\\selenium"
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("--window-size=1400,800")
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--ignore-certificate-errors')
	# options.add_argument(r"user-data-dir={0}".format(ProfilePath))
	#Chama a função que abre a sessão com as configurações e o driver já prédefinidos
	try:
		sessaoTemp = webdriver.Chrome(options=options, executable_path=driver_path)
		arrSessoes.append(sessaoTemp)
		sessaoTemp.get(arrCategoria[1])
	except:
		qCategorias.put(arrCategoria)
		return False
	#Redireciona a sessão para a url
	sessaoTemp.execute_script("window.scrollBy(0,1000);")
	i = 1
	flagSubCategorias = True
	while flagSubCategorias:
		try:
			if i % 12 == 0:
				sessaoTemp.execute_script("window.scrollBy(0,1000);")
			element = WebDriverWait(sessaoTemp, 5).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='categories']/div[2]/div/div/div[{0}]/a".format(i)))
			)
			linkSubCategoria = sessaoTemp.find_element("xpath", "//*[@id='categories']/div[2]/div/div/div[{0}]/a".format(i))
			href = linkSubCategoria.get_attribute("href")
			nomeSubCategoria = sessaoTemp.find_element("xpath", "//*[@id='categories']/div[2]/div/div/div[{0}]/a/div/div[2]/h5".format(i))
			nome = nomeSubCategoria.text
			qSubCategorias.put([nome, href])
			i+=1
		except TimeoutException:
			flagSubCategorias = False
		except:
			print('Ocorreu um erro na categoria {0}'.format(arrCategoria[0]))
			sessaoTemp.quit()
			flagSubCategorias = False
	sessaoTemp.quit()
	return True

def processarStartups():
	arrSubCategoria = qSubCategorias.get()
	#Variáveis de configuração da sessao
	driver_path = 'chromedriver'
	download_dir = "D:\\selenium"
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("--window-size=1400,800")
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--ignore-certificate-errors')
	# options.add_argument(r"user-data-dir={0}".format(ProfilePath))
	#Chama a função que abre a sessão com as configurações e o driver já prédefinidos
	try:
		sessaoTemp = webdriver.Chrome(options=options, executable_path=driver_path)
		#Redireciona a sessão para a url
		sessaoTemp.get(arrSubCategoria[1])
		arrSessoes.append(sessaoTemp)
	except:
		qSubCategorias.put(arrSubCategoria)
		return False
	try:
		element = WebDriverWait(sessaoTemp, 5).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='emailInput']"))
		)
		inputEmail = sessaoTemp.find_element("xpath", "//*[@id='emailInput']")
		inputEmail.send_keys('rafaelmartinsdandrade@gmail.com')
		inputSenha = sessaoTemp.find_element("xpath", "//*[@id='passwordInput']")
		inputSenha.send_keys('senhaStartupScanner')
		btnLogin = sessaoTemp.find_element("xpath", "//*[@id='login-button']")
		btnLogin.click()
		element = WebDriverWait(sessaoTemp, 5).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/section[1]/div/div/div/div/h1"))
		)
	except:
		print("Ocorreu um erro ao processar as Startup's")
	sessaoTemp.execute_script("window.scrollBy(0,600);")
	i = 1
	flagStartups = True
	while flagStartups:
		try:
			if i % 9 == 0:
				sessaoTemp.execute_script("window.scrollBy(0,1500);")
			element = WebDriverWait(sessaoTemp, 5).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='categories']/div[3]/div/div/div[{0}]/div".format(i)))
			)
			nomeStartup = sessaoTemp.find_element("xpath", "//*[@id='categories']/div[3]/div/div/div[{0}]/div/div[1]/div[1]/div[2]/span/h5".format(i))
			nome = nomeStartup.text
			qStartups.put(nome)
			i+=1
		except TimeoutException:
			flagStartups = False
		except:
			print('Ocorreu um erro na subcategoria {0}'.format(arrSubCategoria[0]))
			sessaoTemp.quit()
			flagStartups = False
	print('Startup\'s armazenadas: {0}'.format(qStartups.qsize()))
	sessaoTemp.quit()
	return True
	
if __name__ == '__main__':
	iniciarSessao()