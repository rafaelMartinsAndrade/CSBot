import app

import time
import queue
import pandas

#Imports para o TKinter
from pathlib import Path
from tkinter import Tk as tk, Canvas, Entry, Text, Button, PhotoImage

global window
window = False

global scrapper
scrapper = False

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def carregarTela():
	global window
	global scrapper
	
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
	    command=lambda: globals().update(scrapper=True),
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

	window = False

def atualizarTela():
	while window:
		window.update()
		time.sleep(1)

if __name__ == '__main__':
	carregarTela()