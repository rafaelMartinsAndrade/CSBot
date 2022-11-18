#Imports necessários
import time
# from datetime import datetime
# import os
from threading import Thread
# import pandas
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

# Imports do TKDesigner
from pathlib import Path
from tkinter import Tk as tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def carregarTela():
    global window
    window = tk()

    window.geometry("550x235")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 235,
        width = 550,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        550.0,
        235.0,
        fill="#A936E9",
        outline="")

    canvas.create_text(
        76.0,
        33.0,
        anchor="nw",
        text="CSBot - VKDIGITAL",
        fill="#FFFFFF",
        font=("Nunito Black", 18 * -1)
    )

    canvas.create_text(
        24.0,
        211.0,
        anchor="nw",
        text="By Rafael Martins",
        fill="#FFFFFF",
        font=("Nunito Black", 10 * -1)
    )

    canvas.create_rectangle(
        261.0,
        11.0,
        532.0,
        223.0,
        fill="#FFFFFF",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        39.0,
        45.0,
        image=image_image_1
    )

    canvas.create_text(
        278.0,
        35.0,
        anchor="nw",
        text="Scanner - Startup’s",
        fill="#5A5A5A",
        font=("Nunito Bold", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: acessarMapas(),
        relief="flat"
    )
    button_1.place(
        x=278.0,
        y=175.0,
        width=243.0,
        height=31.0
    )
    window.resizable(False, False)
    window.mainloop()
	# thread = threading.Thread(target=atualizarTela(), args=(), daemon=True)
	# thread.start()

def atualizarTela():
	while True:
		if window: 
			print('update')
			# window.update()
			time.sleep(1)

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
	# options.add_argument(r"user-data-dir=C:\SeleniumProfile")
	global sessao
	#Chama a função que abre a sessão com as configurações e o driver já prédefinidos
	sessao = webdriver.Chrome(options=options, executable_path=driver_path)
	#Redireciona a sessão para a url
	sessao.get(r"https://startupscanner.com/")
	# time.sleep(1)

def acessarMapas():
	print('F')
	iniciarSessao()
	print('Iniciou sessão')
	try:
		element = WebDriverWait(sessao, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)
		linkMenuMapa = sessao.find_element("xpath", "//*[@id='navbarMenu']/ul/li[2]/a")
		linkMenuMapa.click()
		element = WebDriverWait(sessao, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='navbarMenu']/ul/li[2]/a"))
		)
		while():
			sessao.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	except TimeoutException:
		print('Não foi possível acessar os mapas de startup\'s!')
	except NoSuchElementException:
		print('Não foi possível acessar os mapas de startup\'s!')

	# sessao.quit()

if __name__ == '__main__':
	global app
	global attTela

	attTela = Thread(target=atualizarTela, args=(), daemon=True)
	attTela.start()

	carregarTela()

	while True:
		time.sleep(1)
	