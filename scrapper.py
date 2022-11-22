#Imports necessários
import time
import threading
import pandas
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
			print('O usuário já estava logado ao sistema!')
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
		sessao.execute_script("window.scrollBy(0,5000);")
		time.sleep(1)
		sessao.execute_script("window.scrollBy(0,5000);")
		time.sleep(10)
		sessao.execute_script("window.scrollBy(0,0);")
	except TimeoutException:
		print('Não foi possível acessar os mapas de startup\'s!')
	except NoSuchElementException:
		print('Não foi possível acessar os mapas de startup\'s!')

if __name__ == '__main__':
	iniciarSessao()