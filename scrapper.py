#Imports necessários
import time
import threading
import pandas
import queue
# from datetime import datetime
# import os

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

from pathlib import Path

global ProfilePath
ProfilePath = Path(__file__).parent / Path("./SeleniumProfile")

def iniciarSessao():
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
	options.add_argument(r"user-data-dir={0}".format(ProfilePath))
	global sessao
	#Chama a função que abre a sessão com as configurações e o driver já prédefinidos
	sessao = webdriver.Chrome(options=options, executable_path=driver_path)
	#Redireciona a sessão para a url
	sessao.get(r"https://startupscanner.com/")
	try:
		logar()
	except NoSuchWindowException:
		print('A sessão foi encerrada!')

def logar():
	print('Fazer login')
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
			element = WebDriverWait(sessao, 1).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='user-dropdown']/img"))
			)
			# print('O usuário já estava logado ao sistema!')
			acessarMapas()
		except TimeoutException:
			print('Ocorreu um erro ao tentar logar no site!')
	except NoSuchElementException:
		print('Não foi possível acessar os mapas de startup\'s!')

def acessarMapas():
	try:
		element = WebDriverWait(sessao, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)
		element = WebDriverWait(sessao, 3).until(
			EC.element_to_be_clickable((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)

		while True:
			try:
				linkMenuMapa = sessao.find_element("xpath", "//*[@id='navbarMenu']/ul/li[2]/a")
				linkMenuMapa.click()
				break
			except ElementClickInterceptedException:
				time.sleep(0.5)

		element = WebDriverWait(sessao, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)
		processarStartups()
	except TimeoutException:
		print('Não foi possível acessar os mapas de startup\'s!')
	except NoSuchElementException:
		print('Não foi possível acessar os mapas de startup\'s!')

def processarStartups():

	global qCategorias
	qCategorias = queue.Queue()

	global qSubCategorias
	qSubCategorias = queue.Queue()

	sessao.execute_script("window.scrollBy(0,1000);")
	element = WebDriverWait(sessao, 5).until(
		EC.element_to_be_clickable((By.XPATH, "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[1]/a"))
	)
	sessao.execute_script("window.scrollBy(0,1000);")
	element = WebDriverWait(sessao, 5).until(
		EC.element_to_be_clickable((By.XPATH, "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[10]/a"))
	)

	processandoCategorias = True;
	i = 1

	while processandoCategorias:
		try:
			linkCategoria = sessao.find_element("xpath", "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[{0}]/a".format(i))
			href = linkCategoria.get_attribute("href")
			nomeCategoria = sessao.find_element("xpath", "//*[@id='mapasMain']/div/div/div/section/div[3]/div/div/div[{0}]/a/div/h5".format(i))
			nome = nomeCategoria.text
			print([nome, href])
			qCategorias.put([nome, href])
		except NoSuchElementException:
			processandoCategorias = False
		i += 1
	print('Terminou!')
	sessao.quit()
	# global startups
	# startups = True

	# threadScrapper = threading.Thread(target=listarSubCategorias, args=(), daemon=True)
	# threadScrapper.start()


# def listarSubCategorias()


def sairSessao():
	startups = False
	if sessao:
		sessao.quit()

if __name__ == '__main__':
	iniciarSessao()