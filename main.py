import tkinter
from tkinter import *
from PIL import Image, ImageTk
import os
import time
import csv


root = Tk()
images = []
i = 0

for filename in os.listdir("images"):
   images.append(filename)

img = ImageTk.PhotoImage(Image.open("images\\" + images[0]))
panel = tkinter.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

root.title(str(i + 1) + "/" + str(len(images)) + " Images")

with open('picture.csv', mode='w', newline='') as picture:
    fieldnames = ['pic_name', 'result']
    picture_writer = csv.DictWriter(picture, fieldnames=fieldnames)

    picture_writer.writeheader()

def callbackGood(e):
    global i
    i = i + 1
    img2 = ImageTk.PhotoImage(Image.open("images\\" + images[i]))
    panel.configure(image=img2)
    panel.image = img2
    root.title(str(i + 1) + "/" + str(len(images)) + " Images")
    picture_writer.writerow({'pic_name': str(i + 1), 'result': 1})

def callbackBad(e):
    global i
    i = i + 1
    img2 = ImageTk.PhotoImage(Image.open("images\\" + images[i]))
    panel.configure(image=img2)
    panel.image = img2
    root.title(str(i + 1) + "/" + str(len(images)) + " Images")
    picture_writer.writerow({'pic_name': str(i + 1), 'result': 0})


root.bind("<Left>", callbackGood)
root.bind("<Right>", callbackBad)
root.mainloop()

