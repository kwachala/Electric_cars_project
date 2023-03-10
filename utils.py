import tkinter as tk
from tkinter import ttk
import pandas as pd


def create_window(root, title, width, height, icon):
    root.title(title)

    # set size of main window
    window_width = width
    window_height = height

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # set main icon
    root.iconbitmap(icon)

    return root


def set_grid(root, number_of_columns, number_of_rows):
    for i in range(number_of_columns):
        root.columnconfigure(i, weight=1)
    for j in range(number_of_rows):
        root.rowconfigure(j, weight=1)


def set_entry(root):
    text_from = tk.StringVar()
    textbox_from = ttk.Entry(root, textvariable=text_from)
    text_to = tk.StringVar()
    textbox_to = ttk.Entry(root, textvariable=text_to)

    return textbox_from, textbox_to


def set_combobox(root, values):
    combobox = ttk.Combobox(root, state='readonly')
    combobox['values'] = values

    return combobox


def compare_parameters(parameter, car1, car2):
    score = car1[parameter] / car2[parameter]

    return score


def change_window(first_window, second_window):
    first_window.destroy()
    second_window.deiconify()

def get_emissivity(efficiency):
    df = pd.read_excel('emissivity_data.xlsx')
    df = df.loc[df['kW'] == int(efficiency/10)]
    for index, rows in df.iterrows():
        my_list = [int(rows.ev), int(rows.benzyna), int(rows.diesel)]
    emissivity = my_list

    return emissivity