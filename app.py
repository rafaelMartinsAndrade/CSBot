import gui
import scrapper

import threading
import time

def iniciarPrograma():
	threadTela = threading.Thread(target=gui.carregarTela, args=(), daemon=True)
	threadTela.start()

	while not gui.window:
		time.sleep(0.1)

	threadAtualizarTela = threading.Thread(target=gui.atualizarTela, args=(), daemon=True)
	threadAtualizarTela.start()

	threadScrapper = threading.Thread(target=iniciarScrapper, args=(), daemon=True)
	threadScrapper.start()

	while threading.active_count() > 1:
		time.sleep(0.5)

def iniciarScrapper():
	while gui.window:
		if gui.scrapper:
			scrapper.iniciarSessao()		
			gui.scrapper = False
	time.sleep(0.5)

if __name__ == '__main__':
	iniciarPrograma()