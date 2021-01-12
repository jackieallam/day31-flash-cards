import tkinter as tk
import pandas
import random as r
import os.path

BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
BLACK = "#000000"

# Check if the words_to_learn.csv file exists and use that list:
if os.path.isfile("data/words_to_learn.csv"):
    try:
        words_df = pandas.read_csv("data/words_to_learn.csv")
    except pandas.errors.EmptyDataError:
        to_learn = []
    else:
        to_learn = words_df.to_dict(orient="records")
# If not, then use the original words list:
else:
    words_df = pandas.read_csv("data/french_words.csv")
    to_learn = words_df.to_dict(orient="records")

current_card = {}

# ------------------------- SHOW NEW CARD ---------------------------- #


def next_card():
    """Show the next card front (French), also sets/resets a 3 second timer"""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    if len(to_learn) > 0:
        # If there are still words in the list, show the next word
        current_card = r.choice(to_learn)
        canvas.itemconfig(card_color, image=card_front)
        canvas.itemconfig(card_title, text="French", fill=BLACK)
        canvas.itemconfig(card_word, text=current_card["French"], fill=BLACK)
        flip_timer = window.after(3000, func=flip_card)
    else:
        # If no words left, display the "Congratulations"
        canvas.itemconfig(card_color, image=card_front)
        canvas.itemconfig(card_title, text="You have learned all the words", fill=BLACK)
        canvas.itemconfig(card_word, text="Congratulations!", fill=BLACK)
        unknown_button["state"] = "disabled"
        known_button["state"] = "disabled"


# --------------------------- FLIP CARD ------------------------------ #

def flip_card():
    """Show the back side of the card (English)"""
    canvas.itemconfig(card_color, image=card_back)
    canvas.itemconfig(card_title, text="English", fill=WHITE)
    canvas.itemconfig(card_word, text=current_card["English"], fill=WHITE)


# -------------------------- REMOVE CARD ----------------------------- #

def remove_card():
    """Removes the current card from the list of words to learn, then shows the next card"""
    to_learn.remove(current_card)
    to_learn_df = pandas.DataFrame(to_learn)
    to_learn_df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------ #
window = tk.Tk()
window.title("Flashy - Learn French")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# ------------------- CANVAS: CARD BG & TEXT ------------------------- #
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = tk.PhotoImage(file="images/card_front.png")
card_back = tk.PhotoImage(file="images/card_back.png")
card_color = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# ----------------------------- BUTTONS ------------------------------- #
cross_img = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(command=next_card, image=cross_img, highlightthickness=0, bg=BACKGROUND_COLOR,
                           activebackground=BACKGROUND_COLOR)
unknown_button.grid(column=0, row=1)

checkmark_img = tk.PhotoImage(file="images/right.png")
known_button = tk.Button(command=remove_card, image=checkmark_img, highlightthickness=0, bg=BACKGROUND_COLOR,
                         activebackground=BACKGROUND_COLOR)
known_button.grid(column=1, row=1)

next_card()

window.mainloop()
