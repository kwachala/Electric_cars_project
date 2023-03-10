import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils import *
from tkinter import messagebox
from PIL import ImageTk, Image
from backend import *
from main import *

start = tk.Tk()

start = create_window(start, 'BEV for You!', 600, 600, 'bev.ico')
start.resizable(False, False)
bg = tk.PhotoImage(master=start, file="bg.png")
bgl = tk.Label(start, image=bg)
bgl.place(x=0, y=0, relwidth=1, relheight=1)

set_grid(start, 2, 10)

next_button = tk.Button(start, text='Dalej', command=lambda: check_errors())

start_text1 = tk.Label(start, text='Zaznacz w skali od 1 do 9 jak ważny jest dany parametr samochodu',
                       font=("Calibri", "16"))
start_text2 = tk.Label(start, text='Cena', font=("Calibri", "16"))
start_text3 = tk.Label(start, text='Zasięg', font=("Calibri", "16"))
start_text4 = tk.Label(start, text='Prędkość maksymalna', font=("Calibri", "16"))
start_text5 = tk.Label(start, text='Przyśpieszenie od 0 do 100km/h', font=("Calibri", "16"))

textbox_price, textbox_range = set_entry(start)
textbox_topspeed, textbox_zero_to_100 = set_entry(start)

start_text1.grid(columnspan=2, row=0)
start_text2.grid(columnspan=2, row=1)
textbox_price.grid(columnspan=2, row=2)
start_text3.grid(columnspan=2, row=3)
textbox_range.grid(columnspan=2, row=4)
start_text4.grid(columnspan=2, row=5)
textbox_topspeed.grid(columnspan=2, row=6)
start_text5.grid(columnspan=2, row=7)
textbox_zero_to_100.grid(columnspan=2, row=8)
next_button.grid(columnspan=2, row=9)


def get_parameters():
    price_parameter = int(textbox_price.get())
    range_parameter = int(textbox_range.get())
    topspeed_parameter = int(textbox_topspeed.get())
    zero_to_100_parameter = int(textbox_zero_to_100.get())

    return [price_parameter, range_parameter, topspeed_parameter, zero_to_100_parameter]


def check_errors():
    if textbox_price.get().isdigit() and textbox_range.get().isdigit() and textbox_topspeed.get().isdigit() and textbox_zero_to_100.get().isdigit():
        price_parameter = int(textbox_price.get())
        range_parameter = int(textbox_range.get())
        topspeed_parameter = int(textbox_topspeed.get())
        zero_to_100_parameter = int(textbox_zero_to_100.get())

        if 0 < price_parameter < 10 and 0 < range_parameter < 10 and 0 < topspeed_parameter < 10 and 0 < zero_to_100_parameter < 10:
            start.withdraw()
            main_window(get_parameters(), start)
        else:
            messagebox.showwarning('Błąd', 'Wprowadź poprawne dane!')
    else:
        messagebox.showwarning('Błąd', 'Wprowadź poprawne dane!')


def on_closing_start():
    if messagebox.askokcancel("Zamknij", "Czy na pewno chcesz wyjść?"):
        start.destroy()


start.protocol("WM_DELETE_WINDOW", on_closing_start)
start.mainloop()
