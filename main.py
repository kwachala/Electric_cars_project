import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils import *
from tkinter import messagebox
from PIL import ImageTk, Image
from backend import *


def create_environment_window(efficiency):
    environment_window = tk.Toplevel()
    environment_window = create_window(environment_window, "Best car", 700, 200, 'bev.ico')
    environment_window.resizable(False, False)
    set_grid(environment_window, 2, 4)
    efficiency = int(efficiency)
    emissivity = get_emissivity(efficiency)

    first_text = tk.Label(environment_window,
                          text='Dla wyszukanego samochodu emisyjność wynosi: ' + str(emissivity[0]) + 'g CO2/km',
                          font=("Calibri", "14"))
    second_text = tk.Label(environment_window,
                          text='Dla porównywalnego samochodu na benzynę emisyjność wynosi: ' + str(emissivity[1]) + 'g CO2/km',
                          font=("Calibri", "14"))
    third_text = tk.Label(environment_window,
                          text='Dla porównywalnego samochodu na diesel emisyjność wynosi: ' + str(emissivity[2]) + 'g CO2/km',
                          font=("Calibri", "14"))
    assumptions_text = tk.Label(environment_window,
                          text='Przy założeniach, że wszystkie te samochody są ładowane ładowarką domową (3,7kW) oraz, że udział OZE w produkcji energii elektrycznej stanowi 16%',
                          font=("Calibri", "8"))

    first_text.grid(columnspan=2, row=0, sticky=tk.EW)
    second_text.grid(columnspan=2, row=1, sticky=tk.EW)
    third_text.grid(columnspan=2, row=2, sticky=tk.EW)
    assumptions_text.grid(columnspan=2, row=3, sticky=tk.EW)

def last_step(efficiency):
    create_environment_window(efficiency)


def create_final_window(best):
    global carphoto1

    bailout = best[-1]

    new_window = tk.Toplevel()
    new_window = create_window(new_window, "Best car", 600, 700, 'bev.ico')
    new_window.resizable(False, False)
    if type(best) == str:
        set_grid(new_window, 2, 2)
        nocar = tk.Label(new_window, text=best, font=("Calibri", "16"))
        back_button = tk.Button(new_window, text='Cofnij', command=new_window.destroy)

        nocar.grid(columnspan=2, row=0, sticky=tk.EW)
        back_button.grid(columnspan=2, row=1)

    else:
        set_grid(new_window, 2, 16)
        carphoto1 = ImageTk.PhotoImage(Image.open(f"car_photos/{best[0]}.jpg"))
        carlabel1 = tk.Label(new_window, image=carphoto1)

        if best[4] == 'All wheel':
            best[4] = 'Na wszystkie koła'
        elif best[4] == 'Rear wheel':
            best[4] = 'Na tył'
        elif best[4] == 'Front wheel':
            best[4] = 'Na przód'

        if best[6] == 'Hatchback':
            best[6] = 'Kompakt'
        elif best[6] == 'Station':
            best[6] = 'Kombi'
        elif best[6] == 'Cabriolet':
            best[6] = 'Kabriolet'

        carinfo1 = tk.Label(new_window, text='Nazwa: ' + best[0], font=("Calibri", "16"))
        carinfo2 = tk.Label(new_window, text='Pojemność baterii: ' + str(best[1]) + ' kWh', font=("Calibri", "16"))
        carinfo3 = tk.Label(new_window, text='Segment: ' + best[2], font=("Calibri", "16"))
        carinfo4 = tk.Label(new_window, text='Ilość miejsc: ' + str(best[3]), font=("Calibri", "16"))
        carinfo5 = tk.Label(new_window, text='Napęd: ' + best[4], font=("Calibri", "16"))
        print(bailout)
        if bailout == 'Nie':
            carinfo6 = tk.Label(new_window, text='Cena: ' + str(int(best[5] * 4.72)) + 'zł', font=("Calibri", "16"))
            priceinfo = tk.Label(new_window, text='(przy kursie EUR/PLN z dnia 10.11.2022r.)', font=("Calibri", "8"))
        elif bailout == 'Tak' and best[2] == 'N':
            carinfo6 = tk.Label(new_window, text='Cena: ' + str(int(best[5] * 4.72) - 70000) + 'zł',
                                font=("Calibri", "16"))
            priceinfo = tk.Label(new_window,
                                 text='(przy kursie EUR/PLN z dnia 10.11.2022r. z uwzględnieniem maksymalnego możliwego dofinansowania)',
                                 font=("Calibri", "8"))
        else:
            carinfo6 = tk.Label(new_window, text='Cena: ' + str(int(best[5] * 4.72) - 27000) + 'zł',
                                font=("Calibri", "16"))
            priceinfo = tk.Label(new_window,
                                 text='(przy kursie EUR/PLN z dnia 10.11.2022r. z uwzględnieniem maksymalnego możliwego dofinansowania)',
                                 font=("Calibri", "8"))

        carinfo7 = tk.Label(new_window, text='Nadwozie: ' + best[6], font=("Calibri", "16"))
        carinfo8 = tk.Label(new_window, text='0-100: ' + str(best[7]) + ' s', font=("Calibri", "16"))
        carinfo9 = tk.Label(new_window, text='Maksymalna prędkość: ' + str(best[8]) + ' km/h', font=("Calibri", "16"))
        carinfo10 = tk.Label(new_window, text='Zasięg: ' + str(best[9]) + ' km', font=("Calibri", "16"))
        carinfo11 = tk.Label(new_window, text='Efektywność: ' + str(best[10]) + ' Wh/km', font=("Calibri", "16"))
        carinfo12 = tk.Label(new_window, text='Prędkość szybkiego ładowania: ' + str(best[11]) + ' km/h',
                             font=("Calibri", "16"))

        back_button = tk.Button(new_window, text='Cofnij', command=new_window.destroy)
        next_button = tk.Button(new_window, text='Sprawdź korzyści środowiskowe', command=lambda: last_step(best[10]))

        carlabel1.grid(columnspan=2, row=0, sticky=tk.EW)
        carinfo1.grid(columnspan=2, row=1, sticky=tk.EW)
        carinfo2.grid(columnspan=2, row=2, sticky=tk.EW)
        carinfo3.grid(columnspan=2, row=3, sticky=tk.EW)
        carinfo4.grid(columnspan=2, row=4, sticky=tk.EW)
        carinfo5.grid(columnspan=2, row=5, sticky=tk.EW)
        carinfo6.grid(columnspan=2, row=6, sticky=tk.EW)
        priceinfo.grid(columnspan=2, row=7, sticky=tk.EW)
        carinfo7.grid(columnspan=2, row=8, sticky=tk.EW)
        carinfo8.grid(columnspan=2, row=9, sticky=tk.EW)
        carinfo9.grid(columnspan=2, row=10, sticky=tk.EW)
        carinfo10.grid(columnspan=2, row=11, sticky=tk.EW)
        carinfo11.grid(columnspan=2, row=12, sticky=tk.EW)
        carinfo12.grid(columnspan=2, row=13, sticky=tk.EW)

        back_button.grid(column=1, row=14)
        next_button.grid(column=0, row=14)


def main_window(parameters, start):
    root = tk.Tk()

    root = create_window(root, 'BEV for You!', 600, 600, 'bev.ico')
    root.resizable(False, False)
    df = pd.read_json('base.json')
    # print(df)

    bg = tk.PhotoImage(master=root, file="bg.png")
    bgl = tk.Label(root, image=bg)
    bgl.place(x=0, y=0, relwidth=1, relheight=1)

    set_grid(root, 2, 17)

    message_info1 = tk.Label(root, text="Typ nadwozia", font=("Calibri", "16"))
    message_info2 = tk.Label(root, text="Cena (od/do)", font=("Calibri", "16"))
    message_info3 = tk.Label(root, text="Zasięg (od/do)", font=("Calibri", "16"))
    message_info4 = tk.Label(root, text="Ilość miejsc", font=("Calibri", "16"))
    message_info5 = tk.Label(root, text="Napęd", font=("Calibri", "16"))
    message_info6 = tk.Label(root, text="Prędkość maksymalna (od/do)", font=("Calibri", "16"))
    message_info7 = tk.Label(root, text="Od 0 do 100 w ile sekund? (od/do)", font=("Calibri", "16"))
    message_info8 = tk.Label(root, text="Zainteresowany dofinansowaniem?", font=("Calibri", "16"))

    combobox_body = set_combobox(root, ('Kombi', 'Kompakt', 'Minivan', 'Sedan', 'SUV', 'Kabriolet'))

    textbox_price_from, textbox_price_to = set_entry(root)

    combobox_bailout = set_combobox(root, ('Tak', 'Nie'))

    textbox_range_from, textbox_range_to = set_entry(root)

    textbox_topspeed_from, textbox_topspeed_to = set_entry(root)

    combobox_seats = set_combobox(root, (2, 4, 5, 6, 7, 8, 9))

    combobox_drive = set_combobox(root, ("Na przód", "Na tył", "Na wszystkie koła"))

    textbox_100_from, textbox_100_to = set_entry(root)

    search_button = tk.Button(root, text="Znajdź samochód", command=lambda: check_main_errors())
    back_button = tk.Button(root, text='Cofnij', command=lambda: change_window(root, start))

    def get_values():

        body_value = combobox_body.get()
        price_value = int(textbox_price_from.get()) / 4.72, int(textbox_price_to.get()) / 4.72
        range_value = int(textbox_range_from.get()), int(textbox_range_to.get())
        seats_value = int(combobox_seats.get())
        drive_value = combobox_drive.get()
        topspeed_value = int(textbox_topspeed_from.get()), int(textbox_topspeed_to.get())
        zero_to_100_value = int(textbox_100_from.get()), int(textbox_100_to.get())
        checkbox_value = combobox_bailout.get()

        if drive_value == 'Na wszystkie koła':
            drive_value = 'All wheel'
        elif drive_value == 'Na tył':
            drive_value = 'Rear wheel'
        elif drive_value == 'Na przód':
            drive_value = 'Front wheel'

        if body_value == 'Kompakt':
            body_value = 'Hatchback'
        elif body_value == 'Kombi':
            body_value = 'Station'
        elif body_value == 'Kabriolet':
            body_value = 'Cabriolet'

        values = [body_value, price_value, range_value, seats_value, drive_value, topspeed_value, zero_to_100_value,
                  parameters, checkbox_value]

        return values

    def check_main_errors():
        if combobox_body.get() != '' and combobox_drive.get() != '' and combobox_seats.get() != "" and textbox_price_from.get().isdigit() == True and textbox_price_to.get().isdigit() == True and textbox_range_from.get().isdigit() == True and textbox_range_to.get().isdigit() == True and textbox_topspeed_from.get().isdigit() == True and textbox_topspeed_to.get().isdigit() == True and textbox_100_from.get().isdigit() == True and textbox_100_to.get().isdigit() == True and combobox_bailout.get() != '':
            create_final_window(get_best(get_values()))
        else:
            messagebox.showwarning('Błąd', 'Wprowadź poprawne dane!')

    # grid settings
    message_info1.grid(columnspan=2, row=0)
    combobox_body.grid(columnspan=2, row=1, sticky=tk.EW, padx=250)
    message_info2.grid(columnspan=2, row=2)
    textbox_price_from.grid(column=0, row=3, sticky=tk.E, padx=10)
    textbox_price_to.grid(column=1, row=3, sticky=tk.W, padx=10)
    message_info8.grid(columnspan=2, row=4)
    combobox_bailout.grid(columnspan=2, row=5, sticky=tk.EW, padx=250)
    message_info3.grid(columnspan=2, row=6)
    textbox_range_from.grid(column=0, row=7, sticky=tk.E, padx=10)
    textbox_range_to.grid(column=1, row=7, sticky=tk.W, padx=10)
    message_info4.grid(columnspan=2, row=8)
    combobox_seats.grid(columnspan=2, row=9, sticky=tk.EW, padx=250)
    message_info5.grid(columnspan=2, row=10)
    combobox_drive.grid(columnspan=2, row=11, sticky=tk.EW, padx=250)
    message_info6.grid(columnspan=2, row=12)
    textbox_topspeed_from.grid(column=0, row=13, sticky=tk.E, padx=10)
    textbox_topspeed_to.grid(column=1, row=13, sticky=tk.W, padx=10)
    message_info7.grid(columnspan=2, row=14)
    textbox_100_from.grid(column=0, row=15, sticky=tk.E, padx=10)
    textbox_100_to.grid(column=1, row=15, sticky=tk.W, padx=10)
    search_button.grid(column=0, row=16)
    back_button.grid(column=1, row=16)

    # x = combobox_body.get()
    # print(x)

    def on_closing_main():
        if messagebox.askokcancel("Zamknij", "Czy na pewno chcesz wyjść?"):
            root.destroy()
            start.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing_main)
    root.mainloop()
