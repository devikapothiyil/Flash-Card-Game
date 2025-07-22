#Tick Button means word already known
#Cross button means next word

import random
import tkinter as tk
from tkinter import  *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card , flip_timer
    root.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title,text="French",fill="black")
    canvas.itemconfig(card_content,text=current_card["French"],fill="black")
    canvas.itemconfig(card_bg, image=front_image)
    flip_timer = root.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_bg,image=back_image)
    canvas.itemconfig(card_title, text="English",fill="white")
    canvas.itemconfig(card_content, text=current_card["English"],fill="white")

def is_known():
    to_learn.remove(current_card)
    datafile = pd.DataFrame(to_learn)
    datafile.to_csv("data/words_to_learn.csv",index=False)
    next_card()

root = tk.Tk()
root.title("FLASHY : The Flash Card Game")
root.config(bg=BACKGROUND_COLOR,padx=50,pady=50)

flip_timer = root.after(3000,func=flip_card)

canvas = tk.Canvas(width= 800 , height= 526)
front_image = PhotoImage(file = "images/card_front.png")
back_image = PhotoImage(file = "images/card_back.png")
card_bg = canvas.create_image(400,263,image=front_image)
card_title = canvas.create_text(400,150,text="",font=("Arial",40,"italic"))
card_content = canvas.create_text(400,263,text="",font=("Arial",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=2)

tick_image = PhotoImage(file="images/right.png")
tick_button = tk.Button(root,image=tick_image,highlightthickness=0,command=is_known)
tick_button.grid(row=1,column=1)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = tk.Button(root,image=cross_image,highlightthickness=0,command=next_card)
cross_button.grid(row=1,column=0)

next_card()

root.mainloop()
