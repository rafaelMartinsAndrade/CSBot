#Imports necessários
import time
import os
from datetime import datetime

#Imports do selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

#Imports do pyautogui
from pyautogui import *
import pyautogui
import keyboard
import random
import win32api, win32con

# Imports do Tkinter
import tkinter as tk

def carregarTela():
    print('Versão do Robo: 2.0 Beta')
    global t, inputInicial, inputFinal, inputMsg

    t = time.localtime()
    input = {'width' : 30,
             'height' : 1}

    window = tk.Tk(className="\\CSBot - VKDIGITAL")
    window.configure(bg="black")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    titleLb = tk.Label(window, text="Bem vindo!", bg="black", fg="white")
    titleLb.grid(column=0, columnspan=2, row=0, ipadx=0, pady=0, sticky="nsew")

    resultButton = tk.Button(window, text="Processar Startup's", command=carregarContatos, width=60)
    resultButton.grid(column=0, columnspan=2, row=6, padx=10, pady=10, sticky=tk.W)

    # list_items = tk.Variable(value=items)
    #     listbox = tk.Listbox(
    #     container,
    #     height,
    #     listvariable=list_items
    # )

    window.mainloop()

def iniciaSessao():
    #Variáveis de configuração da sessao
    driver_path = 'chromedriver'
    download_dir = "D:\\selenium"
    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--window-size=1400,800")

    global sessao 
    #Chama a função que abre a sessão com as configurações e o driver já prédefinidos
    sessao = webdriver.Chrome(options=options, executable_path=driver_path)
    #Redireciona a sessão para a url
    sessao.get("https://startupscanner.com/")
    # time.sleep(1)

def carregarContatos():
    iniciaSessao()

carregarTela()

