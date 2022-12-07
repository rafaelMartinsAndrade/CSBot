import gui
import scrapper

import threading
import time
import queue

def iniciarPrograma():
	threadTela = threading.Thread(target=gui.carregarTela, args=(), daemon=True)
	threadTela.start()

	while not gui.window:
		time.sleep(0.1)

	threadAtualizarTela = threading.Thread(target=gui.atualizarTela, args=(), daemon=True)
	threadAtualizarTela.start()

	threadScrapper = threading.Thread(target=iniciarScrapper, args=(), daemon=True)
	threadScrapper.start()

	# threadListarThreads = threading.Thread(target=listarThreads, args=(), daemon=True)
	# threadListarThreads.start()

	while gui.window:
		time.sleep(0.5)

	scrapper.sairSessao()

def iniciarScrapper():
	while gui.window:
		if gui.scrapper:
			scrapper.iniciarSessao()
			# try:
			# 	scrapper.iniciarSessao()
			# except:
			# 	print('Ocorreu um erro!')
			gui.scrapper = False

def listarThreads():
	while gui.window:
		for thread in threading.enumerate(): 
			print(thread.name)
		time.sleep(0.5)

if __name__ == '__main__':
	iniciarPrograma()